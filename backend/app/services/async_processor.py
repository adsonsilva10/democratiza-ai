"""
Sistema de processamento assíncrono de contratos
Gerencia jobs de análise com tracking completo e notificações em tempo real
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from fastapi import WebSocket
import logging
from app.services.email_service import EmailService
from app.agents.factory import AgentFactory
from app.services.image_processor import DocumentImageProcessor
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class JobType(str, Enum):
    CONTRACT_ANALYSIS = "contract_analysis"
    IMAGE_PROCESSING = "image_processing"
    DOCUMENT_OCR = "document_ocr"
    FULL_PIPELINE = "full_pipeline"

@dataclass
class JobProgress:
    stage: str
    progress: float  # 0.0 to 1.0
    message: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

@dataclass
class ContractJob:
    id: str
    user_id: str
    job_type: JobType
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    
    # Input data
    files: List[str]  # File paths or URLs
    contract_title: str
    user_email: str
    
    # Processing data
    progress_history: List[JobProgress]
    current_stage: str
    total_stages: int
    estimated_completion: Optional[datetime]
    
    # Results
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    # Configuration
    options: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        if self.estimated_completion:
            data['estimated_completion'] = self.estimated_completion.isoformat()
        
        # Convert progress history
        data['progress_history'] = [
            {
                **asdict(p),
                'timestamp': p.timestamp.isoformat()
            }
            for p in self.progress_history
        ]
        
        return data

class AsyncContractProcessor:
    """Processador assíncrono de contratos com tracking completo"""
    
    def __init__(self):
        self.jobs: Dict[str, ContractJob] = {}
        self.active_jobs: Dict[str, asyncio.Task] = {}
        self.websocket_connections: Dict[str, List[WebSocket]] = {}
        
        # Services
        self.agent_factory = AgentFactory()
        self.image_processor = DocumentImageProcessor()
        self.email_service = EmailService()
        self.rag_service = RAGService()
        
        # Configuration
        self.max_concurrent_jobs = 5
        self.job_timeout_minutes = 30
        
    async def create_job(
        self,
        user_id: str,
        user_email: str,
        job_type: JobType,
        files: List[str],
        contract_title: str,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """Cria um novo job de processamento"""
        
        job_id = str(uuid.uuid4())
        
        # Definir stages baseado no tipo de job
        stages = self._get_job_stages(job_type)
        
        job = ContractJob(
            id=job_id,
            user_id=user_id,
            job_type=job_type,
            status=JobStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            files=files,
            contract_title=contract_title,
            user_email=user_email,
            progress_history=[],
            current_stage="initialization",
            total_stages=len(stages),
            estimated_completion=None,
            options=options or {}
        )
        
        self.jobs[job_id] = job
        
        # Iniciar processamento assíncrono
        task = asyncio.create_task(self._process_job(job_id))
        self.active_jobs[job_id] = task
        
        logger.info(f"Job {job_id} criado para usuário {user_id}")
        
        return job_id
    
    def _get_job_stages(self, job_type: JobType) -> List[str]:
        """Define as etapas de processamento baseado no tipo de job"""
        
        if job_type == JobType.FULL_PIPELINE:
            return [
                "initialization",
                "file_validation", 
                "image_processing",
                "ocr_extraction",
                "contract_classification",
                "agent_analysis",
                "result_compilation",
                "notification"
            ]
        elif job_type == JobType.CONTRACT_ANALYSIS:
            return [
                "initialization",
                "file_validation",
                "ocr_extraction", 
                "contract_classification",
                "agent_analysis",
                "result_compilation",
                "notification"
            ]
        elif job_type == JobType.IMAGE_PROCESSING:
            return [
                "initialization",
                "image_validation",
                "image_enhancement",
                "result_compilation"
            ]
        else:
            return ["initialization", "processing", "completion"]
    
    async def _process_job(self, job_id: str) -> None:
        """Processa um job de forma assíncrona"""
        
        job = self.jobs[job_id]
        
        try:
            await self._update_job_status(job_id, JobStatus.PROCESSING)
            
            if job.job_type == JobType.FULL_PIPELINE:
                await self._process_full_pipeline(job_id)
            elif job.job_type == JobType.CONTRACT_ANALYSIS:
                await self._process_contract_analysis(job_id)
            elif job.job_type == JobType.IMAGE_PROCESSING:
                await self._process_image_enhancement(job_id)
            
            await self._update_job_status(job_id, JobStatus.COMPLETED)
            
        except Exception as e:
            logger.error(f"Erro no processamento do job {job_id}: {str(e)}")
            await self._update_job_status(job_id, JobStatus.FAILED, str(e))
        
        finally:
            # Cleanup
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
    
    async def _process_full_pipeline(self, job_id: str) -> None:
        """Pipeline completo: imagem → OCR → análise → resultado"""
        
        job = self.jobs[job_id]
        
        # 1. Validação de arquivos
        await self._update_progress(
            job_id, "file_validation", 0.1,
            f"Validando {len(job.files)} arquivo(s)..."
        )
        
        validated_files = await self._validate_files(job.files)
        
        # 2. Processamento de imagens (se houver)
        image_files = [f for f in validated_files if self._is_image_file(f)]
        
        if image_files:
            await self._update_progress(
                job_id, "image_processing", 0.2,
                f"Otimizando {len(image_files)} imagem(ns) para OCR..."
            )
            
            enhanced_images = []
            for i, image_file in enumerate(image_files):
                result = await self._process_single_image(image_file)
                enhanced_images.append(result)
                
                progress = 0.2 + (0.2 * (i + 1) / len(image_files))
                await self._update_progress(
                    job_id, "image_processing", progress,
                    f"Processada imagem {i + 1}/{len(image_files)}"
                )
        
        # 3. OCR Extraction
        await self._update_progress(
            job_id, "ocr_extraction", 0.4,
            "Extraindo texto dos documentos..."
        )
        
        extracted_text = await self._extract_text_from_files(validated_files)
        
        # 4. Classificação do contrato
        await self._update_progress(
            job_id, "contract_classification", 0.6,
            "Classificando tipo de contrato..."
        )
        
        contract_type = await self._classify_contract(extracted_text)
        
        # 5. Análise por agente especializado
        await self._update_progress(
            job_id, "agent_analysis", 0.7,
            f"Analisando contrato com agente {contract_type}..."
        )
        
        analysis_result = await self._analyze_with_agent(contract_type, extracted_text)
        
        # 6. Compilação final
        await self._update_progress(
            job_id, "result_compilation", 0.9,
            "Compilando resultado final..."
        )
        
        final_result = await self._compile_final_result(
            job_id, extracted_text, contract_type, analysis_result
        )
        
        # 7. Notificação
        await self._update_progress(
            job_id, "notification", 0.95,
            "Enviando notificações..."
        )
        
        await self._send_completion_notification(job_id, final_result)
        
        # Salvar resultado
        job.result = final_result
        job.updated_at = datetime.utcnow()
    
    async def _process_contract_analysis(self, job_id: str) -> None:
        """Pipeline de análise sem processamento de imagem"""
        
        job = self.jobs[job_id]
        
        # Similar ao pipeline completo, mas sem image_processing
        await self._update_progress(
            job_id, "file_validation", 0.2,
            "Validando arquivos..."
        )
        
        validated_files = await self._validate_files(job.files)
        
        await self._update_progress(
            job_id, "ocr_extraction", 0.4,
            "Extraindo texto..."
        )
        
        extracted_text = await self._extract_text_from_files(validated_files)
        
        await self._update_progress(
            job_id, "contract_classification", 0.6,
            "Classificando contrato..."
        )
        
        contract_type = await self._classify_contract(extracted_text)
        
        await self._update_progress(
            job_id, "agent_analysis", 0.8,
            "Executando análise..."
        )
        
        analysis_result = await self._analyze_with_agent(contract_type, extracted_text)
        
        final_result = await self._compile_final_result(
            job_id, extracted_text, contract_type, analysis_result
        )
        
        await self._send_completion_notification(job_id, final_result)
        
        job.result = final_result
        job.updated_at = datetime.utcnow()
    
    async def _process_image_enhancement(self, job_id: str) -> None:
        """Pipeline apenas para processamento de imagens"""
        
        job = self.jobs[job_id]
        
        await self._update_progress(
            job_id, "image_validation", 0.2,
            "Validando imagens..."
        )
        
        image_files = [f for f in job.files if self._is_image_file(f)]
        
        await self._update_progress(
            job_id, "image_enhancement", 0.4,
            f"Processando {len(image_files)} imagens..."
        )
        
        results = []
        for i, image_file in enumerate(image_files):
            result = await self._process_single_image(image_file)
            results.append(result)
            
            progress = 0.4 + (0.5 * (i + 1) / len(image_files))
            await self._update_progress(
                job_id, "image_enhancement", progress,
                f"Processada {i + 1}/{len(image_files)}"
            )
        
        job.result = {
            'processed_images': results,
            'total_processed': len(results)
        }
        job.updated_at = datetime.utcnow()
    
    # Métodos auxiliares
    async def _validate_files(self, files: List[str]) -> List[str]:
        """Valida se os arquivos existem e são válidos"""
        # Implementar validação de arquivos
        await asyncio.sleep(0.5)  # Simular processamento
        return files
    
    def _is_image_file(self, file_path: str) -> bool:
        """Verifica se é um arquivo de imagem"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        return any(file_path.lower().endswith(ext) for ext in image_extensions)
    
    async def _process_single_image(self, image_path: str) -> Dict[str, Any]:
        """Processa uma única imagem"""
        # Implementar processamento real
        await asyncio.sleep(2)  # Simular processamento
        return {
            'original_path': image_path,
            'enhanced_path': f"{image_path}_enhanced",
            'confidence_score': 0.85,
            'applied_filters': ['perspective_correction', 'contrast_enhancement']
        }
    
    async def _extract_text_from_files(self, files: List[str]) -> str:
        """Extrai texto dos arquivos usando OCR"""
        # Implementar OCR real
        await asyncio.sleep(3)
        return "Texto extraído do contrato..."
    
    async def _classify_contract(self, text: str) -> str:
        """Classifica o tipo de contrato"""
        # Usar classifier agent
        await asyncio.sleep(1)
        return "rental"  # Exemplo
    
    async def _analyze_with_agent(self, contract_type: str, text: str) -> Dict[str, Any]:
        """Analisa contrato com agente especializado"""
        # Usar agent factory
        await asyncio.sleep(5)
        return {
            'risk_level': 'medium',
            'clauses': [],
            'summary': 'Análise completa do contrato'
        }
    
    async def _compile_final_result(
        self, 
        job_id: str, 
        text: str, 
        contract_type: str, 
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compila resultado final"""
        
        return {
            'job_id': job_id,
            'contract_type': contract_type,
            'extracted_text': text[:1000] + "..." if len(text) > 1000 else text,
            'analysis': analysis,
            'processed_at': datetime.utcnow().isoformat(),
            'processing_time_seconds': self._calculate_processing_time(job_id)
        }
    
    def _calculate_processing_time(self, job_id: str) -> float:
        """Calcula tempo total de processamento"""
        job = self.jobs[job_id]
        delta = datetime.utcnow() - job.created_at
        return delta.total_seconds()
    
    async def _send_completion_notification(
        self, 
        job_id: str, 
        result: Dict[str, Any]
    ) -> None:
        """Envia notificação de conclusão"""
        
        job = self.jobs[job_id]
        
        # Enviar email
        try:
            await self.email_service.send_analysis_complete_email(
                to_email=job.user_email,
                contract_title=job.contract_title,
                job_id=job_id,
                result_summary=result['analysis']['summary']
            )
        except Exception as e:
            logger.error(f"Erro ao enviar email para job {job_id}: {str(e)}")
        
        # Notificar via WebSocket
        await self._broadcast_to_user(job.user_id, {
            'type': 'job_completed',
            'job_id': job_id,
            'result': result
        })
    
    # WebSocket methods
    async def connect_websocket(self, user_id: str, websocket: WebSocket):
        """Conecta WebSocket do usuário"""
        await websocket.accept()
        
        if user_id not in self.websocket_connections:
            self.websocket_connections[user_id] = []
        
        self.websocket_connections[user_id].append(websocket)
        
        # Enviar jobs em andamento
        user_jobs = [job for job in self.jobs.values() if job.user_id == user_id]
        for job in user_jobs:
            await websocket.send_json({
                'type': 'job_status',
                'job': job.to_dict()
            })
    
    async def disconnect_websocket(self, user_id: str, websocket: WebSocket):
        """Desconecta WebSocket do usuário"""
        if user_id in self.websocket_connections:
            try:
                self.websocket_connections[user_id].remove(websocket)
                if not self.websocket_connections[user_id]:
                    del self.websocket_connections[user_id]
            except ValueError:
                pass
    
    async def _broadcast_to_user(self, user_id: str, message: Dict[str, Any]):
        """Envia mensagem para todos os WebSockets do usuário"""
        if user_id not in self.websocket_connections:
            return
        
        disconnected = []
        for websocket in self.websocket_connections[user_id]:
            try:
                await websocket.send_json(message)
            except:
                disconnected.append(websocket)
        
        # Remove conexões inválidas
        for ws in disconnected:
            try:
                self.websocket_connections[user_id].remove(ws)
            except ValueError:
                pass
    
    async def _update_job_status(
        self, 
        job_id: str, 
        status: JobStatus, 
        error_message: Optional[str] = None
    ):
        """Atualiza status do job"""
        
        job = self.jobs[job_id]
        job.status = status
        job.updated_at = datetime.utcnow()
        
        if error_message:
            job.error_message = error_message
        
        # Notificar via WebSocket
        await self._broadcast_to_user(job.user_id, {
            'type': 'job_status_changed',
            'job_id': job_id,
            'status': status.value,
            'error': error_message
        })
    
    async def _update_progress(
        self, 
        job_id: str, 
        stage: str, 
        progress: float,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Atualiza progresso do job"""
        
        job = self.jobs[job_id]
        
        progress_entry = JobProgress(
            stage=stage,
            progress=progress,
            message=message,
            timestamp=datetime.utcnow(),
            details=details
        )
        
        job.progress_history.append(progress_entry)
        job.current_stage = stage
        job.updated_at = datetime.utcnow()
        
        # Calcular estimativa de conclusão
        if progress > 0:
            elapsed = datetime.utcnow() - job.created_at
            estimated_total = elapsed / progress
            job.estimated_completion = job.created_at + estimated_total
        
        # Notificar via WebSocket
        await self._broadcast_to_user(job.user_id, {
            'type': 'job_progress',
            'job_id': job_id,
            'stage': stage,
            'progress': progress,
            'message': message,
            'estimated_completion': job.estimated_completion.isoformat() if job.estimated_completion else None
        })
    
    # Public methods para API
    def get_job(self, job_id: str) -> Optional[ContractJob]:
        """Retorna job por ID"""
        return self.jobs.get(job_id)
    
    def get_user_jobs(self, user_id: str) -> List[ContractJob]:
        """Retorna todos os jobs do usuário"""
        return [job for job in self.jobs.values() if job.user_id == user_id]
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancela job em andamento"""
        if job_id in self.active_jobs:
            task = self.active_jobs[job_id]
            task.cancel()
            await self._update_job_status(job_id, JobStatus.CANCELLED)
            return True
        return False
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema"""
        return {
            'total_jobs': len(self.jobs),
            'active_jobs': len(self.active_jobs),
            'connected_users': len(self.websocket_connections),
            'jobs_by_status': {
                status.value: sum(1 for job in self.jobs.values() if job.status == status)
                for status in JobStatus
            }
        }


# Singleton instance
async_processor = AsyncContractProcessor()