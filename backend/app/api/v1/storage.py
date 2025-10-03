"""
API endpoints para gerenciamento de arquivos no Cloudflare R2
Fornece upload, download, listagem e exclusão segura de documentos.
"""

from typing import List, Optional
from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    UploadFile, 
    File,
    Request,
    Response
)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.services.storage_service import r2_service, FileMetadata

router = APIRouter()


@router.post("/upload", response_model=FileMetadata)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload de documento para análise
    
    - **file**: Arquivo PDF, imagem ou texto
    - **Retorna**: Metadados do arquivo armazenado
    """
    # Obter informações do cliente para auditoria
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent")
    
    try:
        # Validar se arquivo foi enviado
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Nenhum arquivo foi enviado"
            )
        
        # Upload para R2
        file_metadata = await r2_service.upload_file(
            file=file,
            user=current_user,
            metadata={
                "upload_source": "api",
                "endpoint": "/storage/upload"
            },
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        return file_metadata
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno durante upload: {str(e)}"
        )


@router.get("/download/{file_id}")
async def download_document(
    file_id: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download de documento
    
    - **file_id**: ID único do arquivo
    - **Retorna**: Arquivo como stream
    """
    # Obter informações do cliente para auditoria
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent")
    
    try:
        # Download do R2
        file_content, file_metadata = await r2_service.download_file(
            file_id=file_id,
            user=current_user,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        # Criar stream de resposta
        file_stream = io.BytesIO(file_content)
        
        # Determinar filename para download
        filename = file_metadata.original_name or f"document_{file_id}"
        
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type=file_metadata.mime_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(file_metadata.file_size)
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno durante download: {str(e)}"
        )


@router.get("/download-url/{file_id}")
async def get_download_url(
    file_id: str,
    request: Request,
    expiration_hours: int = 1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obter URL presignada para download direto
    
    - **file_id**: ID único do arquivo
    - **expiration_hours**: Horas para expiração da URL (padrão: 1)
    - **Retorna**: URL presignada válida por tempo limitado
    """
    try:
        # Validar parâmetros
        if expiration_hours < 1 or expiration_hours > 24:
            raise HTTPException(
                status_code=400,
                detail="Tempo de expiração deve ser entre 1 e 24 horas"
            )
        
        # Gerar URL presignada
        presigned_url = await r2_service.generate_presigned_download_url(
            file_id=file_id,
            user=current_user,
            expiration_hours=expiration_hours
        )
        
        return {
            "download_url": presigned_url,
            "expires_in_hours": expiration_hours,
            "file_id": file_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar URL presignada: {str(e)}"
        )


@router.delete("/{file_id}")
async def delete_document(
    file_id: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Excluir documento
    
    - **file_id**: ID único do arquivo
    - **Retorna**: Confirmação de exclusão
    """
    # Obter informações do cliente para auditoria
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent")
    
    try:
        # Deletar do R2
        success = await r2_service.delete_file(
            file_id=file_id,
            user=current_user,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        if success:
            return {
                "message": "Arquivo excluído com sucesso",
                "file_id": file_id
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Falha ao excluir o arquivo"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno durante exclusão: {str(e)}"
        )


@router.get("/list", response_model=List[FileMetadata])
async def list_user_documents(
    request: Request,
    prefix: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar documentos do usuário
    
    - **prefix**: Filtro por prefixo no nome
    - **limit**: Limite de resultados (padrão: 50, máximo: 100)
    - **Retorna**: Lista de metadados dos arquivos
    """
    try:
        # Validar limite
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail="Limite deve ser entre 1 e 100"
            )
        
        # Listar arquivos do usuário
        files = await r2_service.list_user_files(
            user=current_user,
            prefix=prefix,
            limit=limit
        )
        
        return files
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar arquivos: {str(e)}"
        )


@router.get("/metadata/{file_id}", response_model=FileMetadata)
async def get_file_metadata(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obter metadados de um arquivo específico
    
    - **file_id**: ID único do arquivo
    - **Retorna**: Metadados completos do arquivo
    """
    try:
        # Fazer "download" apenas dos metadados (sem o conteúdo)
        _, file_metadata = await r2_service.download_file(
            file_id=file_id,
            user=current_user
        )
        
        return file_metadata
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter metadados: {str(e)}"
        )


@router.get("/health")
async def storage_health():
    """
    Verificar saúde do serviço de storage
    
    - **Retorna**: Status da conexão com R2
    """
    try:
        # Testar conexão listando objetos no bucket (limite 1 para ser rápido)
        r2_service.s3_client.list_objects_v2(
            Bucket=r2_service.bucket_name,
            MaxKeys=1
        )
        
        return {
            "status": "healthy",
            "service": "Cloudflare R2",
            "bucket": r2_service.bucket_name
        }
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Cloudflare R2", 
            "error": str(e)
        }