"""
Electronic Signature Service using D4Sign API
"""
import os
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.subscription import SignatureRequest, Signer
from app.db.models import User, Contract
from app.core.config import settings

class SignatureService:
    """Service for handling electronic signatures via D4Sign"""
    
    def __init__(self, db: Session):
        self.db = db
        self.base_url = "https://secure.d4sign.com.br/api/v1"
        self.token = settings.D4SIGN_TOKEN
        self.crypto_key = settings.D4SIGN_CRYPTO_KEY
        self.folder_uuid = settings.D4SIGN_FOLDER_UUID
        
    async def create_signature_request(
        self,
        user_id: str,
        document_file: bytes,
        document_name: str,
        signers: List[Dict[str, str]],
        contract_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new signature request"""
        
        try:
            # 1. Upload document to D4Sign
            document_uuid = await self._upload_document(document_file, document_name)
            
            # 2. Create signature request record
            signature_request = SignatureRequest(
                user_id=user_id,
                contract_id=contract_id,
                document_name=document_name,
                d4sign_document_uuid=document_uuid,
                d4sign_folder_uuid=self.folder_uuid,
                signers_count=len(signers),
                signers_data=signers,
                expires_at=datetime.utcnow() + timedelta(days=30)  # 30 days to sign
            )
            
            self.db.add(signature_request)
            await self.db.flush()  # Get the ID
            
            # 3. Add signers to D4Sign document
            signature_links = []
            for signer_data in signers:
                signer_result = await self._add_signer(document_uuid, signer_data)
                
                # Create signer record
                signer = Signer(
                    signature_request_id=signature_request.id,
                    name=signer_data['name'],
                    email=signer_data['email'],
                    document=signer_data.get('document'),
                    phone=signer_data.get('phone'),
                    d4sign_signer_uuid=signer_result.get('uuid')
                )
                self.db.add(signer)
                
                signature_links.append({
                    "name": signer_data['name'],
                    "email": signer_data['email'],
                    "signature_url": signer_result.get('signature_url')
                })
            
            # 4. Configure webhook
            await self._configure_webhook(document_uuid)
            
            # 5. Send document for signature
            send_result = await self._send_to_signature(document_uuid)
            
            signature_request.status = "sent"
            signature_request.sent_at = datetime.utcnow()
            
            await self.db.commit()
            
            return {
                "signature_request_id": str(signature_request.id),
                "document_uuid": document_uuid,
                "status": "sent",
                "signers": signature_links,
                "expires_at": signature_request.expires_at.isoformat()
            }
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error creating signature request: {str(e)}")
    
    async def _upload_document(self, file_content: bytes, document_name: str) -> str:
        """Upload document to D4Sign"""
        
        async with httpx.AsyncClient() as client:
            files = {
                'file': (document_name, file_content, 'application/pdf')
            }
            data = {
                'tokenAPI': self.token,
                'cryptKey': self.crypto_key,
                'folder_uuid': self.folder_uuid
            }
            
            response = await client.post(
                f"{self.base_url}/documents/{self.folder_uuid}/upload",
                files=files,
                data=data,
                timeout=30.0
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"D4Sign upload error: {response.text}")
            
            result = response.json()
            
            if result.get('message') != 'success':
                raise Exception(f"D4Sign upload failed: {result}")
            
            return result['uuid']
    
    async def _add_signer(self, document_uuid: str, signer_data: Dict[str, str]) -> Dict[str, Any]:
        """Add signer to D4Sign document"""
        
        async with httpx.AsyncClient() as client:
            data = {
                'tokenAPI': self.token,
                'cryptKey': self.crypto_key,
                'email': signer_data['email'],
                'act': '1',  # Sign action
                'foreign': '0',  # Brazilian
                'certificadoicpbr': '0',  # No ICP certificate required
                'assinatura_presencial': '0',  # Remote signature
                'docauth': '1',  # Authentication via SMS/Email
                'docauthandselfie': '0',  # No selfie required
                'embed_methodauth': 'sms',  # SMS authentication
                'embed_smsnumber': signer_data.get('phone', ''),
                'workflow': '0'  # No workflow
            }
            
            if signer_data.get('phone'):
                data['whatsapp'] = '1'
                data['embed_smsnumber'] = signer_data['phone']
            
            response = await client.post(
                f"{self.base_url}/documents/{document_uuid}/createlist",
                data=data,
                timeout=30.0
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"D4Sign add signer error: {response.text}")
            
            result = response.json()
            
            if result.get('message') != 'success':
                raise Exception(f"Failed to add signer: {result}")
            
            return {
                'uuid': result.get('uuid'),
                'signature_url': result.get('url_sign')
            }
    
    async def _configure_webhook(self, document_uuid: str):
        """Configure webhook for document status updates"""
        
        webhook_url = f"{settings.API_BASE_URL}/api/v1/signatures/webhook"
        
        async with httpx.AsyncClient() as client:
            data = {
                'tokenAPI': self.token,
                'cryptKey': self.crypto_key,
                'url': webhook_url
            }
            
            response = await client.post(
                f"{self.base_url}/documents/{document_uuid}/webhooks",
                data=data,
                timeout=30.0
            )
            
            # Webhook configuration is optional, don't fail if it doesn't work
            if response.status_code not in [200, 201]:
                print(f"Warning: Could not configure webhook for document {document_uuid}")
    
    async def _send_to_signature(self, document_uuid: str) -> Dict[str, Any]:
        """Send document to signers"""
        
        async with httpx.AsyncClient() as client:
            data = {
                'tokenAPI': self.token,
                'cryptKey': self.crypto_key,
                'message': 'Documento enviado para assinatura via Democratiza AI'
            }
            
            response = await client.post(
                f"{self.base_url}/documents/{document_uuid}/sendtosigner",
                data=data,
                timeout=30.0
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"D4Sign send error: {response.text}")
            
            return response.json()
    
    async def get_signature_status(self, signature_request_id: str) -> Dict[str, Any]:
        """Get current status of signature request"""
        
        result = await self.db.execute(
            select(SignatureRequest).where(SignatureRequest.id == signature_request_id)
        )
        signature_request = result.scalar_one_or_none()
        
        if not signature_request:
            raise ValueError("Signature request not found")
        
        # Get updated status from D4Sign
        d4sign_status = await self._get_d4sign_document_status(signature_request.d4sign_document_uuid)
        
        # Update local status if needed
        if d4sign_status.get('status_id') == '3':  # Completed
            if signature_request.status != "signed":
                signature_request.status = "signed"
                signature_request.completed_at = datetime.utcnow()
                signature_request.signers_completed = signature_request.signers_count
                await self.db.commit()
        
        # Get signers info
        signers_result = await self.db.execute(
            select(Signer).where(Signer.signature_request_id == signature_request_id)
        )
        signers = signers_result.scalars().all()
        
        return {
            "signature_request_id": signature_request_id,
            "document_name": signature_request.document_name,
            "status": signature_request.status,
            "progress_percentage": signature_request.progress_percentage,
            "signers_completed": signature_request.signers_completed,
            "signers_total": signature_request.signers_count,
            "created_at": signature_request.created_at.isoformat(),
            "completed_at": signature_request.completed_at.isoformat() if signature_request.completed_at else None,
            "expires_at": signature_request.expires_at.isoformat() if signature_request.expires_at else None,
            "signers": [
                {
                    "name": signer.name,
                    "email": signer.email,
                    "signed": signer.signed,
                    "signed_at": signer.signed_at.isoformat() if signer.signed_at else None
                }
                for signer in signers
            ],
            "d4sign_info": d4sign_status
        }
    
    async def _get_d4sign_document_status(self, document_uuid: str) -> Dict[str, Any]:
        """Get document status from D4Sign API"""
        
        async with httpx.AsyncClient() as client:
            params = {
                'tokenAPI': self.token,
                'cryptKey': self.crypto_key
            }
            
            response = await client.get(
                f"{self.base_url}/documents/{document_uuid}",
                params=params,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Could not fetch status: {response.text}"}
    
    async def download_signed_document(self, signature_request_id: str) -> Optional[bytes]:
        """Download the signed document"""
        
        result = await self.db.execute(
            select(SignatureRequest).where(SignatureRequest.id == signature_request_id)
        )
        signature_request = result.scalar_one_or_none()
        
        if not signature_request:
            raise ValueError("Signature request not found")
        
        if signature_request.status != "signed":
            raise ValueError("Document is not yet fully signed")
        
        async with httpx.AsyncClient() as client:
            params = {
                'tokenAPI': self.token,
                'cryptKey': self.crypto_key
            }
            
            response = await client.get(
                f"{self.base_url}/documents/{signature_request.d4sign_document_uuid}/download",
                params=params,
                timeout=60.0
            )
            
            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"Download failed: {response.text}")
    
    async def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process D4Sign webhook notifications"""
        
        try:
            document_uuid = webhook_data.get('uuid_doc')
            event_type = webhook_data.get('type_event')
            
            if not document_uuid:
                return {"status": "ignored", "reason": "No document UUID"}
            
            # Find signature request
            result = await self.db.execute(
                select(SignatureRequest).where(SignatureRequest.d4sign_document_uuid == document_uuid)
            )
            signature_request = result.scalar_one_or_none()
            
            if not signature_request:
                return {"status": "ignored", "reason": "Signature request not found"}
            
            # Update webhook events log
            if not signature_request.webhook_events:
                signature_request.webhook_events = []
            
            signature_request.webhook_events.append({
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": event_type,
                "data": webhook_data
            })
            
            # Process different event types
            if event_type == "doc_signed":
                await self._handle_document_signed(signature_request, webhook_data)
            elif event_type == "doc_finished":
                await self._handle_document_finished(signature_request, webhook_data)
            
            await self.db.commit()
            
            return {"status": "processed", "event_type": event_type}
            
        except Exception as e:
            await self.db.rollback()
            return {"status": "error", "reason": str(e)}
    
    async def _handle_document_signed(self, signature_request: SignatureRequest, webhook_data: Dict[str, Any]):
        """Handle individual signer completion"""
        
        signer_email = webhook_data.get('signer_email')
        
        if signer_email:
            # Update signer record
            signer_result = await self.db.execute(
                select(Signer).where(
                    Signer.signature_request_id == signature_request.id,
                    Signer.email == signer_email
                )
            )
            signer = signer_result.scalar_one_or_none()
            
            if signer and not signer.signed:
                signer.signed = True
                signer.signed_at = datetime.utcnow()
                signature_request.signers_completed += 1
    
    async def _handle_document_finished(self, signature_request: SignatureRequest, webhook_data: Dict[str, Any]):
        """Handle document completion"""
        
        signature_request.status = "signed"
        signature_request.completed_at = datetime.utcnow()
        signature_request.signers_completed = signature_request.signers_count
        
        # Update all signers as signed if not already
        signers_result = await self.db.execute(
            select(Signer).where(Signer.signature_request_id == signature_request.id)
        )
        signers = signers_result.scalars().all()
        
        for signer in signers:
            if not signer.signed:
                signer.signed = True
                signer.signed_at = datetime.utcnow()
    
    async def get_user_signature_requests(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all signature requests for a user"""
        
        result = await self.db.execute(
            select(SignatureRequest)
            .where(SignatureRequest.user_id == user_id)
            .order_by(SignatureRequest.created_at.desc())
        )
        signature_requests = result.scalars().all()
        
        return [
            {
                "id": str(sr.id),
                "document_name": sr.document_name,
                "status": sr.status,
                "signers_completed": sr.signers_completed,
                "signers_total": sr.signers_count,
                "progress_percentage": sr.progress_percentage,
                "created_at": sr.created_at.isoformat(),
                "completed_at": sr.completed_at.isoformat() if sr.completed_at else None,
                "expires_at": sr.expires_at.isoformat() if sr.expires_at else None
            }
            for sr in signature_requests
        ]
    
    async def cancel_signature_request(self, signature_request_id: str, user_id: str) -> Dict[str, Any]:
        """Cancel a signature request"""
        
        result = await self.db.execute(
            select(SignatureRequest).where(
                SignatureRequest.id == signature_request_id,
                SignatureRequest.user_id == user_id
            )
        )
        signature_request = result.scalar_one_or_none()
        
        if not signature_request:
            raise ValueError("Signature request not found")
        
        if signature_request.status == "signed":
            raise ValueError("Cannot cancel a completed signature")
        
        # Cancel in D4Sign (if API supports it)
        # For now, just update local status
        signature_request.status = "cancelled"
        await self.db.commit()
        
        return {
            "signature_request_id": signature_request_id,
            "status": "cancelled"
        }