"""
LGPD Compliance Middleware - Democratiza AI
Middleware para interceptar e garantir conformidade em todas as operações
"""

from typing import Dict, Any, List, Optional
from fastapi import Request, Response, HTTPException, status
from datetime import datetime, timedelta
import asyncio
import logging
from dataclasses import dataclass
import json

from app.legal.privacy_service import privacy_service, DataCategory, ProcessingPurpose, LegalBasis
from app.legal.terms_of_service import terms_service, ServiceType, UserType

@dataclass
class ComplianceViolation:
    """Registro de violação de conformidade"""
    violation_type: str
    description: str
    severity: str  # "low", "medium", "high", "critical"
    user_id: Optional[str] = None
    endpoint: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class LGPDComplianceMiddleware:
    """
    Middleware central de conformidade LGPD
    
    Funcionalidades:
    1. Interceptação automática de dados pessoais
    2. Verificação de consentimento em tempo real  
    3. Registro de tratamento transparente
    4. Monitoramento de violações de compliance
    5. Aplicação de políticas de retenção
    6. Auditoria contínua de operações
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.compliance_violations: List[ComplianceViolation] = []
        self.monitored_endpoints = self._initialize_monitored_endpoints()
        self.data_processing_stats = {
            "total_operations": 0,
            "consent_violations": 0,
            "successful_anonymizations": 0,
            "retention_violations": 0,
            "last_audit": datetime.now()
        }
    
    def _initialize_monitored_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """Define endpoints que requerem monitoramento LGPD"""
        return {
            "/api/v1/contracts/ethical/analyze": {
                "requires_consent": True,
                "data_categories": [DataCategory.DOCUMENTO, DataCategory.COMPORTAMENTAL],
                "purposes": [ProcessingPurpose.CONTRACT_ANALYSIS, ProcessingPurpose.SERVICE_PROVISION],
                "legal_basis": LegalBasis.CONSENT,
                "retention_days": 365
            },
            "/api/v1/contracts/upload": {
                "requires_consent": True,
                "data_categories": [DataCategory.DOCUMENTO],
                "purposes": [ProcessingPurpose.CONTRACT_ANALYSIS],
                "legal_basis": LegalBasis.CONSENT,
                "retention_days": 365
            },
            "/api/v1/chat/": {
                "requires_consent": True,
                "data_categories": [DataCategory.COMPORTAMENTAL, DataCategory.CONTATO],
                "purposes": [ProcessingPurpose.SERVICE_PROVISION, ProcessingPurpose.IMPROVEMENT],
                "legal_basis": LegalBasis.CONSENT,
                "retention_days": 180
            },
            "/api/v1/contracts/analyze": {
                "requires_consent": True,
                "data_categories": [DataCategory.DOCUMENTO],
                "purposes": [ProcessingPurpose.CONTRACT_ANALYSIS],
                "legal_basis": LegalBasis.CONSENT,
                "retention_days": 365
            }
        }
    
    async def process_request(self, request: Request, user_id: str = None) -> Dict[str, Any]:
        """
        Processa requisição verificando conformidade LGPD
        
        Returns:
            Dict com status de conformidade e ações necessárias
        """
        
        endpoint = str(request.url.path)
        method = request.method
        
        self.data_processing_stats["total_operations"] += 1
        
        # Verifica se endpoint requer monitoramento
        endpoint_config = self._get_endpoint_config(endpoint)
        if not endpoint_config:
            return {"status": "not_monitored", "action": "continue"}
        
        # Verifica consentimento se necessário
        if endpoint_config.get("requires_consent") and user_id:
            consent_status = await self._verify_consent(user_id, endpoint_config)
            if consent_status["requires_action"]:
                return consent_status
        
        # Registra tratamento de dados
        if user_id:
            processing_record_id = await self._register_data_processing(
                user_id, endpoint_config, request
            )
            
            return {
                "status": "compliant",
                "action": "continue",
                "processing_record_id": processing_record_id
            }
        
        return {"status": "compliant", "action": "continue"}
    
    async def process_response(self, 
                             request: Request, 
                             response: Response,
                             user_id: str = None) -> Dict[str, Any]:
        """Processa resposta aplicando políticas de privacidade"""
        
        endpoint = str(request.url.path)
        endpoint_config = self._get_endpoint_config(endpoint)
        
        if not endpoint_config or not user_id:
            return {"status": "not_processed"}
        
        # Aplica anonimização se configurado
        if endpoint_config.get("auto_anonymize", False):
            # Aqui poderia interceptar response body e anonimizar
            pass
        
        # Registra acesso aos dados
        self._log_data_access(user_id, endpoint, "response_delivered")
        
        return {"status": "processed"}
    
    def _get_endpoint_config(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Obtém configuração de monitoramento para endpoint"""
        
        # Busca exata
        if endpoint in self.monitored_endpoints:
            return self.monitored_endpoints[endpoint]
        
        # Busca por padrão (endpoints que começam com...)
        for monitored_endpoint, config in self.monitored_endpoints.items():
            if endpoint.startswith(monitored_endpoint.rstrip("/")):
                return config
        
        return None
    
    async def _verify_consent(self, user_id: str, endpoint_config: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica se usuário tem consentimento válido"""
        
        required_purposes = endpoint_config.get("purposes", [])
        
        # Verifica cada propósito necessário
        missing_consents = []
        for purpose in required_purposes:
            if not privacy_service.check_consent_valid(user_id, purpose):
                missing_consents.append(purpose)
        
        if missing_consents:
            # Registra violação
            self._record_compliance_violation(
                violation_type="consent_missing",
                description=f"Usuário {user_id} sem consentimento para: {[p.value for p in missing_consents]}",
                severity="high",
                user_id=user_id
            )
            
            self.data_processing_stats["consent_violations"] += 1
            
            return {
                "status": "consent_required",
                "requires_action": True,
                "missing_consents": [p.value for p in missing_consents],
                "consent_text": privacy_service._generate_consent_text(required_purposes),
                "action": "request_consent"
            }
        
        return {"status": "consent_valid", "requires_action": False}
    
    async def _register_data_processing(self, 
                                      user_id: str,
                                      endpoint_config: Dict[str, Any],
                                      request: Request) -> str:
        """Registra tratamento de dados conforme LGPD Art. 37"""
        
        processing_record_id = privacy_service.record_data_processing(
            data_subject_id=user_id,
            data_categories=endpoint_config.get("data_categories", []),
            purposes=endpoint_config.get("purposes", []),
            legal_basis=endpoint_config.get("legal_basis", LegalBasis.CONSENT),
            retention_days=endpoint_config.get("retention_days", 365)
        )
        
        # Log detalhado para auditoria
        self.logger.info(
            f"Data processing registered: {processing_record_id} | "
            f"User: {user_id} | Endpoint: {request.url.path} | "
            f"Categories: {[c.value for c in endpoint_config.get('data_categories', [])]}"
        )
        
        return processing_record_id
    
    def _log_data_access(self, user_id: str, endpoint: str, action: str):
        """Registra acesso aos dados para auditoria"""
        
        self.logger.info(
            f"Data access logged: User {user_id} | Endpoint: {endpoint} | Action: {action} | "
            f"Timestamp: {datetime.now().isoformat()}"
        )
    
    def _record_compliance_violation(self, 
                                   violation_type: str,
                                   description: str,
                                   severity: str,
                                   user_id: str = None,
                                   endpoint: str = None):
        """Registra violação de conformidade"""
        
        violation = ComplianceViolation(
            violation_type=violation_type,
            description=description,
            severity=severity,
            user_id=user_id,
            endpoint=endpoint
        )
        
        self.compliance_violations.append(violation)
        
        # Log baseado na severidade
        if severity in ["critical", "high"]:
            self.logger.error(f"Compliance violation [{severity}]: {description}")
        else:
            self.logger.warning(f"Compliance violation [{severity}]: {description}")
    
    async def cleanup_expired_data(self) -> Dict[str, Any]:
        """
        Executa limpeza automática de dados expirados
        Deve ser chamado periodicamente (cronjob)
        """
        
        cleanup_stats = {
            "processed_records": 0,
            "deleted_records": 0,
            "anonymized_records": 0,
            "errors": 0,
            "start_time": datetime.now()
        }
        
        try:
            # Identifica registros expirados
            expired_records = [
                record for record in privacy_service.processing_records
                if (datetime.now() - record.timestamp) > record.retention_period
                and not record.deleted and not record.anonymized
            ]
            
            cleanup_stats["processed_records"] = len(expired_records)
            
            for record in expired_records:
                try:
                    if record.legal_basis == LegalBasis.CONSENT:
                        # Deleta dados baseados em consentimento
                        record.deleted = True
                        cleanup_stats["deleted_records"] += 1
                    else:
                        # Anonimiza outros dados
                        record.anonymized = True
                        cleanup_stats["anonymized_records"] += 1
                        
                except Exception as e:
                    cleanup_stats["errors"] += 1
                    self.logger.error(f"Error cleaning up record {record.id}: {str(e)}")
            
            self.logger.info(f"Data cleanup completed: {cleanup_stats}")
            
        except Exception as e:
            cleanup_stats["errors"] += 1
            self.logger.error(f"Error during data cleanup: {str(e)}")
        
        cleanup_stats["end_time"] = datetime.now()
        cleanup_stats["duration_seconds"] = (
            cleanup_stats["end_time"] - cleanup_stats["start_time"]
        ).total_seconds()
        
        return cleanup_stats
    
    def get_compliance_dashboard(self) -> Dict[str, Any]:
        """Gera dashboard de conformidade em tempo real"""
        
        # Análise de violações por tipo
        violations_by_type = {}
        violations_by_severity = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        for violation in self.compliance_violations:
            violations_by_type[violation.violation_type] = \
                violations_by_type.get(violation.violation_type, 0) + 1
            violations_by_severity[violation.severity] += 1
        
        # Estatísticas de processamento
        processing_stats = privacy_service.generate_compliance_report()
        
        # Análise de tendências (últimos 30 dias)
        recent_violations = [
            v for v in self.compliance_violations
            if datetime.now() - v.timestamp <= timedelta(days=30)
        ]
        
        return {
            "compliance_score": self._calculate_overall_compliance_score(),
            "processing_statistics": self.data_processing_stats,
            "privacy_compliance": processing_stats,
            "violations_summary": {
                "total_violations": len(self.compliance_violations),
                "recent_violations": len(recent_violations),
                "by_type": violations_by_type,
                "by_severity": violations_by_severity
            },
            "monitored_endpoints": list(self.monitored_endpoints.keys()),
            "last_updated": datetime.now().isoformat(),
            "recommendations": self._generate_compliance_recommendations()
        }
    
    def _calculate_overall_compliance_score(self) -> float:
        """Calcula score geral de conformidade (0-100)"""
        
        score = 100.0
        
        if self.data_processing_stats["total_operations"] > 0:
            # Penaliza violações de consentimento
            consent_violation_rate = (
                self.data_processing_stats["consent_violations"] / 
                self.data_processing_stats["total_operations"]
            )
            score -= consent_violation_rate * 50
            
            # Penaliza violações críticas
            critical_violations = sum(
                1 for v in self.compliance_violations 
                if v.severity == "critical"
            )
            score -= critical_violations * 10
            
            # Penaliza violações de retenção
            retention_violation_rate = (
                self.data_processing_stats["retention_violations"] / 
                max(self.data_processing_stats["total_operations"], 1)
            )
            score -= retention_violation_rate * 30
        
        return max(0.0, score)
    
    def _generate_compliance_recommendations(self) -> List[str]:
        """Gera recomendações para melhorar conformidade"""
        
        recommendations = []
        
        # Análise de violações recentes
        recent_violations = [
            v for v in self.compliance_violations
            if datetime.now() - v.timestamp <= timedelta(days=7)
        ]
        
        if recent_violations:
            violation_types = set(v.violation_type for v in recent_violations)
            
            if "consent_missing" in violation_types:
                recommendations.append(
                    "Implementar verificação proativa de consentimento antes do processamento"
                )
            
            critical_violations = [v for v in recent_violations if v.severity == "critical"]
            if critical_violations:
                recommendations.append(
                    "Revisar imediatamente operações que causaram violações críticas"
                )
        
        # Análise de taxa de conformidade
        compliance_score = self._calculate_overall_compliance_score()
        
        if compliance_score < 90:
            recommendations.append("Melhorar processos de verificação de consentimento")
        
        if compliance_score < 70:
            recommendations.append("Implementar treinamento adicional em conformidade LGPD")
            recommendations.append("Revisar políticas de retenção de dados")
        
        if not recommendations:
            recommendations.append("Manter bom nível de conformidade atual")
        
        return recommendations
    
    async def generate_audit_report(self, days: int = 30) -> Dict[str, Any]:
        """Gera relatório detalhado de auditoria"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filtra dados do período
        recent_violations = [
            v for v in self.compliance_violations
            if v.timestamp >= cutoff_date
        ]
        
        recent_processing = [
            r for r in privacy_service.processing_records
            if r.timestamp >= cutoff_date
        ]
        
        return {
            "audit_period": {
                "start_date": cutoff_date.isoformat(),
                "end_date": datetime.now().isoformat(),
                "days": days
            },
            "compliance_overview": {
                "overall_score": self._calculate_overall_compliance_score(),
                "total_operations": len(recent_processing),
                "violations_count": len(recent_violations),
                "compliance_rate": (
                    (len(recent_processing) - len(recent_violations)) / 
                    max(len(recent_processing), 1) * 100
                )
            },
            "detailed_violations": [
                {
                    "type": v.violation_type,
                    "description": v.description,
                    "severity": v.severity,
                    "timestamp": v.timestamp.isoformat(),
                    "user_id": v.user_id,
                    "endpoint": v.endpoint
                }
                for v in recent_violations
            ],
            "processing_analysis": {
                "total_records": len(recent_processing),
                "by_legal_basis": self._analyze_processing_by_basis(recent_processing),
                "by_data_category": self._analyze_processing_by_category(recent_processing),
                "retention_compliance": self._analyze_retention_compliance(recent_processing)
            },
            "recommendations": self._generate_compliance_recommendations(),
            "generated_at": datetime.now().isoformat()
        }
    
    def _analyze_processing_by_basis(self, records: List) -> Dict[str, int]:
        """Analisa registros por base legal"""
        basis_counts = {}
        for record in records:
            basis = record.legal_basis.value
            basis_counts[basis] = basis_counts.get(basis, 0) + 1
        return basis_counts
    
    def _analyze_processing_by_category(self, records: List) -> Dict[str, int]:
        """Analisa registros por categoria de dados"""
        category_counts = {}
        for record in records:
            for category in record.data_categories:
                cat_value = category.value
                category_counts[cat_value] = category_counts.get(cat_value, 0) + 1
        return category_counts
    
    def _analyze_retention_compliance(self, records: List) -> Dict[str, Any]:
        """Analisa conformidade de retenção"""
        now = datetime.now()
        expired_records = [
            r for r in records
            if (now - r.timestamp) > r.retention_period
        ]
        
        return {
            "total_records": len(records),
            "expired_records": len(expired_records),
            "compliance_rate": (
                (len(records) - len(expired_records)) / max(len(records), 1) * 100
            ),
            "needs_cleanup": len([r for r in expired_records if not r.deleted and not r.anonymized])
        }

# Instância global
lgpd_middleware = LGPDComplianceMiddleware()