"""
LGPD Compliance Infrastructure - Democratiza AI
Sistema de conformidade com Lei Geral de Proteção de Dados
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from enum import Enum
from datetime import datetime, timedelta
import hashlib
import json
import uuid
import logging
from cryptography.fernet import Fernet
import base64
import os

class DataCategory(Enum):
    """Categorias de dados pessoais segundo LGPD"""
    IDENTIFICACAO = "identificacao"  # Nome, CPF, RG, etc.
    CONTATO = "contato"  # Email, telefone, endereço
    DOCUMENTO = "documento"  # Conteúdo de contratos
    COMPORTAMENTAL = "comportamental"  # Uso da plataforma
    SENSIVEL = "sensivel"  # Dados sensíveis (se houver)

class ProcessingPurpose(Enum):
    """Finalidades de tratamento segundo LGPD"""
    CONTRACT_ANALYSIS = "analise_contratual"
    SERVICE_PROVISION = "prestacao_servico"
    LEGAL_COMPLIANCE = "cumprimento_legal"
    SECURITY = "seguranca"
    IMPROVEMENT = "melhorias"

class LegalBasis(Enum):
    """Bases legais para tratamento (Art. 7º LGPD)"""
    CONSENT = "consentimento"  # Art. 7º, I
    CONTRACT = "contrato"  # Art. 7º, V  
    LEGAL_OBLIGATION = "obrigacao_legal"  # Art. 7º, II
    LEGITIMATE_INTEREST = "interesse_legitimo"  # Art. 7º, IX
    VITAL_INTEREST = "interesse_vital"  # Art. 7º, IV

@dataclass
class DataProcessingRecord:
    """Registro de tratamento de dados (Art. 37 LGPD)"""
    id: str
    data_subject_id: str  # ID do titular
    data_categories: List[DataCategory]
    processing_purposes: List[ProcessingPurpose]
    legal_basis: LegalBasis
    timestamp: datetime
    retention_period: timedelta
    anonymized: bool = False
    deleted: bool = False
    consent_withdrawn: bool = False
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())

@dataclass
class ConsentRecord:
    """Registro de consentimento do titular"""
    id: str
    user_id: str
    purposes: List[ProcessingPurpose] 
    granted_at: datetime
    withdrawn_at: Optional[datetime] = None
    ip_address: str = ""
    user_agent: str = ""
    consent_text: str = ""
    
    def is_active(self) -> bool:
        return self.withdrawn_at is None

class PrivacyService:
    """
    Serviço central de privacidade e conformidade LGPD
    
    Implementa:
    1. Registro e controle de consentimentos
    2. Anonimização e pseudonimização
    3. Auditoria de tratamento de dados
    4. Gestão de direitos do titular
    5. Relatórios de conformidade
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._encryption_key = self._get_or_create_encryption_key()
        self._cipher_suite = Fernet(self._encryption_key)
        
        # Armazenamento em memória (produção usaria banco)
        self.consent_records: Dict[str, ConsentRecord] = {}
        self.processing_records: List[DataProcessingRecord] = []
        self.anonymization_mappings: Dict[str, str] = {}
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Gera ou recupera chave de criptografia"""
        key_file = "encryption_key.key"
        
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key
    
    def record_consent(self,
                      user_id: str,
                      purposes: List[ProcessingPurpose],
                      ip_address: str = "",
                      user_agent: str = "") -> str:
        """Registra consentimento do usuário (Art. 8º LGPD)"""
        
        consent_text = self._generate_consent_text(purposes)
        
        consent = ConsentRecord(
            id=str(uuid.uuid4()),
            user_id=user_id,
            purposes=purposes,
            granted_at=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            consent_text=consent_text
        )
        
        self.consent_records[consent.id] = consent
        
        self.logger.info(f"Consent recorded: {consent.id} for user {user_id}")
        return consent.id
    
    def withdraw_consent(self, user_id: str, consent_id: str) -> bool:
        """Revoga consentimento (Art. 8º, §5º LGPD)"""
        
        if consent_id not in self.consent_records:
            return False
        
        consent = self.consent_records[consent_id]
        if consent.user_id != user_id:
            return False
        
        consent.withdrawn_at = datetime.now()
        
        # Marca registros relacionados como consentimento retirado
        for record in self.processing_records:
            if (record.data_subject_id == user_id and 
                record.legal_basis == LegalBasis.CONSENT):
                record.consent_withdrawn = True
        
        self.logger.info(f"Consent withdrawn: {consent_id} by user {user_id}")
        return True
    
    def check_consent_valid(self, user_id: str, purpose: ProcessingPurpose) -> bool:
        """Verifica se há consentimento válido para finalidade específica"""
        
        for consent in self.consent_records.values():
            if (consent.user_id == user_id and 
                consent.is_active() and 
                purpose in consent.purposes):
                return True
        
        return False
    
    def record_data_processing(self,
                             data_subject_id: str,
                             data_categories: List[DataCategory],
                             purposes: List[ProcessingPurpose],
                             legal_basis: LegalBasis,
                             retention_days: int = 365) -> str:
        """Registra tratamento de dados pessoais (Art. 37 LGPD)"""
        
        record = DataProcessingRecord(
            id=str(uuid.uuid4()),
            data_subject_id=data_subject_id,
            data_categories=data_categories,
            processing_purposes=purposes,
            legal_basis=legal_basis,
            timestamp=datetime.now(),
            retention_period=timedelta(days=retention_days)
        )
        
        self.processing_records.append(record)
        
        self.logger.info(f"Data processing recorded: {record.id}")
        return record.id
    
    def anonymize_text(self, text: str, user_id: str) -> str:
        """Anonimiza texto substituindo dados pessoais (Art. 12 LGPD)"""
        
        # Padrões comuns de dados pessoais
        patterns = {
            'cpf': r'\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11}',
            'cnpj': r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{14}',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\(\d{2}\)\s?\d{4,5}-?\d{4}',
            'cep': r'\d{5}-?\d{3}'
        }
        
        anonymized_text = text
        
        import re
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                # Gera hash consistente para o mesmo valor
                hash_key = f"{user_id}:{match}"
                if hash_key not in self.anonymization_mappings:
                    hash_value = hashlib.sha256(hash_key.encode()).hexdigest()[:8]
                    self.anonymization_mappings[hash_key] = f"[{pattern_name.upper()}_{hash_value}]"
                
                anonymized_text = anonymized_text.replace(match, self.anonymization_mappings[hash_key])
        
        return anonymized_text
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Criptografa dados sensíveis"""
        encrypted = self._cipher_suite.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Descriptografa dados sensíveis"""
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted = self._cipher_suite.decrypt(encrypted_bytes)
        return decrypted.decode()
    
    def delete_user_data(self, user_id: str) -> Dict[str, Any]:
        """Exerce direito de eliminação (Art. 18, VI LGPD)"""
        
        deleted_count = 0
        anonymized_count = 0
        
        # Marca registros como deletados
        for record in self.processing_records:
            if record.data_subject_id == user_id:
                if record.legal_basis == LegalBasis.CONSENT:
                    record.deleted = True
                    deleted_count += 1
                else:
                    # Se não for consentimento, anonimiza
                    record.anonymized = True
                    record.data_subject_id = f"ANON_{hashlib.sha256(user_id.encode()).hexdigest()[:8]}"
                    anonymized_count += 1
        
        # Remove consentimentos
        consent_ids_to_remove = []
        for consent_id, consent in self.consent_records.items():
            if consent.user_id == user_id:
                consent_ids_to_remove.append(consent_id)
        
        for consent_id in consent_ids_to_remove:
            del self.consent_records[consent_id]
        
        result = {
            "user_id": user_id,
            "deleted_records": deleted_count,
            "anonymized_records": anonymized_count,
            "consent_records_removed": len(consent_ids_to_remove),
            "processed_at": datetime.now().isoformat()
        }
        
        self.logger.info(f"User data deletion completed: {result}")
        return result
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """Direito de portabilidade (Art. 18, V LGPD)"""
        
        user_consents = [
            {
                "id": consent.id,
                "purposes": [p.value for p in consent.purposes],
                "granted_at": consent.granted_at.isoformat(),
                "withdrawn_at": consent.withdrawn_at.isoformat() if consent.withdrawn_at else None,
                "active": consent.is_active()
            }
            for consent in self.consent_records.values()
            if consent.user_id == user_id
        ]
        
        user_processing = [
            {
                "id": record.id,
                "data_categories": [c.value for c in record.data_categories],
                "purposes": [p.value for p in record.processing_purposes],
                "legal_basis": record.legal_basis.value,
                "timestamp": record.timestamp.isoformat(),
                "retention_period_days": record.retention_period.days,
                "anonymized": record.anonymized,
                "deleted": record.deleted
            }
            for record in self.processing_records
            if record.data_subject_id == user_id and not record.deleted
        ]
        
        return {
            "user_id": user_id,
            "export_date": datetime.now().isoformat(),
            "consent_records": user_consents,
            "processing_records": user_processing,
            "total_records": len(user_processing)
        }
    
    def _generate_consent_text(self, purposes: List[ProcessingPurpose]) -> str:
        """Gera texto de consentimento claro e específico"""
        
        purpose_descriptions = {
            ProcessingPurpose.CONTRACT_ANALYSIS: "análise de contratos e documentos jurídicos",
            ProcessingPurpose.SERVICE_PROVISION: "prestação dos serviços da plataforma",
            ProcessingPurpose.LEGAL_COMPLIANCE: "cumprimento de obrigações legais",
            ProcessingPurpose.SECURITY: "segurança da plataforma e prevenção de fraudes",
            ProcessingPurpose.IMPROVEMENT: "melhoria dos serviços e experiência do usuário"
        }
        
        purposes_text = ", ".join([purpose_descriptions.get(p, p.value) for p in purposes])
        
        return f"""
Ao concordar, você autoriza a Democratiza AI a tratar seus dados pessoais para as seguintes finalidades: {purposes_text}.

Seus direitos como titular:
• Acesso aos seus dados
• Correção de dados incorretos
• Portabilidade dos dados
• Eliminação dos dados
• Revogação do consentimento a qualquer momento

Para exercer seus direitos, entre em contato através do nosso canal de privacidade.
        """.strip()
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """Gera relatório de conformidade LGPD"""
        
        active_consents = sum(1 for c in self.consent_records.values() if c.is_active())
        withdrawn_consents = sum(1 for c in self.consent_records.values() if not c.is_active())
        
        processing_by_basis = {}
        for record in self.processing_records:
            basis = record.legal_basis.value
            processing_by_basis[basis] = processing_by_basis.get(basis, 0) + 1
        
        expired_records = sum(
            1 for record in self.processing_records
            if datetime.now() - record.timestamp > record.retention_period
        )
        
        return {
            "report_date": datetime.now().isoformat(),
            "consent_summary": {
                "active_consents": active_consents,
                "withdrawn_consents": withdrawn_consents,
                "total_consents": len(self.consent_records)
            },
            "processing_summary": {
                "total_records": len(self.processing_records),
                "by_legal_basis": processing_by_basis,
                "expired_records": expired_records,
                "anonymized_records": sum(1 for r in self.processing_records if r.anonymized),
                "deleted_records": sum(1 for r in self.processing_records if r.deleted)
            },
            "data_categories_processed": list(set(
                cat.value for record in self.processing_records 
                for cat in record.data_categories
            )),
            "compliance_score": self._calculate_compliance_score()
        }
    
    def _calculate_compliance_score(self) -> float:
        """Calcula score de conformidade (0-100)"""
        
        if not self.processing_records:
            return 100.0
        
        score = 100.0
        
        # Penaliza registros sem base legal clara
        invalid_basis = sum(1 for r in self.processing_records if not r.legal_basis)
        score -= (invalid_basis / len(self.processing_records)) * 30
        
        # Penaliza registros expirados não tratados
        expired = sum(
            1 for r in self.processing_records
            if datetime.now() - r.timestamp > r.retention_period and not r.anonymized and not r.deleted
        )
        score -= (expired / len(self.processing_records)) * 25
        
        # Penaliza consentimentos sem registro de tratamento
        orphan_consents = sum(
            1 for consent in self.consent_records.values()
            if not any(r.data_subject_id == consent.user_id for r in self.processing_records)
        )
        if self.consent_records:
            score -= (orphan_consents / len(self.consent_records)) * 20
        
        return max(0.0, score)

# Instância global
privacy_service = PrivacyService()