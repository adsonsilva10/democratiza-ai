import asyncio
import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import boto3
from google.cloud import vision
import httpx
from datetime import datetime

from app.db.database import AsyncSessionLocal
from app.db.models import Contract, User, RiskFactor
from app.agents.factory import AgentFactory
from app.services.rag_service import rag_service
from app.services.email_service import email_service
from app.core.config import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Background worker for processing uploaded contracts"""
    
    def __init__(self):
        # Initialize cloud services
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        self.vision_client = vision.ImageAnnotatorClient()
        
        # Initialize agent factory (will need proper clients)
        self.agent_factory = None  # Will be initialized with proper clients
    
    async def process_contract(self, contract_id: str) -> Dict[str, Any]:
        """
        Main processing pipeline for a contract:
        1. Download file from storage
        2. Extract text via OCR
        3. Classify contract type
        4. Analyze with specialized agent
        5. Save results
        6. Send notification email
        """
        async with AsyncSessionLocal() as db:
            try:
                # Get contract record
                result = await db.execute(
                    select(Contract).where(Contract.id == contract_id)
                )
                contract = result.scalar_one_or_none()
                
                if not contract:
                    raise ValueError(f"Contract {contract_id} not found")
                
                # Update status to processing
                contract.processing_status = "processing"
                await db.commit()
                
                logger.info(f"Starting processing for contract {contract_id}")
                
                # Step 1: Download file from Cloudflare R2
                file_content = await self._download_file(contract.file_url)
                
                # Step 2: Extract text via OCR
                extracted_text, ocr_confidence = await self._extract_text_from_file(
                    file_content, 
                    contract.mime_type
                )
                
                # Update contract with extracted text
                contract.extracted_text = extracted_text
                contract.ocr_confidence = ocr_confidence
                await db.commit()
                
                # Step 3 & 4: Analyze with AI agents
                analysis_results = await self._analyze_contract_with_agents(
                    extracted_text, 
                    contract_id
                )
                
                # Step 5: Save analysis results
                await self._save_analysis_results(contract, analysis_results, db)
                
                # Step 6: Send notification email
                await self._send_completion_notification(contract, db)
                
                logger.info(f"Successfully processed contract {contract_id}")
                
                return {
                    "status": "success",
                    "contract_id": contract_id,
                    "risk_level": contract.risk_level,
                    "confidence_score": contract.confidence_score
                }
                
            except Exception as e:
                logger.error(f"Error processing contract {contract_id}: {str(e)}")
                
                # Update contract status to failed
                contract.processing_status = "failed"
                await db.commit()
                
                return {
                    "status": "error",
                    "contract_id": contract_id,
                    "error": str(e)
                }
    
    async def _download_file(self, file_url: str) -> bytes:
        """Download file from Cloudflare R2 storage"""
        # This would implement Cloudflare R2 download
        # For now, return placeholder
        logger.info(f"Downloading file from {file_url}")
        return b"sample_content"  # Placeholder
    
    async def _extract_text_from_file(self, file_content: bytes, mime_type: str) -> tuple[str, float]:
        """Extract text from file using Google Cloud Vision OCR"""
        
        if mime_type == "application/pdf":
            # For PDF files, convert to images first then OCR
            return await self._extract_text_from_pdf(file_content)
        elif mime_type.startswith("image/"):
            # Direct OCR for images
            return await self._extract_text_from_image(file_content)
        else:
            raise ValueError(f"Unsupported file type: {mime_type}")
    
    async def _extract_text_from_pdf(self, pdf_content: bytes) -> tuple[str, float]:
        """Extract text from PDF using OCR"""
        # This would implement PDF to image conversion + OCR
        # For now, return placeholder
        logger.info("Extracting text from PDF")
        return "Texto extraído do PDF...", 0.95
    
    async def _extract_text_from_image(self, image_content: bytes) -> tuple[str, float]:
        """Extract text from image using Google Cloud Vision"""
        try:
            image = vision.Image(content=image_content)
            
            # Perform OCR
            response = self.vision_client.text_detection(image=image)
            texts = response.text_annotations
            
            if texts:
                extracted_text = texts[0].description
                # Calculate average confidence
                confidence = sum([
                    vertex.confidence for text in texts 
                    for vertex in text.bounding_poly.vertices 
                    if hasattr(vertex, 'confidence')
                ]) / len(texts) if texts else 0.0
                
                return extracted_text, confidence
            else:
                return "", 0.0
                
        except Exception as e:
            logger.error(f"OCR error: {str(e)}")
            return "", 0.0
    
    async def _analyze_contract_with_agents(self, contract_text: str, contract_id: str) -> Dict[str, Any]:
        """Analyze contract using AI agent factory"""
        
        # Initialize agent factory with proper clients
        # TODO: Initialize with actual Claude client and RAG service
        if not self.agent_factory:
            self.agent_factory = AgentFactory(None, rag_service)
        
        try:
            # Use agent factory for analysis
            analysis_results = await self.agent_factory.analyze_contract(contract_text)
            return analysis_results
            
        except Exception as e:
            logger.error(f"Agent analysis error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "classification": {"contract_type": "unknown", "confidence": 0.0},
                "analysis": None
            }
    
    async def _save_analysis_results(
        self, 
        contract: Contract, 
        analysis_results: Dict[str, Any], 
        db: AsyncSession
    ):
        """Save analysis results to database"""
        
        if analysis_results["status"] == "success":
            classification = analysis_results["classification"]
            analysis = analysis_results["analysis"]
            
            # Update contract
            contract.contract_type = classification["contract_type"]
            contract.risk_level = analysis["risk_level"]
            contract.analysis_summary = analysis["summary"]
            contract.analysis_results = analysis_results
            contract.confidence_score = analysis["confidence_score"]
            contract.analyzed_at = datetime.utcnow()
            contract.processing_status = "completed"
            
            # Save risk factors
            for risk_factor_data in analysis["risk_factors"]:
                risk_factor = RiskFactor(
                    contract_id=contract.id,
                    risk_type=risk_factor_data["type"],
                    description=risk_factor_data["description"],
                    severity=risk_factor_data["severity"],
                    clause_text=risk_factor_data.get("clause"),
                    recommendation=risk_factor_data.get("recommendation"),
                    legal_basis=risk_factor_data.get("legal_basis")
                )
                db.add(risk_factor)
        
        else:
            # Analysis failed
            contract.processing_status = "failed"
            contract.analysis_results = analysis_results
        
        await db.commit()
    
    async def _send_completion_notification(self, contract: Contract, db: AsyncSession):
        """Send email notification when analysis is complete"""
        
        if contract.processing_status != "completed":
            return
        
        # Get contract owner
        result = await db.execute(
            select(User).where(User.id == contract.owner_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            await email_service.send_analysis_complete_email(
                user_email=user.email,
                user_name=user.full_name,
                contract_title=contract.title,
                risk_level=contract.risk_level or "Não avaliado",
                contract_id=str(contract.id)
            )

# SQS Message handler
class SQSHandler:
    """Handle SQS messages for document processing"""
    
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.processor = DocumentProcessor()
    
    async def start_worker(self):
        """Start SQS worker to process messages"""
        
        logger.info("Starting SQS worker...")
        
        while True:
            try:
                # Poll for messages
                response = self.sqs.receive_message(
                    QueueUrl=settings.SQS_QUEUE_URL,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=20,  # Long polling
                    MessageAttributeNames=['All']
                )
                
                messages = response.get('Messages', [])
                
                for message in messages:
                    await self._process_message(message)
                    
            except Exception as e:
                logger.error(f"SQS worker error: {str(e)}")
                await asyncio.sleep(30)  # Wait before retrying
    
    async def _process_message(self, message: Dict[str, Any]):
        """Process individual SQS message"""
        
        try:
            # Parse message
            message_body = message['Body']
            contract_id = message_body  # Assuming message body contains contract ID
            
            # Process contract
            result = await self.processor.process_contract(contract_id)
            
            if result["status"] == "success":
                # Delete message from queue
                self.sqs.delete_message(
                    QueueUrl=settings.SQS_QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
                logger.info(f"Successfully processed and deleted message for contract {contract_id}")
            else:
                logger.error(f"Failed to process contract {contract_id}: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"Error processing SQS message: {str(e)}")

# Main function to run the worker
async def main():
    """Main function to start the document processor worker"""
    
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting Document Processor Worker")
    
    handler = SQSHandler()
    await handler.start_worker()

if __name__ == "__main__":
    asyncio.run(main())
