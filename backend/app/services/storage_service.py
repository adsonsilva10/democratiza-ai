"""
Cloudflare R2 Storage Service para o Democratiza AI
Fornece armazenamento seguro e criptografado para documentos de contratos.

Funcionalidades:
- Upload de arquivos com criptografia
- Download com validação de acesso
- Exclusão segura de arquivos
- Auditoria completa de operações
- Controle de acesso por usuário
- Geração de URLs presignadas
"""

import os
import uuid
import hashlib
import mimetypes
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple
from io import BytesIO

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from botocore.config import Config
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel

from app.core.config import settings
from app.db.models import User


class FileMetadata(BaseModel):
    """Metadados de um arquivo armazenado"""
    file_id: str
    original_name: str
    file_size: int
    mime_type: str
    upload_date: datetime
    user_id: int
    file_hash: str
    encryption_key: Optional[str] = None


class StorageAuditLog(BaseModel):
    """Log de auditoria para operações de storage"""
    operation: str  # upload, download, delete, access
    file_id: str
    user_id: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None


class CloudflareR2Service:
    """
    Serviço de armazenamento usando Cloudflare R2
    Compatível com S3 API, mas com custos menores e performance global
    """
    
    def __init__(self):
        """Inicializa o cliente R2 com configurações seguras"""
        self._validate_configuration()
        
        # Configuração do cliente S3 compatível para R2
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT,
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
            config=Config(
                region_name='auto',  # R2 usa 'auto' como região
                retries={'max_attempts': 3},
                max_pool_connections=50
            )
        )
        
        self.bucket_name = settings.CLOUDFLARE_R2_BUCKET
        self._ensure_bucket_exists()
    
    def _validate_configuration(self) -> None:
        """Valida se todas as credenciais R2 estão configuradas"""
        required_settings = [
            'CLOUDFLARE_R2_ACCESS_KEY',
            'CLOUDFLARE_R2_SECRET_KEY', 
            'CLOUDFLARE_R2_BUCKET',
            'CLOUDFLARE_R2_ENDPOINT'
        ]
        
        missing = []
        for setting in required_settings:
            if not getattr(settings, setting):
                missing.append(setting)
        
        if missing:
            raise ValueError(f"Credenciais R2 faltando: {', '.join(missing)}")
    
    def _ensure_bucket_exists(self) -> None:
        """Verifica se o bucket existe, cria se necessário"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                # Bucket não existe, criar
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                except ClientError as create_error:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Não foi possível criar bucket R2: {str(create_error)}"
                    )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao acessar bucket R2: {str(e)}"
                )
    
    def _generate_file_id(self) -> str:
        """Gera ID único para o arquivo"""
        return str(uuid.uuid4())
    
    def _generate_s3_key(self, user_id: int, file_id: str, original_name: str) -> str:
        """Gera chave S3 organizada por usuário e com timestamp"""
        timestamp = datetime.utcnow().strftime("%Y/%m/%d")
        file_extension = os.path.splitext(original_name)[1]
        return f"users/{user_id}/{timestamp}/{file_id}{file_extension}"
    
    def _calculate_file_hash(self, file_content: bytes) -> str:
        """Calcula hash SHA-256 do arquivo para verificação de integridade"""
        return hashlib.sha256(file_content).hexdigest()
    
    def _validate_file_type(self, filename: str) -> str:
        """Valida tipo de arquivo e retorna MIME type"""
        file_extension = os.path.splitext(filename)[1].lower().lstrip('.')
        
        if file_extension not in settings.allowed_file_types_list:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de arquivo não permitido: {file_extension}. "
                       f"Tipos permitidos: {', '.join(settings.allowed_file_types_list)}"
            )
        
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type or "application/octet-stream"
    
    async def upload_file(
        self,
        file: UploadFile,
        user: User,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> FileMetadata:
        """
        Upload seguro de arquivo para R2
        
        Args:
            file: Arquivo para upload
            user: Usuário que está fazendo o upload
            metadata: Metadados adicionais
            ip_address: IP do cliente (para auditoria)
            user_agent: User Agent (para auditoria)
        
        Returns:
            FileMetadata: Informações do arquivo armazenado
        """
        file_id = self._generate_file_id()
        
        try:
            # Ler conteúdo do arquivo
            file_content = await file.read()
            file_size = len(file_content)
            
            # Validar tamanho
            if file_size > settings.max_file_size_bytes:
                raise HTTPException(
                    status_code=413,
                    detail=f"Arquivo muito grande. Máximo: {settings.MAX_FILE_SIZE_MB}MB"
                )
            
            # Validar tipo
            mime_type = self._validate_file_type(file.filename)
            
            # Calcular hash para integridade
            file_hash = self._calculate_file_hash(file_content)
            
            # Gerar chave S3
            s3_key = self._generate_s3_key(user.id, file_id, file.filename)
            
            # Preparar metadados
            s3_metadata = {
                'user-id': str(user.id),
                'original-name': file.filename,
                'file-hash': file_hash,
                'upload-date': datetime.utcnow().isoformat(),
                'mime-type': mime_type
            }
            
            if metadata:
                # Adicionar metadados customizados (prefixados para evitar conflitos)
                for key, value in metadata.items():
                    s3_metadata[f'custom-{key}'] = str(value)
            
            # Upload para R2
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=mime_type,
                Metadata=s3_metadata,
                ServerSideEncryption='AES256'  # Criptografia no servidor
            )
            
            # Criar metadados de resposta
            file_metadata = FileMetadata(
                file_id=file_id,
                original_name=file.filename,
                file_size=file_size,
                mime_type=mime_type,
                upload_date=datetime.utcnow(),
                user_id=user.id,
                file_hash=file_hash
            )
            
            # Log de auditoria
            await self._log_operation(
                operation="upload",
                file_id=file_id,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=True
            )
            
            return file_metadata
        
        except HTTPException:
            raise
        except Exception as e:
            # Log de erro
            await self._log_operation(
                operation="upload",
                file_id=file_id,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                error_message=str(e)
            )
            raise HTTPException(
                status_code=500,
                detail=f"Erro durante upload: {str(e)}"
            )
    
    async def download_file(
        self,
        file_id: str,
        user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[bytes, FileMetadata]:
        """
        Download seguro de arquivo do R2
        
        Args:
            file_id: ID do arquivo
            user: Usuário solicitando o download
            ip_address: IP do cliente
            user_agent: User Agent
        
        Returns:
            Tuple[bytes, FileMetadata]: Conteúdo do arquivo e metadados
        """
        try:
            # Buscar arquivo no bucket (lista para encontrar a chave)
            s3_key = await self._find_file_key(file_id, user.id)
            
            if not s3_key:
                raise HTTPException(
                    status_code=404,
                    detail="Arquivo não encontrado ou sem permissão de acesso"
                )
            
            # Download do arquivo
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            file_content = response['Body'].read()
            metadata_dict = response.get('Metadata', {})
            
            # Reconstruir metadados
            file_metadata = FileMetadata(
                file_id=file_id,
                original_name=metadata_dict.get('original-name', 'unknown'),
                file_size=len(file_content),
                mime_type=metadata_dict.get('mime-type', 'application/octet-stream'),
                upload_date=datetime.fromisoformat(
                    metadata_dict.get('upload-date', datetime.utcnow().isoformat())
                ),
                user_id=int(metadata_dict.get('user-id', user.id)),
                file_hash=metadata_dict.get('file-hash', '')
            )
            
            # Verificar integridade
            calculated_hash = self._calculate_file_hash(file_content)
            if file_metadata.file_hash and calculated_hash != file_metadata.file_hash:
                raise HTTPException(
                    status_code=500,
                    detail="Erro de integridade: arquivo pode estar corrompido"
                )
            
            # Log de auditoria
            await self._log_operation(
                operation="download",
                file_id=file_id,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=True
            )
            
            return file_content, file_metadata
        
        except HTTPException:
            raise
        except Exception as e:
            # Log de erro
            await self._log_operation(
                operation="download",
                file_id=file_id,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                error_message=str(e)
            )
            raise HTTPException(
                status_code=500,
                detail=f"Erro durante download: {str(e)}"
            )
    
    async def delete_file(
        self,
        file_id: str,
        user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> bool:
        """
        Exclusão segura de arquivo
        
        Args:
            file_id: ID do arquivo
            user: Usuário solicitando a exclusão
            ip_address: IP do cliente
            user_agent: User Agent
        
        Returns:
            bool: True se excluído com sucesso
        """
        try:
            # Buscar arquivo
            s3_key = await self._find_file_key(file_id, user.id)
            
            if not s3_key:
                raise HTTPException(
                    status_code=404,
                    detail="Arquivo não encontrado ou sem permissão de acesso"
                )
            
            # Deletar do R2
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            # Log de auditoria
            await self._log_operation(
                operation="delete",
                file_id=file_id,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=True
            )
            
            return True
        
        except HTTPException:
            raise
        except Exception as e:
            # Log de erro
            await self._log_operation(
                operation="delete",
                file_id=file_id,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                error_message=str(e)
            )
            raise HTTPException(
                status_code=500,
                detail=f"Erro durante exclusão: {str(e)}"
            )
    
    async def generate_presigned_download_url(
        self,
        file_id: str,
        user: User,
        expiration_hours: int = 1
    ) -> str:
        """
        Gera URL presignada para download direto (sem passar pelo servidor)
        
        Args:
            file_id: ID do arquivo
            user: Usuário solicitando a URL
            expiration_hours: Horas para expiração da URL
        
        Returns:
            str: URL presignada
        """
        try:
            s3_key = await self._find_file_key(file_id, user.id)
            
            if not s3_key:
                raise HTTPException(
                    status_code=404,
                    detail="Arquivo não encontrado ou sem permissão de acesso"
                )
            
            # Gerar URL presignada
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration_hours * 3600
            )
            
            # Log de auditoria
            await self._log_operation(
                operation="presigned_url",
                file_id=file_id,
                user_id=user.id,
                success=True
            )
            
            return presigned_url
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao gerar URL presignada: {str(e)}"
            )
    
    async def list_user_files(
        self,
        user: User,
        prefix: Optional[str] = None,
        limit: int = 100
    ) -> List[FileMetadata]:
        """
        Lista arquivos do usuário
        
        Args:
            user: Usuário
            prefix: Filtro por prefixo
            limit: Limite de resultados
        
        Returns:
            List[FileMetadata]: Lista de metadados dos arquivos
        """
        try:
            user_prefix = f"users/{user.id}/"
            if prefix:
                user_prefix += prefix
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=user_prefix,
                MaxKeys=limit
            )
            
            files = []
            for obj in response.get('Contents', []):
                # Obter metadados do objeto
                head_response = self.s3_client.head_object(
                    Bucket=self.bucket_name,
                    Key=obj['Key']
                )
                
                metadata = head_response.get('Metadata', {})
                
                # Extrair file_id da chave
                file_id = os.path.basename(obj['Key']).split('.')[0]
                
                file_metadata = FileMetadata(
                    file_id=file_id,
                    original_name=metadata.get('original-name', 'unknown'),
                    file_size=obj['Size'],
                    mime_type=metadata.get('mime-type', 'application/octet-stream'),
                    upload_date=obj['LastModified'],
                    user_id=user.id,
                    file_hash=metadata.get('file-hash', '')
                )
                
                files.append(file_metadata)
            
            return files
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao listar arquivos: {str(e)}"
            )
    
    async def _find_file_key(self, file_id: str, user_id: int) -> Optional[str]:
        """
        Encontra a chave S3 de um arquivo pelo ID e valida acesso do usuário
        
        Args:
            file_id: ID do arquivo
            user_id: ID do usuário
        
        Returns:
            Optional[str]: Chave S3 se encontrada e autorizada
        """
        try:
            user_prefix = f"users/{user_id}/"
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=user_prefix
            )
            
            for obj in response.get('Contents', []):
                key = obj['Key']
                # Extrair file_id do nome do arquivo na chave
                filename_with_id = os.path.basename(key)
                extracted_file_id = filename_with_id.split('.')[0]
                
                if extracted_file_id == file_id:
                    return key
            
            return None
        
        except Exception:
            return None
    
    async def _log_operation(
        self,
        operation: str,
        file_id: str,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """
        Log de auditoria para operações de storage
        """
        try:
            # Import here to avoid circular imports
            from app.db.database import AsyncSessionLocal
            from app.db.models import StorageAuditLog as StorageAuditLogModel
            
            # Save to database
            async with AsyncSessionLocal() as db:
                audit_log = StorageAuditLogModel(
                    user_id=user_id,
                    operation=operation,
                    file_id=file_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    success=success,
                    error_message=error_message,
                    operation_metadata={}
                )
                db.add(audit_log)
                await db.commit()
                
        except Exception as e:
            # Fallback to console logging if database fails
            if settings.DEBUG:
                print(f"[STORAGE AUDIT ERROR] Failed to log to DB: {e}")
                print(f"[STORAGE AUDIT] {operation} | {file_id} | {user_id} | {success}")


# Instância global do serviço
r2_service = CloudflareR2Service()