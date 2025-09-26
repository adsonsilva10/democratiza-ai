from typing import Dict, Any, Optional
from app.agents.intelligent_classifier import IntelligentClassifier

# Importar todos os agentes especializados
from app.agents.base_agent import BaseContractAgent
from app.agents.rental_agent import RentalAgent  # Geral residencial
from app.agents.rental_commercial_agent import RentalCommercialAgent
from app.agents.real_estate_agent import RealEstateAgent
from app.agents.personal_loan_agent import PersonalLoanAgent
from app.agents.health_insurance_agent import HealthInsuranceAgent
from app.agents.internet_agent import InternetAgent
from app.agents.vehicle_insurance_agent import VehicleInsuranceAgent
from app.agents.credit_card_agent import CreditCardAgent
from app.agents.employment_clt_agent import EmploymentCLTAgent
from app.agents.vehicle_financing_agent import VehicleFinancingAgent
from app.agents.consortium_agent import ConsortiumAgent
from app.agents.tv_subscription_agent import TVSubscriptionAgent
from app.agents.life_insurance_agent import LifeInsuranceAgent
from app.agents.telecom_agent import TelecomAgent  # Geral telecom
from app.agents.financial_agent import FinancialAgent  # Geral financeiro

class IntelligentAgentFactory:
    """Factory inteligente para criação automática de agentes especializados"""
    
    def __init__(self):
        self.classifier = IntelligentClassifier()
        
        # Mapeamento completo categoria -> classe do agente
        self._agent_registry = {
            # HABITAÇÃO
            'rental_residential': RentalAgent,  # Usa o existente
            'rental_commercial': RentalCommercialAgent,
            'real_estate': RealEstateAgent,
            'housing_financing': PersonalLoanAgent,  # Temporário, usar financeiro para habitação
            
            # FINANCEIRO  
            'personal_loan': PersonalLoanAgent,
            'credit_card': CreditCardAgent,
            'vehicle_financing': VehicleFinancingAgent,
            'consortium': ConsortiumAgent,
            
            # TELECOMUNICAÇÕES
            'internet': InternetAgent,
            'mobile': TelecomAgent,  # Usar geral por enquanto
            'tv_subscription': TVSubscriptionAgent,
            
            # SAÚDE
            'health_insurance': HealthInsuranceAgent,
            'life_insurance': LifeInsuranceAgent,
            
            # ENERGIA
            'electricity': TelecomAgent,  # Usar geral telecom por similaridade regulatória
            'gas_supply': TelecomAgent,
            
            # TRANSPORTE
            'vehicle_insurance': VehicleInsuranceAgent,
            'vehicle_rental': RentalAgent,
            
            # EDUCAÇÃO
            'higher_education': FinancialAgent,  # Aspectos contratuais similares
            'professional_course': FinancialAgent,
            
            # TRABALHO
            'employment_clt': EmploymentCLTAgent,
            'service_contract': FinancialAgent,
            
            # CONSUMO
            'ecommerce': FinancialAgent,  # CDC similar
            'subscription_service': TelecomAgent,  # Similar a telecom
            
            # GERAL (fallback)
            'general': FinancialAgent  # Usar agente financeiro como geral (mais completo)
        }
    
    def classify_and_create_agent(self, text: str, question: str = "") -> Dict[str, Any]:
        """
        Classifica automaticamente e retorna informações do agente + resposta
        
        Args:
            text: Texto do contrato (se disponível)  
            question: Pergunta do usuário
            
        Returns:
            Dict com classificação, agente e resposta
        """
        
        # Usar tanto texto do contrato quanto pergunta para classificação
        classification_text = f"{text} {question}".strip()
        
        # Classificar automaticamente
        classification_result = self.classifier.classify_contract(classification_text)
        
        # Obter classe do agente
        agent_type = classification_result['agent_type']
        agent_class = self._agent_registry.get(agent_type, FinancialAgent)
        
        # Criar instância do agente
        agent_instance = agent_class()
        
        # Gerar resposta especializada
        response = agent_instance.generate_response(question, text)
        
        return {
            # Informações da classificação
            'classification': classification_result['classification'],
            'agent_type': agent_type,
            'confidence': classification_result['confidence'],
            'matched_keywords': classification_result.get('matched_keywords', []),
            'is_automatic': classification_result['is_automatic'],
            'method': classification_result['method'],
            
            # Informações do agente
            'agent_name': getattr(agent_instance, 'specialization', 'Assistente Geral'),
            'agent_icon': getattr(agent_instance, 'icon', '🤖'),
            
            # Resposta gerada
            'response': response,
            'question': question,
            'has_context': bool(text and text.strip())
        }
    
    def get_agent_by_type(self, agent_type: str) -> Optional[BaseContractAgent]:
        """Retorna instância de agente específico por tipo"""
        agent_class = self._agent_registry.get(agent_type)
        if agent_class:
            return agent_class()
        return None
    
    def get_all_available_agents(self) -> Dict[str, Dict[str, Any]]:
        """Retorna informações sobre todos os agentes disponíveis"""
        agents_info = {}
        
        for agent_type, agent_class in self._agent_registry.items():
            try:
                agent_instance = agent_class()
                agents_info[agent_type] = {
                    'name': getattr(agent_instance, 'specialization', agent_type),
                    'icon': getattr(agent_instance, 'icon', '🤖'),
                    'class': agent_class.__name__
                }
            except Exception as e:
                agents_info[agent_type] = {
                    'name': agent_type.title(),
                    'icon': '🤖', 
                    'class': agent_class.__name__,
                    'error': str(e)
                }
        
        return agents_info
    
    def get_classification_info(self, text: str) -> Dict[str, Any]:
        """Retorna apenas informações de classificação sem criar agente"""
        return self.classifier.classify_contract(text)

# Instância global para uso em toda aplicação
agent_factory = IntelligentAgentFactory()