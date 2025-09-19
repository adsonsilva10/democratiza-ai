from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

from app.db.database import get_db
from app.db.models import Contract, User, RiskFactor
from app.api.v1.auth import get_current_user
from app.agents.factory import AgentFactory
from app.core.config import settings

router = APIRouter()

# Pydantic models
class ContractCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ContractResponse(BaseModel):
    id: str
    title: str
    contract_type: Optional[str]
    risk_level: Optional[str]
    analysis_summary: Optional[str]
    confidence_score: Optional[float]
    processing_status: str
    created_at: datetime
    analyzed_at: Optional[datetime]

class ContractAnalysisResponse(BaseModel):
    contract_id: str
    contract_type: str
    risk_level: str
    summary: str
    key_findings: List[str]
    risk_factors: List[dict]
    recommendations: List[str]
    confidence_score: float

class RiskFactorResponse(BaseModel):
    id: str
    risk_type: str
    description: str
    severity: str
    clause_text: Optional[str]
    recommendation: Optional[str]
    legal_basis: Optional[str]

# File upload validation
def validate_file(file: UploadFile) -> bool:
    """Validate uploaded file"""
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        return False
    if file.size and file.size > settings.MAX_FILE_SIZE:
        return False
    return True

@router.post("/upload", response_model=ContractResponse)
async def upload_contract(
    file: UploadFile = File(...),
    title: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload contract file for analysis"""
    
    # Validate file
    if not validate_file(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type or size"
        )
    
    try:
        # Create contract record
        contract = Contract(
            owner_id=current_user.id,
            title=title,
            original_filename=file.filename,
            file_size=file.size,
            mime_type=file.content_type,
            processing_status="pending"
        )
        
        db.add(contract)
        await db.commit()
        await db.refresh(contract)
        
        # TODO: Implement file upload to Cloudflare R2
        # TODO: Queue document processing task
        
        return ContractResponse(
            id=str(contract.id),
            title=contract.title,
            contract_type=contract.contract_type,
            risk_level=contract.risk_level,
            analysis_summary=contract.analysis_summary,
            confidence_score=contract.confidence_score,
            processing_status=contract.processing_status,
            created_at=contract.created_at,
            analyzed_at=contract.analyzed_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload contract"
        )

@router.get("/", response_model=List[ContractResponse])
async def list_contracts(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's contracts"""
    
    result = await db.execute(
        select(Contract)
        .where(Contract.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(Contract.created_at.desc())
    )
    contracts = result.scalars().all()
    
    return [
        ContractResponse(
            id=str(contract.id),
            title=contract.title,
            contract_type=contract.contract_type,
            risk_level=contract.risk_level,
            analysis_summary=contract.analysis_summary,
            confidence_score=contract.confidence_score,
            processing_status=contract.processing_status,
            created_at=contract.created_at,
            analyzed_at=contract.analyzed_at
        )
        for contract in contracts
    ]

@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific contract"""
    
    result = await db.execute(
        select(Contract)
        .where(Contract.id == contract_id, Contract.owner_id == current_user.id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    
    return ContractResponse(
        id=str(contract.id),
        title=contract.title,
        contract_type=contract.contract_type,
        risk_level=contract.risk_level,
        analysis_summary=contract.analysis_summary,
        confidence_score=contract.confidence_score,
        processing_status=contract.processing_status,
        created_at=contract.created_at,
        analyzed_at=contract.analyzed_at
    )

@router.get("/{contract_id}/analysis", response_model=ContractAnalysisResponse)
async def get_contract_analysis(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed contract analysis"""
    
    result = await db.execute(
        select(Contract)
        .where(Contract.id == contract_id, Contract.owner_id == current_user.id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    
    if contract.processing_status != "completed" or not contract.analysis_results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract analysis not completed"
        )
    
    analysis = contract.analysis_results.get("analysis", {})
    
    return ContractAnalysisResponse(
        contract_id=str(contract.id),
        contract_type=contract.contract_type or "unknown",
        risk_level=contract.risk_level or "Não avaliado",
        summary=contract.analysis_summary or "",
        key_findings=analysis.get("key_findings", []),
        risk_factors=analysis.get("risk_factors", []),
        recommendations=analysis.get("recommendations", []),
        confidence_score=contract.confidence_score or 0.0
    )

@router.get("/{contract_id}/risks", response_model=List[RiskFactorResponse])
async def get_contract_risks(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get contract risk factors"""
    
    # Verify contract ownership
    contract_result = await db.execute(
        select(Contract)
        .where(Contract.id == contract_id, Contract.owner_id == current_user.id)
    )
    contract = contract_result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    
    # Get risk factors
    result = await db.execute(
        select(RiskFactor).where(RiskFactor.contract_id == contract_id)
    )
    risk_factors = result.scalars().all()
    
    return [
        RiskFactorResponse(
            id=str(risk.id),
            risk_type=risk.risk_type,
            description=risk.description,
            severity=risk.severity,
            clause_text=risk.clause_text,
            recommendation=risk.recommendation,
            legal_basis=risk.legal_basis
        )
        for risk in risk_factors
    ]

@router.post("/{contract_id}/reanalyze")
async def reanalyze_contract(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Trigger contract reanalysis"""
    
    result = await db.execute(
        select(Contract)
        .where(Contract.id == contract_id, Contract.owner_id == current_user.id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    
    if not contract.extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract text not available for analysis"
        )
    
    # Update status and queue for reanalysis
    contract.processing_status = "processing"
    await db.commit()
    
    # TODO: Queue reanalysis task
    
    return {"message": "Contract queued for reanalysis"}

@router.delete("/{contract_id}")
async def delete_contract(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete contract"""
    
    result = await db.execute(
        select(Contract)
        .where(Contract.id == contract_id, Contract.owner_id == current_user.id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    
    await db.delete(contract)
    await db.commit()
    
    # TODO: Delete file from Cloudflare R2
    
    return {"message": "Contract deleted successfully"}
