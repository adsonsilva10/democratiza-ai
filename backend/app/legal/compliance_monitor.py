"""
LGPD Automated Compliance Monitor - Democratiza AI
Sistema de monitoramento e execução automática de tarefas de conformidade
"""

import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging
from dataclasses import dataclass
import json
import os

from app.legal.privacy_service import privacy_service
from app.legal.lgpd_middleware import lgpd_middleware
from app.legal.bias_auditor import bias_auditor

@dataclass
class ComplianceTask:
    """Tarefa de conformidade agendada"""
    task_id: str
    name: str
    description: str
    frequency: str  # "daily", "weekly", "monthly"
    last_run: datetime = None
    next_run: datetime = None
    enabled: bool = True
    
class LGPDComplianceMonitor:
    """
    Monitor automático de conformidade LGPD
    
    Executa tarefas agendadas de compliance:
    1. Limpeza automática de dados expirados
    2. Verificação de consentimentos próximos ao vencimento
    3. Relatórios periódicos de conformidade
    4. Monitoramento de violações de retenção
    5. Auditoria de vieses algoritmos
    6. Backup de registros de tratamento
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.tasks = self._initialize_compliance_tasks()
        self.execution_history: List[Dict[str, Any]] = []
        self.config = self._load_config()
    
    def _initialize_compliance_tasks(self) -> List[ComplianceTask]:
        """Inicializa tarefas de conformidade"""
        tasks = []
        
        # Limpeza diária de dados expirados
        tasks.append(ComplianceTask(
            task_id="daily_data_cleanup",
            name="Limpeza de Dados Expirados",
            description="Remove ou anonimiza dados que excederam período de retenção",
            frequency="daily"
        ))
        
        # Verificação semanal de consentimentos
        tasks.append(ComplianceTask(
            task_id="weekly_consent_check",
            name="Verificação de Consentimentos",
            description="Verifica consentimentos próximos ao vencimento e notifica usuários",
            frequency="weekly"
        ))
        
        # Relatório mensal de conformidade
        tasks.append(ComplianceTask(
            task_id="monthly_compliance_report",
            name="Relatório de Conformidade",
            description="Gera relatório detalhado de conformidade LGPD",
            frequency="monthly"
        ))
        
        # Auditoria semanal de vieses
        tasks.append(ComplianceTask(
            task_id="weekly_bias_audit",
            name="Auditoria de Viés IA",
            description="Analisa tendências de viés nas análises de contratos",
            frequency="weekly"
        ))
        
        # Backup diário de registros
        tasks.append(ComplianceTask(
            task_id="daily_records_backup",
            name="Backup de Registros",
            description="Faz backup de registros de tratamento e consentimentos",
            frequency="daily"
        ))
        
        return tasks
    
    def _load_config(self) -> Dict[str, Any]:
        """Carrega configurações do monitor"""
        return {
            "max_execution_time_minutes": 30,
            "retry_failed_tasks": True,
            "max_retries": 3,
            "notification_email": "compliance@democratiza-ai.com",
            "backup_retention_days": 90,
            "critical_violation_alert": True
        }
    
    def start_monitoring(self):
        """Inicia monitoramento contínuo"""
        
        if self.is_running:
            self.logger.warning("Monitor já está em execução")
            return
        
        self.is_running = True
        self.logger.info("Iniciando monitor de conformidade LGPD")
        
        # Agenda tarefas
        self._schedule_tasks()
        
        # Loop principal de monitoramento
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
                
        except KeyboardInterrupt:
            self.logger.info("Monitor interrompido pelo usuário")
        except Exception as e:
            self.logger.error(f"Erro no monitor: {str(e)}")
        finally:
            self.is_running = False
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.is_running = False
        self.logger.info("Monitor de conformidade parado")
    
    def _schedule_tasks(self):
        """Agenda tarefas baseada na frequência"""
        
        for task in self.tasks:
            if not task.enabled:
                continue
                
            if task.frequency == "daily":
                schedule.every().day.at("02:00").do(
                    self._execute_task_safe, task
                )
            elif task.frequency == "weekly":
                schedule.every().monday.at("03:00").do(
                    self._execute_task_safe, task
                )
            elif task.frequency == "monthly":
                schedule.every().month.do(
                    self._execute_task_safe, task
                )
        
        self.logger.info(f"Agendadas {len([t for t in self.tasks if t.enabled])} tarefas de conformidade")
    
    def _execute_task_safe(self, task: ComplianceTask):
        """Executa tarefa com tratamento de erros"""
        
        start_time = datetime.now()
        execution_result = {
            "task_id": task.task_id,
            "task_name": task.name,
            "start_time": start_time.isoformat(),
            "status": "running",
            "error": None,
            "result": None
        }
        
        try:
            self.logger.info(f"Executando tarefa: {task.name}")
            
            # Executa tarefa específica
            result = asyncio.run(self._execute_task(task))
            
            execution_result["status"] = "success"
            execution_result["result"] = result
            task.last_run = start_time
            
            self.logger.info(f"Tarefa concluída: {task.name}")
            
        except Exception as e:
            execution_result["status"] = "error"
            execution_result["error"] = str(e)
            
            self.logger.error(f"Erro ao executar {task.name}: {str(e)}")
            
            # Tenta reexecução se configurado
            if self.config.get("retry_failed_tasks"):
                self._schedule_retry(task)
        
        finally:
            execution_result["end_time"] = datetime.now().isoformat()
            execution_result["duration_seconds"] = (
                datetime.now() - start_time
            ).total_seconds()
            
            self.execution_history.append(execution_result)
            
            # Mantém apenas últimas 100 execuções
            if len(self.execution_history) > 100:
                self.execution_history = self.execution_history[-100:]
    
    async def _execute_task(self, task: ComplianceTask) -> Dict[str, Any]:
        """Executa tarefa específica baseada no ID"""
        
        if task.task_id == "daily_data_cleanup":
            return await self._execute_data_cleanup()
            
        elif task.task_id == "weekly_consent_check":
            return await self._execute_consent_check()
            
        elif task.task_id == "monthly_compliance_report":
            return await self._execute_compliance_report()
            
        elif task.task_id == "weekly_bias_audit":
            return await self._execute_bias_audit()
            
        elif task.task_id == "daily_records_backup":
            return await self._execute_records_backup()
        
        else:
            raise ValueError(f"Tarefa não reconhecida: {task.task_id}")
    
    async def _execute_data_cleanup(self) -> Dict[str, Any]:
        """Executa limpeza automática de dados"""
        
        # Limpeza via middleware
        cleanup_result = await lgpd_middleware.cleanup_expired_data()
        
        # Limpeza adicional no privacy service
        privacy_cleanup = {
            "consent_cleanup": 0,
            "processing_cleanup": 0
        }
        
        # Remove consentimentos muito antigos (>2 anos)
        old_threshold = datetime.now() - timedelta(days=730)
        old_consents = [
            consent_id for consent_id, consent in privacy_service.consent_records.items()
            if consent.granted_at < old_threshold and consent.withdrawn_at
        ]
        
        for consent_id in old_consents:
            del privacy_service.consent_records[consent_id]
            privacy_cleanup["consent_cleanup"] += 1
        
        return {
            "middleware_cleanup": cleanup_result,
            "privacy_cleanup": privacy_cleanup,
            "total_cleaned": (
                cleanup_result.get("deleted_records", 0) + 
                cleanup_result.get("anonymized_records", 0) +
                privacy_cleanup["consent_cleanup"]
            )
        }
    
    async def _execute_consent_check(self) -> Dict[str, Any]:
        """Verifica consentimentos próximos ao vencimento"""
        
        # Identifica consentimentos que vencem em 30 dias
        warning_threshold = datetime.now() + timedelta(days=30)
        
        expiring_consents = []
        for consent_id, consent in privacy_service.consent_records.items():
            # Assume que consentimento vale por 1 ano
            expiry_date = consent.granted_at + timedelta(days=365)
            
            if expiry_date <= warning_threshold and consent.is_active():
                expiring_consents.append({
                    "consent_id": consent_id,
                    "user_id": consent.user_id,
                    "granted_at": consent.granted_at.isoformat(),
                    "expires_at": expiry_date.isoformat(),
                    "purposes": [p.value for p in consent.purposes]
                })
        
        # Em produção, enviaria notificações aos usuários
        self.logger.info(f"Encontrados {len(expiring_consents)} consentimentos próximos ao vencimento")
        
        return {
            "checked_consents": len(privacy_service.consent_records),
            "expiring_consents": len(expiring_consents),
            "expiring_details": expiring_consents,
            "notification_sent": False  # Implementar envio real
        }
    
    async def _execute_compliance_report(self) -> Dict[str, Any]:
        """Gera relatório mensal de conformidade"""
        
        # Relatório de privacidade
        privacy_report = privacy_service.generate_compliance_report()
        
        # Relatório de middleware
        middleware_report = lgpd_middleware.get_compliance_dashboard()
        
        # Relatório de viés
        bias_report = bias_auditor.get_bias_statistics(days=30)
        
        # Relatório consolidado
        consolidated_report = {
            "report_period": "monthly",
            "generated_at": datetime.now().isoformat(),
            "privacy_compliance": privacy_report,
            "middleware_compliance": middleware_report,
            "bias_analysis": bias_report,
            "overall_score": self._calculate_consolidated_score(
                privacy_report, middleware_report, bias_report
            ),
            "key_metrics": {
                "total_data_processing_records": len(privacy_service.processing_records),
                "active_consents": sum(1 for c in privacy_service.consent_records.values() if c.is_active()),
                "compliance_violations": len(lgpd_middleware.compliance_violations),
                "bias_detections": sum(1 for audit in bias_auditor.audit_history if audit.detected_biases)
            }
        }
        
        # Salva relatório
        await self._save_compliance_report(consolidated_report)
        
        return {
            "report_generated": True,
            "report_size_kb": len(json.dumps(consolidated_report)) / 1024,
            "key_metrics": consolidated_report["key_metrics"],
            "overall_score": consolidated_report["overall_score"]
        }
    
    async def _execute_bias_audit(self) -> Dict[str, Any]:
        """Executa auditoria semanal de vieses"""
        
        # Gera estatísticas de viés
        bias_stats = bias_auditor.get_bias_statistics(days=7)
        
        # Analisa tendências
        recent_audits = [
            audit for audit in bias_auditor.audit_history
            if (datetime.now() - audit.timestamp).days <= 7
        ]
        
        trends = {
            "total_audits": len(recent_audits),
            "biased_responses": sum(1 for audit in recent_audits if audit.detected_biases),
            "human_review_required": sum(1 for audit in recent_audits if audit.requires_human_review),
            "improvement_trend": "stable"  # Calcularia baseado em histórico
        }
        
        return {
            "bias_statistics": bias_stats,
            "trends_analysis": trends,
            "recommendations_generated": len(bias_stats.get("recommendations", [])),
            "audit_period_days": 7
        }
    
    async def _execute_records_backup(self) -> Dict[str, Any]:
        """Faz backup dos registros de conformidade"""
        
        backup_data = {
            "backup_timestamp": datetime.now().isoformat(),
            "consent_records": [
                {
                    "id": consent.id,
                    "user_id": consent.user_id,
                    "purposes": [p.value for p in consent.purposes],
                    "granted_at": consent.granted_at.isoformat(),
                    "withdrawn_at": consent.withdrawn_at.isoformat() if consent.withdrawn_at else None,
                    "active": consent.is_active()
                }
                for consent in privacy_service.consent_records.values()
            ],
            "processing_records": [
                {
                    "id": record.id,
                    "data_subject_id": record.data_subject_id,
                    "data_categories": [c.value for c in record.data_categories],
                    "purposes": [p.value for p in record.processing_purposes],
                    "legal_basis": record.legal_basis.value,
                    "timestamp": record.timestamp.isoformat(),
                    "retention_period_days": record.retention_period.days,
                    "anonymized": record.anonymized,
                    "deleted": record.deleted
                }
                for record in privacy_service.processing_records
            ],
            "compliance_violations": [
                {
                    "type": violation.violation_type,
                    "description": violation.description,
                    "severity": violation.severity,
                    "user_id": violation.user_id,
                    "endpoint": violation.endpoint,
                    "timestamp": violation.timestamp.isoformat()
                }
                for violation in lgpd_middleware.compliance_violations
            ]
        }
        
        # Salvaria em storage seguro (S3, etc.)
        backup_file = f"compliance_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Por enquanto, salva localmente
        os.makedirs("backups", exist_ok=True)
        with open(f"backups/{backup_file}", "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        return {
            "backup_file": backup_file,
            "consent_records_backed_up": len(backup_data["consent_records"]),
            "processing_records_backed_up": len(backup_data["processing_records"]),
            "violations_backed_up": len(backup_data["compliance_violations"]),
            "backup_size_kb": os.path.getsize(f"backups/{backup_file}") / 1024
        }
    
    def _calculate_consolidated_score(self, 
                                    privacy_report: Dict[str, Any],
                                    middleware_report: Dict[str, Any],
                                    bias_report: Dict[str, Any]) -> float:
        """Calcula score consolidado de conformidade"""
        
        privacy_score = privacy_report.get("compliance_score", 100)
        middleware_score = middleware_report.get("compliance_score", 100)
        
        # Score de viés (inverte taxa de problemas)
        bias_rate = bias_report.get("bias_detection_rate", 0) / 100
        bias_score = max(0, 100 - (bias_rate * 50))
        
        # Média ponderada
        consolidated_score = (privacy_score * 0.4 + middleware_score * 0.4 + bias_score * 0.2)
        
        return round(consolidated_score, 2)
    
    async def _save_compliance_report(self, report: Dict[str, Any]):
        """Salva relatório de conformidade"""
        
        # Cria diretório se necessário
        os.makedirs("compliance_reports", exist_ok=True)
        
        # Nome do arquivo com timestamp
        filename = f"compliance_report_{datetime.now().strftime('%Y%m_%B')}.json"
        filepath = f"compliance_reports/{filename}"
        
        # Salva relatório
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Relatório de conformidade salvo: {filepath}")
    
    def _schedule_retry(self, task: ComplianceTask):
        """Agenda nova tentativa para tarefa falha"""
        
        retry_time = datetime.now() + timedelta(hours=1)
        
        # Em implementação real, usaria scheduler mais robusto
        self.logger.info(f"Reagendando {task.name} para {retry_time}")
    
    def get_monitor_status(self) -> Dict[str, Any]:
        """Retorna status atual do monitor"""
        
        return {
            "is_running": self.is_running,
            "total_tasks": len(self.tasks),
            "enabled_tasks": len([t for t in self.tasks if t.enabled]),
            "last_executions": self.execution_history[-5:] if self.execution_history else [],
            "next_scheduled_tasks": [
                {
                    "task_name": task.name,
                    "frequency": task.frequency,
                    "last_run": task.last_run.isoformat() if task.last_run else None,
                    "enabled": task.enabled
                }
                for task in self.tasks
            ],
            "config": self.config
        }
    
    async def manual_task_execution(self, task_id: str) -> Dict[str, Any]:
        """Executa tarefa manualmente para teste"""
        
        task = next((t for t in self.tasks if t.task_id == task_id), None)
        if not task:
            raise ValueError(f"Tarefa não encontrada: {task_id}")
        
        result = await self._execute_task(task)
        
        return {
            "task_id": task_id,
            "task_name": task.name,
            "execution_result": result,
            "executed_at": datetime.now().isoformat(),
            "execution_type": "manual"
        }

# Instância global
compliance_monitor = LGPDComplianceMonitor()