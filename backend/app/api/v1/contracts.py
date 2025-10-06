from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import json

from app.db.database import get_db
from app.db.models import Contract, User, RiskFactor
from app.api.v1.auth import get_current_user
from app.agents.factory import AgentFactory
from app.core.config import settings
from app.legal.privacy_service import ProcessingPurpose
from app.services.contract_analysis_service import contract_analysis_service
from app.services.llm_router import LLMProvider
from app.services.storage_service import get_r2_service
from app.services.async_processor import AsyncContractProcessor

router = APIRouter()

# Initialize processor
async_processor = AsyncContractProcessor()

# Helper function to get initialized AgentFactory
def get_agent_factory(db: AsyncSession = None):
    """Get initialized AgentFactory with LLM client and RAG service"""
    from app.services.rag_service import get_rag_service
    from app.services.llm_client import UnifiedLLMService
    
    # Get RAG service
    rag_service = get_rag_service()
    
    # Initialize LLM service and get Claude client
    llm_service = UnifiedLLMService()
    claude_client = None
    
    # Try to get an available Claude client
    for client_name, client in llm_service.clients.items():
        if 'anthropic' in client_name.lower() or 'claude' in client_name.lower():
            claude_client = client
            break
    
    # If no Claude client, use first available
    if not claude_client and llm_service.clients:
        claude_client = list(llm_service.clients.values())[0]
    
    return AgentFactory(
        claude_client=claude_client,
        rag_service=rag_service,
        db_session=db
    )

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

# Novos modelos para fundação ética
class ConsentRequest(BaseModel):
    purposes: List[str]  # Lista de ProcessingPurpose
    user_agent: Optional[str] = ""

class ConsentResponse(BaseModel):
    consent_id: str
    status: str
    message: str
    purposes: List[str]
    timestamp: str

class EthicalAnalysisRequest(BaseModel):
    contract_text: str
    user_type: str = "CPF"  # "CPF" ou "CNPJ"
    anonymize: Optional[bool] = False
    explicit_consent: Optional[bool] = False

class EthicalAnalysisResponse(BaseModel):
    # Análise principal
    analysis: dict
    response_text: str
    
    # Informações de entidade
    entity_analysis: dict
    
    # Auditoria de viés
    bias_audit: dict
    
    # Conformidade
    compliance_status: str
    processing_record_id: str
    user_type: str
    terms_version: str
    privacy_compliant: bool
    timestamp: str
    
    # Campos opcionais para consentimento
    requires_consent: Optional[bool] = False
    consent_text: Optional[str] = None
    pre_analysis_warning: Optional[str] = None

class UserDataExportResponse(BaseModel):
    user_id: str
    export_date: str
    consent_records: List[dict]
    processing_records: List[dict]
    total_records: int

class DataDeletionResponse(BaseModel):
    user_id: str
    deleted_records: int
    anonymized_records: int
    consent_records_removed: int
    processed_at: str

class ComplianceReportResponse(BaseModel):
    terms_of_service: dict
    privacy_compliance: dict
    bias_audit: dict
    supported_agents: List[str]
    factory_version: str
    generated_at: str

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
    background_tasks: BackgroundTasks = None,
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
        
        # Upload file to Cloudflare R2
        r2_service = get_r2_service()
        if r2_service:
            try:
                file_content = await file.read()
                file_key = f"contracts/{current_user.id}/{contract.id}/{file.filename}"
                
                file_url = await r2_service.upload_file(
                    file_content=file_content,
                    file_key=file_key,
                    content_type=file.content_type
                )
                
                # Update contract with storage info
                contract.storage_path = file_key
                contract.storage_url = file_url
                await db.commit()
                
            except Exception as upload_error:
                # Log but don't fail - file can be reprocessed
                print(f"R2 upload error: {upload_error}")
        
        # Queue document processing task asynchronously
        try:
            job_id = await async_processor.create_job(
                contract_id=str(contract.id),
                user_id=str(current_user.id),
                file_path=contract.storage_path or file.filename,
                metadata={
                    'title': title,
                    'filename': file.filename,
                    'mime_type': file.content_type
                }
            )
            
            # Start processing in background
            await async_processor.start_processing(job_id)
            
        except Exception as processing_error:
            print(f"Processing queue error: {processing_error}")
            # Update status to failed
            contract.processing_status = "failed"
            await db.commit()
        
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
    
    # Queue reanalysis task
    try:
        job_id = await async_processor.create_job(
            contract_id=contract_id,
            user_id=str(current_user.id),
            file_path=contract.storage_path or contract.original_filename,
            metadata={
                'title': contract.title,
                'reanalysis': True
            }
        )
        
        # Start reprocessing
        await async_processor.start_processing(job_id)
        
        return {
            "message": "Contract queued for reanalysis",
            "job_id": job_id
        }
        
    except Exception as e:
        contract.processing_status = "failed"
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to queue reanalysis: {str(e)}"
        )

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
    
    # Delete file from Cloudflare R2 if stored
    if contract.storage_path:
        r2_service = get_r2_service()
        if r2_service:
            try:
                await r2_service.delete_file(contract.storage_path)
            except Exception as delete_error:
                # Log but don't fail the deletion
                print(f"R2 deletion error: {delete_error}")
    
    await db.delete(contract)
    await db.commit()
    
    return {"message": "Contract deleted successfully"}

# RAG Service Endpoints

class RAGSearchRequest(BaseModel):
    query: str
    contract_category: Optional[str] = None
    document_types: Optional[List[str]] = None
    authority_level: Optional[str] = None
    limit: int = 10
    similarity_threshold: float = 0.75

class RAGSearchResponse(BaseModel):
    legal_chunks: List[dict]
    knowledge_base: List[dict]
    query_metadata: dict

@router.post("/rag/search", response_model=RAGSearchResponse)
async def search_legal_knowledge(
    request: RAGSearchRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search legal knowledge base using RAG"""
    
    try:
        from app.services.rag_service import get_rag_service
        
        results = await get_rag_service().search_legal_knowledge(
            query=request.query,
            contract_category=request.contract_category,
            document_types=request.document_types,
            authority_level=request.authority_level,
            limit=request.limit,
            similarity_threshold=request.similarity_threshold,
            db=db
        )
        
        return RAGSearchResponse(**results)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching legal knowledge: {str(e)}"
        )

class EnhancedAnalysisRequest(BaseModel):
    contract_text: str
    contract_category: Optional[str] = None
    analysis_type: str = "analysis"

@router.post("/{contract_id}/enhanced-analysis")
async def get_enhanced_contract_analysis(
    contract_id: str,
    request: EnhancedAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get enhanced contract analysis using RAG Service"""
    
    # Verify contract ownership
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
    
    try:
        # Create agent factory with database session
        agent_factory = get_agent_factory(db)
        
        # Get enhanced analysis using RAG
        enhanced_analysis = await agent_factory.analyze_contract(
            contract_text=request.contract_text or contract.extracted_text,
            context={"contract_id": contract_id, "enhanced_rag": True}
        )
        
        # Update contract with enhanced analysis
        if enhanced_analysis["status"] == "success":
            contract.analysis_results = enhanced_analysis["analysis"]
            contract.risk_level = enhanced_analysis["analysis"]["risk_level"]
            contract.analysis_summary = enhanced_analysis["analysis"]["summary"]
            contract.confidence_score = enhanced_analysis["analysis"]["confidence_score"]
            contract.analyzed_at = datetime.utcnow()
            
            await db.commit()
        
        return {
            "contract_id": contract_id,
            "enhanced_analysis": enhanced_analysis,
            "rag_enhanced": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in enhanced analysis: {str(e)}"
        )

class LegalPrecedentsRequest(BaseModel):
    contract_clause: str
    contract_type: str

@router.post("/legal-precedents")
async def get_legal_precedents(
    request: LegalPrecedentsRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get legal precedents for specific contract clauses"""
    
    try:
        from app.services.rag_service import get_rag_service
        
        precedents = await get_rag_service().get_legal_precedents(
            contract_clause=request.contract_clause,
            contract_type=request.contract_type,
            limit=5,
            db=db
        )
        
        return {
            "contract_clause": request.contract_clause,
            "contract_type": request.contract_type,
            "precedents": precedents,
            "total_found": len(precedents)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving legal precedents: {str(e)}"
        )

@router.get("/rag/stats")
async def get_rag_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get RAG knowledge base statistics"""
    
    try:
        from app.services.rag_service import get_rag_service
        
        stats = await get_rag_service().get_knowledge_stats(db)
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving RAG statistics: {str(e)}"
        )

# ===============================
# ETHICAL FOUNDATION ENDPOINTS
# ===============================

@router.post("/ethical/consent", response_model=ConsentResponse)
async def record_user_consent(
    request: ConsentRequest,
    http_request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Registra consentimento do usuário para tratamento de dados (LGPD)"""
    
    try:
        from app.agents.factory import AgentFactory
        from app.services.rag_service import get_rag_service
        
        # Converte strings para enums
        purposes = [ProcessingPurpose(purpose) for purpose in request.purposes]
        
        # Obtém informações da requisição
        ip_address = http_request.client.host if http_request.client else ""
        user_agent = http_request.headers.get("user-agent", "")
        
        # Cria factory e registra consentimento
        factory = get_agent_factory(db)
        result = factory.record_user_consent(
            user_id=str(current_user.id),
            purposes=purposes,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Erro ao registrar consentimento")
            )
        
        return ConsentResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Finalidade inválida: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar consentimento: {str(e)}"
        )

@router.post("/ethical/analyze", response_model=EthicalAnalysisResponse)
async def analyze_contract_ethically(
    request: EthicalAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Análise de contrato com conformidade ética completa
    
    Implementa:
    - Verificação automática de consentimento LGPD
    - Análise inteligente com detecção de entidades
    - Auditoria de viés em tempo real
    - Aplicação de disclaimers legais apropriados
    """
    
    try:
        # Inicializa factory com dependências completas
        factory = get_agent_factory(db)
        
        # Executa análise ética completa
        result = await factory.analyze_contract_ethically(
            contract_text=request.contract_text,
            user_id=str(current_user.id),
            user_type_str=request.user_type,
            context={
                "anonymize": request.anonymize,
                "explicit_consent": request.explicit_consent
            }
        )
        
        # Se requer consentimento, retorna informações de consentimento
        if result.get("requires_consent"):
            return EthicalAnalysisResponse(
                analysis={},
                response_text="",
                entity_analysis={},
                bias_audit={},
                compliance_status="awaiting_consent",
                processing_record_id="",
                user_type=request.user_type,
                terms_version=result.get("terms_version", "1.0.0"),
                privacy_compliant=True,
                timestamp=result.get("timestamp", ""),
                requires_consent=True,
                consent_text=result.get("consent_text"),
                pre_analysis_warning=result.get("pre_analysis_warning")
            )
        
        # Se houve erro
        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Erro durante análise ética")
            )
        
        # Extrai dados da análise ética
        ethical_analysis = result.get("ethical_analysis", {})
        
        return EthicalAnalysisResponse(
            analysis=ethical_analysis.get("analysis", result.get("analysis", {})),
            response_text=ethical_analysis.get("response_text", result.get("response", "")),
            entity_analysis=ethical_analysis.get("entity_analysis", result.get("entity_analysis", {})),
            bias_audit=ethical_analysis.get("bias_audit", {}),
            compliance_status=result.get("compliance_status", "approved"),
            processing_record_id=ethical_analysis.get("processing_record_id", ""),
            user_type=result.get("user_type", request.user_type),
            terms_version=result.get("terms_version", "1.0.0"),
            privacy_compliant=result.get("privacy_compliant", True),
            timestamp=result.get("timestamp", "")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro durante análise ética: {str(e)}"
        )

@router.get("/ethical/user-data", response_model=UserDataExportResponse)
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Exporta dados do usuário (direito de portabilidade - LGPD Art. 18, V)"""
    
    try:
        factory = get_agent_factory(db)
        data = factory.get_user_data_summary(str(current_user.id))
        
        if data.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=data.get("message", "Erro ao exportar dados")
            )
        
        return UserDataExportResponse(**data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao exportar dados: {str(e)}"
        )

@router.delete("/ethical/user-data", response_model=DataDeletionResponse)
async def delete_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Deleta dados do usuário (direito de eliminação - LGPD Art. 18, VI)"""
    
    try:
        factory = get_agent_factory(db)
        result = factory.delete_user_data(str(current_user.id))
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Erro ao deletar dados")
            )
        
        return DataDeletionResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar dados: {str(e)}"
        )

@router.get("/ethical/compliance-report", response_model=ComplianceReportResponse)
async def get_compliance_report(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Gera relatório de conformidade ética e legal (apenas para administradores)"""
    
    # Verifica se usuário é administrador (implementar lógica de autorização)
    # if not current_user.is_admin:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Acesso negado. Apenas administradores podem acessar relatórios de conformidade."
    #     )
    
    try:
        factory = get_agent_factory(db)
        report = factory.get_compliance_report()
        
        return ComplianceReportResponse(**report)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar relatório: {str(e)}"
        )

@router.get("/ethical/required-consent/{user_type}")
async def get_required_consent_text(
    user_type: str,
    current_user: User = Depends(get_current_user)
):
    """Obtém texto de consentimento necessário para tipo de usuário específico"""
    
    if user_type not in ["CPF", "CNPJ"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de usuário deve ser 'CPF' ou 'CNPJ'"
        )
    
    try:
        from app.legal.terms_of_service import terms_service, ServiceType, UserType
        
        user_type_enum = UserType.INDIVIDUAL_CPF if user_type == "CPF" else UserType.SMALL_BUSINESS_CNPJ
        
        requires_consent = terms_service.should_require_explicit_consent(
            ServiceType.CONTRACT_ANALYSIS, 
            user_type_enum
        )
        
        if requires_consent:
            consent_text = terms_service.get_consent_text(ServiceType.CONTRACT_ANALYSIS)
            pre_warning = terms_service.get_pre_analysis_warning(user_type_enum)
            
            return {
                "requires_consent": True,
                "consent_text": consent_text,
                "pre_analysis_warning": pre_warning,
                "user_type": user_type,
                "purposes_required": [
                    ProcessingPurpose.CONTRACT_ANALYSIS.value,
                    ProcessingPurpose.SERVICE_PROVISION.value
                ]
            }
        else:
            return {
                "requires_consent": False,
                "message": "Consentimento não obrigatório para este tipo de usuário e serviço",
                "user_type": user_type
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter informações de consentimento: {str(e)}"
        )

# Novos endpoints com roteamento inteligente de LLM

@router.post("/analyze-smart")
async def analyze_contract_smart(
    contract_text: str = Form(...),
    contract_metadata: Optional[str] = Form(None),
    analysis_depth: str = Form("standard"),
    force_model: Optional[str] = Form(None),
    include_rag: bool = Form(True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Análise inteligente de contrato com roteamento automático de LLM
    
    - **contract_text**: Texto completo do contrato
    - **contract_metadata**: Metadados em JSON (valor, tipo, duração, etc.)
    - **analysis_depth**: quick, standard, detailed, comprehensive  
    - **force_model**: gemini_flash, gemini_pro, anthropic_haiku, anthropic_sonnet, anthropic_opus
    - **include_rag**: Incluir consulta à base de conhecimento jurídico
    """
    
    try:
        # Parse dos metadados se fornecidos
        metadata = {}
        if contract_metadata:
            try:
                metadata = json.loads(contract_metadata)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400, 
                    detail="Metadados devem estar em formato JSON válido"
                )
        
        # Validação do modelo forçado
        force_provider = None
        if force_model:
            try:
                force_provider = LLMProvider(force_model)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Modelo '{force_model}' não suportado. Use: gemini_flash, gemini_pro, anthropic_haiku, anthropic_sonnet, anthropic_opus"
                )
        
        # Validação da profundidade de análise
        valid_depths = ["quick", "standard", "detailed", "comprehensive"]
        if analysis_depth not in valid_depths:
            raise HTTPException(
                status_code=400,
                detail=f"Profundidade '{analysis_depth}' inválida. Use: {', '.join(valid_depths)}"
            )
        
        # Adicionar informações do usuário aos metadados
        metadata.update({
            'user_id': str(current_user.id),
            'analysis_requested_at': datetime.now().isoformat()
        })
        
        # Executar análise
        analysis_result = await contract_analysis_service.analyze_contract(
            contract_text=contract_text,
            contract_metadata=metadata,
            analysis_depth=analysis_depth,
            force_model=force_provider,
            include_rag=include_rag
        )
        
        # Converter dataclass para dict
        result_dict = {
            'contract_id': analysis_result.contract_id,
            'analysis_summary': analysis_result.analysis_summary,
            'risk_assessment': analysis_result.risk_assessment,
            'legal_insights': analysis_result.legal_insights,
            'recommendations': analysis_result.recommendations,
            'cost_breakdown': analysis_result.cost_breakdown,
            'processing_metadata': analysis_result.processing_metadata,
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'data': result_dict,
            'message': 'Análise de contrato realizada com sucesso'
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na análise do contrato: {str(e)}"
        )

@router.post("/upload-analyze-smart")
async def upload_and_analyze_contract_smart(
    file: UploadFile = File(...),
    contract_metadata: Optional[str] = Form(None),
    analysis_depth: str = Form("standard"),
    force_model: Optional[str] = Form(None),
    include_rag: bool = Form(True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload de arquivo PDF/DOC e análise automática com roteamento inteligente
    
    - **file**: Arquivo do contrato (PDF, DOC, DOCX, TXT)
    - **contract_metadata**: Metadados em JSON (valor, tipo, duração, etc.)
    - **analysis_depth**: quick, standard, detailed, comprehensive
    - **force_model**: gemini_flash, gemini_pro, anthropic_haiku, anthropic_sonnet, anthropic_opus  
    - **include_rag**: Incluir consulta à base de conhecimento jurídico
    """
    
    try:
        # Validar tipo de arquivo
        allowed_types = ['application/pdf', 'text/plain', 'application/msword', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Tipo de arquivo não suportado. Use PDF, DOC, DOCX ou TXT"
            )
        
        # Ler conteúdo do arquivo
        file_content = await file.read()
        
        # Extrair texto baseado no tipo de arquivo
        if file.content_type == 'text/plain':
            contract_text = file_content.decode('utf-8')
        elif file.content_type == 'application/pdf':
            # Usar OCR service para extração de PDF
            from app.services.ocr_service import OCRService
            ocr_service = OCRService()
            
            if not ocr_service.available:
                raise HTTPException(
                    status_code=501,
                    detail="Serviço de OCR não configurado. Configure Google Cloud Vision para processar PDFs."
                )
            
            ocr_result = await ocr_service.extract_text_from_pdf(file_content)
            if ocr_result.get('error'):
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao extrair texto do PDF: {ocr_result['error']}"
                )
            contract_text = ocr_result.get('text', '')
        else:
            # Suporte para outros formatos via OCR
            from app.services.ocr_service import OCRService
            ocr_service = OCRService()
            
            if not ocr_service.available:
                raise HTTPException(
                    status_code=501,
                    detail="Tipo de arquivo não suportado sem OCR configurado. Use texto plano ou configure Google Cloud Vision."
                )
            
            ocr_result = await ocr_service.extract_text_from_file(file_content, file.filename)
            if ocr_result.get('error'):
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao extrair texto: {ocr_result['error']}"
                )
            contract_text = ocr_result.get('text', '')
        
        # Parse dos metadados
        metadata = {}
        if contract_metadata:
            try:
                metadata = json.loads(contract_metadata)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Metadados devem estar em formato JSON válido"
                )
        
        # Adicionar informações do arquivo e usuário aos metadados
        metadata.update({
            'filename': file.filename,
            'file_size': len(file_content),
            'content_type': file.content_type,
            'upload_timestamp': datetime.now().isoformat(),
            'user_id': str(current_user.id)
        })
        
        # Executar análise
        analysis_result = await contract_analysis_service.analyze_contract(
            contract_text=contract_text,
            contract_metadata=metadata,
            analysis_depth=analysis_depth,
            force_model=LLMProvider(force_model) if force_model else None,
            include_rag=include_rag
        )
        
        # Converter resultado para dict
        result_dict = {
            'contract_id': analysis_result.contract_id,
            'analysis_summary': analysis_result.analysis_summary,
            'risk_assessment': analysis_result.risk_assessment,
            'legal_insights': analysis_result.legal_insights,
            'recommendations': analysis_result.recommendations,
            'cost_breakdown': analysis_result.cost_breakdown,
            'processing_metadata': analysis_result.processing_metadata,
            'file_info': {
                'filename': file.filename,
                'size': len(file_content),
                'type': file.content_type
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'data': result_dict,
            'message': 'Upload e análise realizados com sucesso'
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no upload e análise: {str(e)}"
        )

@router.get("/routing-stats")
async def get_routing_statistics(
    current_user: User = Depends(get_current_user)
):
    """
    Estatísticas do roteamento inteligente de LLMs
    
    Retorna métricas de uso, custos e eficiência do sistema de roteamento
    """
    
    try:
        # Obter estatísticas do roteador
        routing_stats = contract_analysis_service.llm_router.get_usage_statistics()
        
        # Obter estatísticas dos clientes LLM
        client_stats = contract_analysis_service.llm_service.get_all_stats()
        
        # Obter provedores disponíveis
        available_providers = contract_analysis_service.llm_service.get_available_providers()
        
        return {
            'success': True,
            'data': {
                'routing_statistics': routing_stats,
                'client_statistics': client_stats,
                'available_providers': [p.value for p in available_providers],
                'system_info': {
                    'total_models_configured': len(contract_analysis_service.llm_router.llm_configs),
                    'models_available': len(available_providers),
                    'rag_enabled': True,
                    'last_updated': datetime.now().isoformat()
                }
            },
            'message': 'Estatísticas obtidas com sucesso'
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas: {str(e)}"
        )

@router.post("/complexity-preview")
async def analyze_contract_complexity_preview(
    contract_text: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """
    Análise prévia de complexidade do contrato (sem usar LLM)
    
    Retorna apenas a análise de complexidade para preview do roteamento
    """
    
    try:
        # Usar apenas o analisador de complexidade
        complexity_analysis = contract_analysis_service.llm_router.complexity_analyzer.analyze_complexity(
            contract_text
        )
        
        # Simular roteamento para mostrar qual modelo seria usado
        routing_preview = await contract_analysis_service.llm_router.route_contract_analysis(
            contract_text=contract_text,
            analysis_type="standard"
        )
        
        return {
            'success': True,
            'data': {
                'complexity_analysis': {
                    'complexity_level': complexity_analysis['complexity_level'].value,
                    'total_score': complexity_analysis['total_score'],
                    'breakdown': complexity_analysis['breakdown'],
                    'reasoning': complexity_analysis['reasoning'],
                    'document_stats': complexity_analysis['document_stats']
                },
                'routing_preview': {
                    'recommended_model': routing_preview['selected_model'].value,
                    'estimated_cost': routing_preview['cost_analysis']['estimated_cost_usd'],
                    'cost_vs_premium': routing_preview['cost_analysis']['cost_vs_opus'],
                    'savings_percentage': routing_preview['cost_analysis']['savings_percentage']
                }
            },
            'message': 'Análise de complexidade realizada'
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na análise de complexidade: {str(e)}"
        )


# ========================================
# 🚀 NOVOS ENDPOINTS COM OCR
# ========================================

@router.post("/upload-with-ocr", response_model=Dict[str, Any])
async def upload_and_analyze_contract_ocr(
    file: UploadFile = File(..., description="Arquivo PDF, PNG, JPG ou JPEG"),
    user_id: Optional[str] = Form(None, description="ID do usuário (opcional)"),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    🔥 **NOVO**: Upload com OCR + Análise Jurídica Completa
    
    Pipeline inteligente:
    1. 📄 OCR via Google Cloud Vision  
    2. 🔍 Classificação automática
    3. 📊 Roteamento por complexidade  
    4. ⚖️ Análise jurídica especializada
    5. 🎯 Detecção de riscos e cláusulas
    
    **Melhorias**: Suporte a PDFs escaneados, imagens, análise híbrida
    """
    
    from ...workers.document_processor import DocumentProcessor
    
    # Validar tipo de arquivo
    allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.gif'}
    file_extension = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "Tipo de arquivo não suportado",
                "supported": list(allowed_extensions),
                "received": file_extension
            }
        )
    
    # Validar tamanho (25MB)
    if file.size and file.size > 25 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Arquivo muito grande. Máximo: 25MB"
        )
    
    try:
        # Processar arquivo
        file_content = await file.read()
        processor = DocumentProcessor()
        
        result = await processor.process_contract_file(
            file_content=file_content,
            filename=file.filename,
            user_id=str(current_user.id)
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": "📄 Contrato analisado com OCR! 🎉",
                "data": {
                    "filename": result["filename"],
                    "contract_type": result["contract_type"], 
                    "risk_level": result["analysis"].get("risk_level", "medium"),
                    "key_findings": result["analysis"].get("key_findings", [])[:5],
                    "summary": result["analysis"].get("summary", "Análise concluída"),
                    "ocr_info": {
                        "method": result["ocr_result"]["method"],
                        "confidence": f"{result['ocr_result']['confidence']*100:.1f}%",
                        "pages": result["ocr_result"]["pages"]
                    },
                    "ai_routing": {
                        "complexity": result["complexity"]["level"],
                        "model_used": result["complexity"]["model_used"]
                    }
                },
                "full_analysis": result["analysis"]
            }
        else:
            raise HTTPException(
                status_code=422,
                detail=result.get("error", "Erro no processamento")
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ocr-status")
async def check_ocr_status() -> Dict[str, Any]:
    """
    🔍 Verificar status do sistema OCR
    """
    from ...services.ocr_service import ocr_service
    
    status = ocr_service.get_status()
    
    return {
        "ocr_available": status["available"],
        "google_vision": status["google_vision_installed"],
        "credentials_ok": status["credentials_found"],
        "project_id": status.get("project_id"),
        "capabilities": {
            "pdf_native": status["pymupdf_available"],
            "image_ocr": status["available"],
            "hybrid_mode": status["available"] and status["pymupdf_available"]
        },
        "status_message": "✅ OCR funcionando" if status["available"] else "❌ OCR não disponível"
    }


@router.post("/test-ocr")
async def test_ocr_only(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    🧪 Testar apenas OCR (sem análise jurídica)
    """
    from ...services.ocr_service import ocr_service
    
    try:
        file_content = await file.read()
        result = await ocr_service.extract_text_from_file(file_content, file.filename)
        
        return {
            "filename": file.filename,
            "text_length": len(result["text"]),
            "text_preview": result["text"][:300] + "..." if len(result["text"]) > 300 else result["text"],
            "method": result["method"],
            "confidence": f"{result['confidence']*100:.1f}%",
            "pages": result.get("pages", 1)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
