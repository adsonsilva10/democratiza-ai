"""
Termos de Serviço e Fundação Ética - Democratiza AI
Sistema de gestão de disclaimers, limitações legais e diretrizes éticas
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import json
from datetime import datetime

class ServiceType(Enum):
    """Tipos de serviços oferecidos pela plataforma"""
    CONTRACT_ANALYSIS = "contract_analysis"
    DOCUMENT_REVIEW = "document_review"
    LEGAL_GUIDANCE = "legal_guidance"
    RISK_ASSESSMENT = "risk_assessment"

class UserType(Enum):
    """Tipos de usuários da plataforma"""
    INDIVIDUAL_CPF = "individual_cpf"  # Pessoa física
    SMALL_BUSINESS_CNPJ = "small_business_cnpj"  # Micro/pequena empresa
    LARGE_BUSINESS_CNPJ = "large_business_cnpj"  # Empresa de grande porte

@dataclass
class LegalDisclaimer:
    """Modelo de disclaimer legal específico"""
    service_type: ServiceType
    user_type: UserType
    title: str
    content: str
    severity: str  # "critical", "important", "informative"
    legal_basis: str
    last_updated: datetime

class TermsOfService:
    """
    Gerenciador central de Termos de Serviço e Disclaimers Legais
    
    Responsável por:
    1. Definir limitações claras do serviço
    2. Estabelecer disclaimers específicos por tipo de análise
    3. Garantir conformidade com regulamentações
    4. Proteger usuários e plataforma juridicamente
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.effective_date = datetime(2024, 1, 15)
        self.disclaimers = self._initialize_disclaimers()
    
    def _initialize_disclaimers(self) -> Dict[str, LegalDisclaimer]:
        """Inicializa todos os disclaimers legais necessários"""
        disclaimers = {}
        
        # Disclaimer principal - Natureza informativa
        disclaimers["main_service"] = LegalDisclaimer(
            service_type=ServiceType.CONTRACT_ANALYSIS,
            user_type=UserType.INDIVIDUAL_CPF,
            title="Natureza Informativa dos Serviços",
            content="""
            IMPORTANTE: Os serviços da Democratiza AI têm caráter EXCLUSIVAMENTE INFORMATIVO 
            e educacional. NÃO constituem:
            
            • Consultoria jurídica personalizada
            • Aconselhamento legal profissional  
            • Opinião jurídica vinculante
            • Substituição à orientação de advogado
            
            As análises são geradas por inteligência artificial e podem conter imprecisões.
            SEMPRE consulte um advogado qualificado para decisões jurídicas importantes.
            """,
            severity="critical",
            legal_basis="Art. 1º Lei 8.906/94 (Estatuto da OAB) - Exercício da advocacia",
            last_updated=datetime.now()
        )
        
        # Disclaimer para análise de contratos
        disclaimers["contract_analysis"] = LegalDisclaimer(
            service_type=ServiceType.CONTRACT_ANALYSIS,
            user_type=UserType.INDIVIDUAL_CPF,
            title="Limitações da Análise Contratual",
            content="""
            A análise de contratos oferecida:
            
            ✓ Identifica pontos de atenção gerais
            ✓ Destaca cláusulas potencialmente desfavoráveis
            ✓ Fornece orientações educativas sobre direitos
            
            ✗ NÃO substitui revisão jurídica profissional
            ✗ NÃO garante identificação de todos os riscos
            ✗ NÃO constitui parecer jurídico válido
            
            Recomendamos fortemente consultar advogado antes de assinar 
            contratos de alto valor ou complexidade.
            """,
            severity="important",
            legal_basis="CDC Art. 6º, III - Direito à informação adequada",
            last_updated=datetime.now()
        )
        
        # Disclaimer para empresas (CNPJ)
        disclaimers["business_services"] = LegalDisclaimer(
            service_type=ServiceType.DOCUMENT_REVIEW,
            user_type=UserType.SMALL_BUSINESS_CNPJ,
            title="Serviços para Pessoas Jurídicas",
            content="""
            Para empresas (CNPJ), nossos serviços são ferramentas de apoio 
            à gestão documental e análise preliminar.
            
            RESPONSABILIDADES DA EMPRESA:
            • Validar todas as análises com departamento jurídico
            • Não tomar decisões baseadas apenas em nossas análises
            • Manter assessoria jurídica qualificada
            • Compreender limitações da automação
            
            Especialmente crítico para contratos B2B, fusões, aquisições 
            e operações de alto valor financeiro.
            """,
            severity="critical",
            legal_basis="CC Art. 421 - Função social do contrato",
            last_updated=datetime.now()
        )
        
        # Disclaimer sobre IA e precisão
        disclaimers["ai_limitations"] = LegalDisclaimer(
            service_type=ServiceType.RISK_ASSESSMENT,
            user_type=UserType.INDIVIDUAL_CPF,
            title="Limitações da Inteligência Artificial",
            content="""
            Nossa IA é treinada com vasta base jurídica brasileira, mas:
            
            PODE FALHAR EM:
            • Nuances jurídicas muito específicas
            • Jurisprudência recente não incorporada
            • Casos excepcionais ou atípicos
            • Interpretações subjetivas complexas
            
            SEMPRE VERIFIQUE:
            • Informações críticas com fontes oficiais
            • Prazos e datas com calendário jurídico
            • Valores e cálculos com profissional
            • Estratégias jurídicas com advogado
            """,
            severity="important", 
            legal_basis="Lei 13.709/18 (LGPD) Art. 20 - Decisões automatizadas",
            last_updated=datetime.now()
        )
        
        return disclaimers
    
    def get_applicable_disclaimers(self, 
                                 service_type: ServiceType,
                                 user_type: UserType) -> List[LegalDisclaimer]:
        """Retorna disclaimers aplicáveis para contexto específico"""
        applicable = []
        
        # Disclaimer principal sempre aplicável
        applicable.append(self.disclaimers["main_service"])
        
        # Disclaimer sobre limitações da IA sempre aplicável
        applicable.append(self.disclaimers["ai_limitations"])
        
        # Disclaimers específicos por tipo de serviço
        if service_type == ServiceType.CONTRACT_ANALYSIS:
            applicable.append(self.disclaimers["contract_analysis"])
        
        # Disclaimers específicos por tipo de usuário
        if user_type in [UserType.SMALL_BUSINESS_CNPJ, UserType.LARGE_BUSINESS_CNPJ]:
            applicable.append(self.disclaimers["business_services"])
        
        return applicable
    
    def format_disclaimers_for_response(self,
                                      service_type: ServiceType,
                                      user_type: UserType) -> str:
        """Formata disclaimers para incluir na resposta do agente"""
        disclaimers = self.get_applicable_disclaimers(service_type, user_type)
        
        formatted = "\n\n" + "="*60 + "\n"
        formatted += "⚖️  AVISOS LEGAIS IMPORTANTES\n"
        formatted += "="*60 + "\n\n"
        
        for disclaimer in disclaimers:
            if disclaimer.severity == "critical":
                icon = "🚨"
            elif disclaimer.severity == "important":
                icon = "⚠️"
            else:
                icon = "ℹ️"
            
            formatted += f"{icon} {disclaimer.title}\n"
            formatted += disclaimer.content.strip() + "\n\n"
        
        formatted += "📞 DÚVIDAS? Consulte sempre um advogado qualificado.\n"
        formatted += f"📅 Versão dos Termos: {self.version} - {self.effective_date.strftime('%d/%m/%Y')}\n"
        formatted += "="*60
        
        return formatted
    
    def get_pre_analysis_warning(self, user_type: UserType) -> str:
        """Warning a ser exibido ANTES da análise começar"""
        if user_type == UserType.INDIVIDUAL_CPF:
            return """
🚨 ATENÇÃO: Esta análise tem caráter INFORMATIVO e NÃO substitui consultoria jurídica.
📚 Use para entender melhor o documento, mas consulte advogado para decisões importantes.
⚖️ A Democratiza AI não se responsabiliza por decisões baseadas apenas nesta análise.
            """.strip()
        else:
            return """
🚨 ATENÇÃO EMPRESARIAL: Análise preliminar para apoio à gestão documental.
🏢 Sempre valide com departamento jurídico antes de tomar decisões.
⚖️ Não substitui assessoria jurídica profissional especializada.
            """.strip()
    
    def should_require_explicit_consent(self, 
                                      service_type: ServiceType,
                                      user_type: UserType) -> bool:
        """Define se deve exigir consentimento explícito do usuário"""
        # Sempre exigir consentimento para análises contratuais
        if service_type == ServiceType.CONTRACT_ANALYSIS:
            return True
        
        # Sempre exigir para empresas
        if user_type in [UserType.SMALL_BUSINESS_CNPJ, UserType.LARGE_BUSINESS_CNPJ]:
            return True
        
        return False
    
    def get_consent_text(self, service_type: ServiceType) -> str:
        """Texto de consentimento explícito"""
        return f"""
Ao prosseguir, você DECLARA que:

✓ Compreende que este serviço é INFORMATIVO
✓ NÃO substitui consultoria jurídica profissional  
✓ Consultará advogado para decisões importantes
✓ A Democratiza AI não se responsabiliza por suas decisões
✓ Leu e aceita as limitações do serviço

Digite 'ACEITO' para continuar com a análise.
        """.strip()
    
    def export_terms_summary(self) -> Dict:
        """Exporta resumo dos termos para documentação"""
        return {
            "version": self.version,
            "effective_date": self.effective_date.isoformat(),
            "disclaimer_count": len(self.disclaimers),
            "service_types": [t.value for t in ServiceType],
            "user_types": [t.value for t in UserType],
            "compliance_frameworks": [
                "Lei 8.906/94 (Estatuto da OAB)",
                "Lei 13.709/18 (LGPD)", 
                "Código de Defesa do Consumidor",
                "Código Civil Brasileiro"
            ]
        }

# Instância global
terms_service = TermsOfService()