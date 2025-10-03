"""
API Endpoint para Upload e Processamento de Contratos
Integra OCR + Análise Jurídica + Sistema Híbrido LLM
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging

from ...workers.document_processor import DocumentProcessor
from ...core.config import settings

router = APIRouter(prefix="/contracts", tags=["contracts"])
logger = logging.getLogger(__name__)

@router.post("/upload", response_model=Dict[str, Any])
async def upload_and_analyze_contract(
    file: UploadFile = File(..., description="Arquivo PDF, PNG, JPG ou JPEG"),
    user_id: Optional[str] = Form(None, description="ID do usuário (opcional)")
) -> JSONResponse:
    """
    Upload e análise completa de contrato
    
    Pipeline completo:
    1. 📄 Extração de texto via OCR (Google Cloud Vision)  
    2. 🔍 Classificação automática do tipo de contrato
    3. 📊 Análise de complexidade para roteamento inteligente
    4. ⚖️ Análise jurídica especializada por agente
    5. 🎯 Identificação de riscos e cláusulas problemáticas
    
    **Formatos suportados**: PDF, PNG, JPG, JPEG
    **Tamanho máximo**: 25MB
    """
    
    # Validar tipo de arquivo
    allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.gif'}
    file_extension = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "Tipo de arquivo não suportado",
                "message": f"Use apenas: {', '.join(allowed_extensions)}",
                "received": file_extension
            }
        )
    
    # Validar tamanho (25MB max)
    max_size = 25 * 1024 * 1024  # 25MB
    if file.size and file.size > max_size:
        raise HTTPException(
            status_code=413,
            detail={
                "error": "Arquivo muito grande", 
                "message": f"Tamanho máximo: 25MB",
                "received_size": f"{file.size / 1024 / 1024:.1f}MB"
            }
        )
    
    try:
        logger.info(f"📁 Recebendo upload: {file.filename} ({file.size} bytes)")
        
        # Ler conteúdo do arquivo
        file_content = await file.read()
        
        # Processar documento com pipeline completo
        processor = DocumentProcessor()
        result = await processor.process_contract_file(
            file_content=file_content,
            filename=file.filename,
            user_id=user_id
        )
        
        if result["success"]:
            # Sucesso - retornar análise completa
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Contrato analisado com sucesso! 🎉",
                    "data": {
                        "filename": result["filename"],
                        "contract_type": result["contract_type"],
                        "analysis_summary": {
                            "risk_level": result["analysis"].get("risk_level", "medium"),
                            "key_findings": result["analysis"].get("key_findings", [])[:5],  # Top 5
                            "summary": result["analysis"].get("summary", "Análise concluída"),
                            "recommendations": result["analysis"].get("recommendations", [])[:3]  # Top 3
                        },
                        "processing_info": {
                            "ocr_method": result["ocr_result"]["method"],
                            "ocr_confidence": f"{result['ocr_result']['confidence']*100:.1f}%",
                            "pages_processed": result["ocr_result"]["pages"],
                            "complexity_level": result["complexity"]["level"],
                            "ai_model_used": result["complexity"]["model_used"].get("provider", "gemini"),
                            "processing_time": result["ocr_result"].get("processing_time", "N/A")
                        }
                    },
                    "full_analysis": result["analysis"]  # Análise completa para desenvolvedores
                }
            )
        else:
            # Erro no processamento
            error_details = {
                "status": "error",
                "message": "Erro no processamento do documento",
                "error": result.get("error", "Erro desconhecido"),
                "details": {
                    "filename": result["filename"],
                    "ocr_available": result.get("ocr_available", False),
                    "timestamp": result.get("timestamp")
                }
            }
            
            return JSONResponse(
                status_code=422,
                content=error_details
            )
            
    except Exception as e:
        logger.error(f"❌ Erro crítico no upload: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "Erro interno do servidor",
                "message": "Falha no processamento do documento",
                "details": str(e)
            }
        )

@router.get("/ocr-status", response_model=Dict[str, Any])
async def get_ocr_status() -> JSONResponse:
    """
    Verifica status do sistema OCR e dependências
    
    Retorna informações sobre:
    - Disponibilidade do Google Cloud Vision
    - Status das credenciais
    - Dependências instaladas
    """
    
    from ...services.ocr_service import ocr_service
    
    status = ocr_service.get_status()
    
    return JSONResponse({
        "ocr_system": {
            "available": status["available"],
            "status": "✅ Funcionando" if status["available"] else "❌ Não disponível"
        },
        "dependencies": {
            "google_cloud_vision": status["google_vision_installed"],
            "pymupdf": status["pymupdf_available"], 
            "pillow": status["pil_available"]
        },
        "configuration": {
            "credentials_configured": status["credentials_found"],
            "project_id": status.get("project_id", "Não configurado"),
            "service_account": status.get("service_account", "Não configurado")
        },
        "capabilities": {
            "pdf_processing": status["pymupdf_available"] and status["available"],
            "image_processing": status["pil_available"] and status["available"],
            "direct_text_extraction": status["pymupdf_available"],
            "ocr_fallback": status["available"]
        }
    })

@router.get("/supported-formats")
async def get_supported_formats() -> JSONResponse:
    """
    Lista formatos de arquivo suportados e limitações
    """
    
    return JSONResponse({
        "supported_formats": {
            "documents": ["pdf"],
            "images": ["png", "jpg", "jpeg", "gif"]
        },
        "limitations": {
            "max_file_size": "25MB",
            "max_pages": "Ilimitado (PDFs)",
            "languages": ["Português", "Inglês", "Espanhol"]
        },
        "processing_methods": {
            "pdf_native": "Extração direta de texto (mais rápida)",
            "ocr_vision": "Google Cloud Vision (PDFs escaneados/imagens)",
            "hybrid": "Combinação automática baseada no conteúdo"
        }
    })

@router.post("/test-ocr")
async def test_ocr_endpoint(
    file: UploadFile = File(..., description="Arquivo para testar OCR")
) -> JSONResponse:
    """
    Endpoint de teste para OCR - apenas extração de texto
    NÃO faz análise jurídica, apenas teste de OCR
    """
    
    from ...services.ocr_service import ocr_service
    
    try:
        file_content = await file.read()
        
        # Apenas OCR, sem análise
        result = await ocr_service.extract_text_from_file(file_content, file.filename)
        
        return JSONResponse({
            "status": "success",
            "filename": file.filename,
            "ocr_result": {
                "text_preview": result["text"][:500] + "..." if len(result["text"]) > 500 else result["text"],
                "full_text_length": len(result["text"]),
                "method": result["method"],
                "confidence": f"{result['confidence']*100:.1f}%",
                "pages": result.get("pages", 1),
                "processing_time": result.get("processing_time", "N/A")
            }
        })
        
    except Exception as e:
        logger.error(f"Erro no teste OCR: {e}")
        raise HTTPException(status_code=500, detail=str(e))