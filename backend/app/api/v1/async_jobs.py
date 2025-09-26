"""
WebSocket endpoints para comunicação em tempo real
Permite tracking de jobs e notificações instantâneas
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.services.async_processor import async_processor, JobType, JobStatus
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class JobCreateRequest(BaseModel):
    job_type: JobType
    files: List[str]
    contract_title: str
    user_email: str
    options: Optional[Dict[str, Any]] = None

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: str
    current_stage: str
    progress: Optional[float] = None
    message: Optional[str] = None
    estimated_completion: Optional[str] = None
    error_message: Optional[str] = None

# Job Management Endpoints

@router.post("/jobs", response_model=Dict[str, str])
async def create_job(
    request: JobCreateRequest,
    user_id: str = "demo_user"  # Em produção, extrair do token JWT
):
    """
    Cria um novo job de processamento assíncrono
    """
    try:
        job_id = await async_processor.create_job(
            user_id=user_id,
            user_email=request.user_email,
            job_type=request.job_type,
            files=request.files,
            contract_title=request.contract_title,
            options=request.options
        )
        
        return {
            "job_id": job_id,
            "message": "Job criado com sucesso",
            "status": "pending"
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar job: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar job: {str(e)}")

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_status(
    job_id: str,
    user_id: str = "demo_user"
):
    """
    Retorna status detalhado de um job
    """
    job = async_processor.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    
    if job.user_id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado ao job")
    
    # Pegar progresso mais recente
    latest_progress = job.progress_history[-1] if job.progress_history else None
    
    return JobResponse(
        job_id=job.id,
        status=job.status,
        created_at=job.created_at.isoformat(),
        current_stage=job.current_stage,
        progress=latest_progress.progress if latest_progress else None,
        message=latest_progress.message if latest_progress else None,
        estimated_completion=job.estimated_completion.isoformat() if job.estimated_completion else None,
        error_message=job.error_message
    )

@router.get("/jobs", response_model=List[JobResponse])
async def get_user_jobs(
    user_id: str = "demo_user",
    status: Optional[JobStatus] = None,
    limit: int = 50
):
    """
    Lista jobs do usuário com filtros opcionais
    """
    jobs = async_processor.get_user_jobs(user_id)
    
    # Filtrar por status se especificado
    if status:
        jobs = [job for job in jobs if job.status == status]
    
    # Limitar resultados
    jobs = jobs[-limit:]
    
    # Converter para response format
    responses = []
    for job in jobs:
        latest_progress = job.progress_history[-1] if job.progress_history else None
        
        responses.append(JobResponse(
            job_id=job.id,
            status=job.status,
            created_at=job.created_at.isoformat(),
            current_stage=job.current_stage,
            progress=latest_progress.progress if latest_progress else None,
            message=latest_progress.message if latest_progress else None,
            estimated_completion=job.estimated_completion.isoformat() if job.estimated_completion else None,
            error_message=job.error_message
        ))
    
    return responses

@router.delete("/jobs/{job_id}")
async def cancel_job(
    job_id: str,
    user_id: str = "demo_user"
):
    """
    Cancela um job em andamento
    """
    job = async_processor.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    
    if job.user_id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado ao job")
    
    if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
        raise HTTPException(status_code=400, detail="Job não pode ser cancelado")
    
    success = await async_processor.cancel_job(job_id)
    
    if success:
        return {"message": "Job cancelado com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao cancelar job")

@router.get("/jobs/{job_id}/result")
async def get_job_result(
    job_id: str,
    user_id: str = "demo_user"
):
    """
    Retorna resultado de um job concluído
    """
    job = async_processor.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    
    if job.user_id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado ao job")
    
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400, 
            detail=f"Job ainda não concluído. Status atual: {job.status.value}"
        )
    
    return {
        "job_id": job_id,
        "result": job.result,
        "completed_at": job.updated_at.isoformat()
    }

@router.get("/jobs/{job_id}/progress")
async def get_job_progress_history(
    job_id: str,
    user_id: str = "demo_user"
):
    """
    Retorna histórico completo de progresso do job
    """
    job = async_processor.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    
    if job.user_id != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado ao job")
    
    progress_history = [
        {
            "stage": p.stage,
            "progress": p.progress,
            "message": p.message,
            "timestamp": p.timestamp.isoformat(),
            "details": p.details
        }
        for p in job.progress_history
    ]
    
    return {
        "job_id": job_id,
        "total_stages": job.total_stages,
        "current_stage": job.current_stage,
        "progress_history": progress_history
    }

# WebSocket Endpoint

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket para comunicação em tempo real com o usuário
    Envia atualizações de progresso e notificações
    """
    try:
        await async_processor.connect_websocket(user_id, websocket)
        logger.info(f"WebSocket conectado para usuário {user_id}")
        
        # Enviar mensagem de boas-vindas
        await websocket.send_json({
            "type": "connection_established",
            "user_id": user_id,
            "message": "Conectado ao sistema de tracking"
        })
        
        # Loop para manter conexão viva e processar mensagens
        while True:
            try:
                # Receber mensagens do cliente (heartbeat, comandos, etc.)
                data = await websocket.receive_json()
                
                # Processar diferentes tipos de mensagem
                if data.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": "2025-09-26T10:00:00Z"
                    })
                
                elif data.get("type") == "get_active_jobs":
                    # Enviar lista de jobs ativos
                    user_jobs = async_processor.get_user_jobs(user_id)
                    active_jobs = [
                        job.to_dict() for job in user_jobs 
                        if job.status in [JobStatus.PENDING, JobStatus.PROCESSING]
                    ]
                    
                    await websocket.send_json({
                        "type": "active_jobs",
                        "jobs": active_jobs
                    })
                
                elif data.get("type") == "subscribe_job":
                    # Cliente quer receber atualizações específicas de um job
                    job_id = data.get("job_id")
                    job = async_processor.get_job(job_id)
                    
                    if job and job.user_id == user_id:
                        await websocket.send_json({
                            "type": "job_subscribed",
                            "job_id": job_id,
                            "job": job.to_dict()
                        })
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Job não encontrado ou acesso negado"
                        })
                
            except Exception as e:
                logger.error(f"Erro processando mensagem WebSocket: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "message": "Erro interno do servidor"
                })
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket desconectado para usuário {user_id}")
    
    except Exception as e:
        logger.error(f"Erro no WebSocket para usuário {user_id}: {str(e)}")
    
    finally:
        await async_processor.disconnect_websocket(user_id, websocket)

# System Stats (Admin)

@router.get("/system/stats")
async def get_system_stats():
    """
    Retorna estatísticas do sistema de processamento
    """
    return async_processor.get_system_stats()

# Helper endpoints para desenvolvimento

@router.post("/demo/create-full-pipeline-job")
async def create_demo_full_pipeline_job():
    """
    Cria um job de demonstração com pipeline completo
    """
    job_id = await async_processor.create_job(
        user_id="demo_user",
        user_email="demo@democratiza.ai",
        job_type=JobType.FULL_PIPELINE,
        files=[
            "/demo/contract1.pdf",
            "/demo/page1.jpg", 
            "/demo/page2.jpg"
        ],
        contract_title="Contrato de Locação - Demo",
        options={
            "auto_enhance_images": True,
            "preserve_colors": False,
            "priority": "normal"
        }
    )
    
    return {
        "job_id": job_id,
        "message": "Job de demonstração criado",
        "websocket_url": f"/api/v1/async/ws/demo_user"
    }

@router.post("/demo/create-image-processing-job")
async def create_demo_image_job():
    """
    Cria um job de demonstração apenas para processamento de imagens
    """
    job_id = await async_processor.create_job(
        user_id="demo_user",
        user_email="demo@democratiza.ai",
        job_type=JobType.IMAGE_PROCESSING,
        files=[
            "/demo/document_photo1.jpg",
            "/demo/document_photo2.jpg",
            "/demo/document_photo3.jpg"
        ],
        contract_title="Otimização de Imagens - Demo",
        options={
            "output_format": "PNG",
            "quality": "high"
        }
    )
    
    return {
        "job_id": job_id,
        "message": "Job de processamento de imagens criado",
        "websocket_url": f"/api/v1/async/ws/demo_user"
    }