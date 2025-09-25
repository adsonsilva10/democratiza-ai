"""
Electronic Signature API endpoints
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.services.signature_service import SignatureService
from app.api.v1.auth import get_current_user
from app.db.models import User

router = APIRouter()

class SignerData(BaseModel):
    """Signer information"""
    name: str
    email: str
    document: str = ""  # CPF/CNPJ
    phone: str = ""

class CreateSignatureRequest(BaseModel):
    """Request model for creating signature request"""
    signers: List[SignerData]
    contract_id: str = ""

@router.post("/create")
async def create_signature_request(
    document: UploadFile = File(...),
    signers_json: str = Form(...),
    contract_id: str = Form(""),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new signature request"""
    
    try:
        # Validate file type
        if document.content_type not in ["application/pdf"]:
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse signers data
        import json
        try:
            signers_data = json.loads(signers_json)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid signers JSON format")
        
        # Validate signers
        if not signers_data or len(signers_data) == 0:
            raise HTTPException(status_code=400, detail="At least one signer is required")
        
        # Read document content
        document_content = await document.read()
        
        signature_service = SignatureService(db)
        
        result = await signature_service.create_signature_request(
            user_id=str(current_user.id),
            document_file=document_content,
            document_name=document.filename,
            signers=signers_data,
            contract_id=contract_id if contract_id else None
        )
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{signature_request_id}/status")
async def get_signature_status(
    signature_request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get signature request status"""
    
    try:
        signature_service = SignatureService(db)
        result = await signature_service.get_signature_status(signature_request_id)
        
        return {
            "status": "success",
            "data": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{signature_request_id}/download")
async def download_signed_document(
    signature_request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download the signed document"""
    
    try:
        signature_service = SignatureService(db)
        document_content = await signature_service.download_signed_document(signature_request_id)
        
        from fastapi.responses import Response
        
        return Response(
            content=document_content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=signed_document_{signature_request_id}.pdf"}
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/requests")
async def get_user_signature_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all signature requests for current user"""
    
    try:
        signature_service = SignatureService(db)
        requests = await signature_service.get_user_signature_requests(str(current_user.id))
        
        return {
            "status": "success",
            "data": requests
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{signature_request_id}/cancel")
async def cancel_signature_request(
    signature_request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a signature request"""
    
    try:
        signature_service = SignatureService(db)
        result = await signature_service.cancel_signature_request(
            signature_request_id,
            str(current_user.id)
        )
        
        return {
            "status": "success",
            "data": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def d4sign_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle D4Sign webhook notifications"""
    
    try:
        # Parse webhook data
        webhook_data = await request.json()
        
        signature_service = SignatureService(db)
        result = await signature_service.process_webhook(webhook_data)
        
        return {
            "status": result["status"],
            "message": result.get("reason", "Webhook processed")
        }
        
    except Exception as e:
        # Log error but return success to avoid webhook retries
        print(f"D4Sign webhook processing error: {str(e)}")
        return {"status": "error", "message": "Internal error"}

# Additional utility endpoints

@router.get("/templates")
async def get_document_templates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get available document templates for signature"""
    
    # This could be expanded to include pre-made contract templates
    return {
        "status": "success",
        "templates": [
            {
                "id": "rental_contract",
                "name": "Contrato de Locação",
                "description": "Modelo padrão para contratos de locação residencial",
                "category": "real_estate"
            },
            {
                "id": "service_contract",
                "name": "Contrato de Prestação de Serviços",
                "description": "Modelo para contratos de serviços gerais",
                "category": "services"
            },
            {
                "id": "purchase_agreement",
                "name": "Contrato de Compra e Venda",
                "description": "Modelo para compra e venda de bens",
                "category": "sales"
            }
        ]
    }

@router.get("/validation/cpf/{cpf}")
async def validate_cpf(
    cpf: str,
    current_user: User = Depends(get_current_user)
):
    """Validate CPF format and checksum"""
    
    def is_valid_cpf(cpf: str) -> bool:
        """Validate CPF checksum"""
        # Remove non-numeric characters
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Check if has 11 digits
        if len(cpf) != 11:
            return False
        
        # Check if all digits are the same
        if cpf == cpf[0] * 11:
            return False
        
        # Calculate first verification digit
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Calculate second verification digit
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        # Check if calculated digits match
        return cpf[-2:] == f"{digit1}{digit2}"
    
    return {
        "cpf": cpf,
        "valid": is_valid_cpf(cpf),
        "formatted": f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf
    }