import asyncio
import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import httpx

# Imports condicionais
try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    
try:
    from google.cloud import vision
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False

from app.db.database import AsyncSessionLocal
from app.db.models import Contract, User, RiskFactor
from app.agents.factory import AgentFactory
from app.services.rag_service import get_rag_service
from app.services.email_service import email_service
from app.services.ocr_service import ocr_service
from app.services.llm_router import LLMRouter
from app.services.storage_service import r2_service
from app.core.config import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Processador completo de documentos com OCR e análise jurídica
    Pipeline: Upload → OCR → Classification → Analysis → Storage
    """
    
    def __init__(self):
        self.agent_factory = AgentFactory()
        self.llm_router = LLMRouter()
        
        # R2 storage service (already initialized)
        self.storage_service = r2_service
        
        # Legacy S3 for backward compatibility (optional)
        self.s3_client = None
        if BOTO3_AVAILABLE and getattr(settings, 'AWS_ACCESS_KEY_ID', None):
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION
                )
            except Exception as e:
                logger.warning(f"AWS S3 não configurado: {e}")
        else:
            logger.info("AWS S3 não disponível - usando Cloudflare R2 como storage principal")
    
    async def process_contract_file(
        self, 
        file_content: bytes, 
        filename: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Pipeline completo de processamento de contrato
        1. Extração de texto via OCR
        2. Classificação do tipo de contrato
        3. Análise de complexidade para roteamento
        4. Análise jurídica especializada
        5. Compilação de resultados
        """
        
        logger.info(f"🔄 Iniciando processamento: {filename}")
        
        try:
            # 1. Extração de texto via OCR
            logger.info("📄 Extraindo texto do documento...")
            ocr_result = await ocr_service.extract_text_from_file(file_content, filename)
            
            if not ocr_result.get("text") or len(ocr_result["text"].strip()) < 50:
                return {
                    "success": False,
                    "error": "Não foi possível extrair texto suficiente do documento",
                    "ocr_result": ocr_result
                }
            
            text_content = ocr_result["text"]
            
            # 2. Classificação do tipo de contrato
            logger.info("🔍 Classificando tipo de contrato...")
            classifier = self.agent_factory.get_classifier()
            
            try:
                contract_type = await classifier.classify_contract(text_content)
            except Exception as e:
                logger.warning(f"Erro na classificação, usando 'generico': {e}")
                contract_type = "generico"
            
            # 3. Análise de complexidade para roteamento
            logger.info("📊 Analisando complexidade...")
            try:
                complexity = await self.llm_router.analyze_complexity(text_content)
                selected_model = self.llm_router.route_to_best_model(text_content, {})
            except Exception as e:
                logger.warning(f"Erro no roteamento, usando modelo padrão: {e}")
                complexity = "medium"
                selected_model = {"provider": "gemini_flash", "model": "gemini-1.5-flash"}
            
            # 4. Análise especializada
            logger.info(f"⚖️ Analisando com agente {contract_type}...")
            specialist = self.agent_factory.get_specialist(contract_type)
            
            try:
                analysis_result = await specialist.analyze_contract(
                    contract_content=text_content,
                    user_context={"user_id": user_id} if user_id else None
                )
            except Exception as e:
                logger.error(f"Erro na análise especializada: {e}")
                # Fallback com análise básica
                analysis_result = {
                    "risk_level": "medium",
                    "key_findings": ["Documento processado com análise limitada"],
                    "summary": "Análise básica devido a erro no processamento especializado",
                    "recommendations": ["Revisar documento manualmente"],
                    "error": str(e)
                }
            
            # 5. Compilar resultado final
            final_result = {
                "success": True,
                "filename": filename,
                "contract_type": contract_type,
                "ocr_result": {
                    "method": ocr_result["method"],
                    "confidence": ocr_result["confidence"],
                    "pages": ocr_result.get("pages", 1),
                    "processing_time": ocr_result.get("processing_time", "N/A")
                },
                "complexity": {
                    "level": complexity,
                    "model_used": selected_model
                },
                "analysis": analysis_result,
                "processing_metadata": {
                    "ocr_available": ocr_service.is_available(),
                    "text_length": len(text_content),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            logger.info(f"✅ Processamento concluído: {filename}")
            return final_result
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento de {filename}: {e}")
            return {
                "success": False,
                "filename": filename,
                "error": str(e),
                "ocr_available": ocr_service.is_available(),
                "timestamp": datetime.now().isoformat()
            }

    async def process_contract(self, contract_id: str) -> Dict[str, Any]:
        """
        Processa contrato existente no banco de dados
        DEPRECATED: Use process_contract_file para novos uploads
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
    
    async def _download_file(self, file_id_or_url: str) -> bytes:
        """Download file from Cloudflare R2 storage"""
        try:
            logger.info(f"Downloading file: {file_id_or_url}")
            
            # If it's a file_id (from new R2 system), need to create a mock user for download
            # In production, this should be called with proper user context
            if not file_id_or_url.startswith('http'):
                # This is a file_id, we need user context to download
                # For now, create a temporary download using direct R2 access
                # NOTE: Using user_id=1 as fallback - in production get from contract.owner_id
                s3_key = await self.storage_service._find_file_key(file_id_or_url, user_id=1)
                
                if not s3_key:
                    raise ValueError(f"File not found: {file_id_or_url}")
                
                # Direct download from R2
                response = self.storage_service.s3_client.get_object(
                    Bucket=self.storage_service.bucket_name,
                    Key=s3_key
                )
                
                file_content = response['Body'].read()
                logger.info(f"Successfully downloaded {len(file_content)} bytes from R2")
                return file_content
                
            else:
                # Legacy URL download
                async with httpx.AsyncClient() as client:
                    response = await client.get(file_id_or_url)
                    response.raise_for_status()
                    return response.content
                    
        except Exception as e:
            logger.error(f"Error downloading file {file_id_or_url}: {e}")
            raise
    
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
            self.agent_factory = AgentFactory(None, get_rag_service())
        
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

    async def process_contract_from_r2(
        self, 
        contract_id: str, 
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a contract that's already uploaded to R2 storage
        This method provides proper user context for R2 operations
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
                
                # Get user for R2 operations
                user_result = await db.execute(
                    select(User).where(User.id == user_id)
                )
                user = user_result.scalar_one_or_none()
                
                if not user:
                    raise ValueError(f"User {user_id} not found")
                
                # Update status to processing
                contract.processing_status = "processing"
                await db.commit()
                
                logger.info(f"🔄 Processing contract {contract_id} for user {user_id}")
                
                # Download file from R2 with proper user context
                if contract.file_url:
                    file_content, file_metadata = await self.storage_service.download_file(
                        file_id=contract.file_url,
                        user=user,
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                    
                    # Process the file content
                    processing_result = await self.process_contract_file(
                        file_content=file_content,
                        filename=file_metadata.original_name,
                        user_id=str(user_id)
                    )
                    
                    if processing_result.get("success"):
                        # Update contract with results
                        contract.extracted_text = processing_result.get("analysis", {}).get("text", "")
                        contract.ocr_confidence = processing_result.get("ocr_confidence", 0.0)
                        contract.contract_type = processing_result.get("contract_type", "unknown")
                        contract.processing_status = "completed"
                        contract.analysis_results = processing_result.get("analysis", {})
                        
                        # Calculate risk level from analysis
                        analysis = processing_result.get("analysis", {})
                        if "risk_level" in analysis:
                            contract.risk_level = analysis["risk_level"]
                        
                        await db.commit()
                        
                        # Send notification
                        await self._send_completion_notification(contract, db)
                        
                        logger.info(f"✅ Successfully processed contract {contract_id}")
                        
                        return {
                            "status": "completed",
                            "contract_id": contract_id,
                            "processing_result": processing_result
                        }
                    else:
                        # Processing failed
                        contract.processing_status = "failed"
                        contract.analysis_results = {"error": processing_result.get("error", "Unknown error")}
                        await db.commit()
                        
                        return {
                            "status": "failed",
                            "contract_id": contract_id,
                            "error": processing_result.get("error", "Processing failed")
                        }
                else:
                    raise ValueError("Contract has no file_url")
                    
            except Exception as e:
                logger.error(f"❌ Error processing contract {contract_id}: {e}")
                
                # Update contract status to failed
                try:
                    contract.processing_status = "failed"
                    contract.analysis_results = {"error": str(e)}
                    await db.commit()
                except:
                    pass  # Don't fail if we can't update status
                
                return {
                    "status": "error",
                    "contract_id": contract_id,
                    "error": str(e)
                }

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
