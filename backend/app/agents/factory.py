from typing import Dict, Any, Optional
from app.agents.classifier_agent import ClassifierAgent
from app.agents.intelligent_factory import agent_factory as intelligent_agent_factory
from app.agents.base_agent import BaseContractAgent
from app.legal.terms_of_service import terms_service, ServiceType, UserType
from app.legal.privacy_service import privacy_service, ProcessingPurpose

# Import all specialized agents
from app.agents.rental_agent import RentalAgent
from app.agents.rental_commercial_agent import RentalCommercialAgent
from app.agents.real_estate_agent import RealEstateAgent
from app.agents.personal_loan_agent import PersonalLoanAgent
from app.agents.health_insurance_agent import HealthInsuranceAgent
from app.agents.internet_agent import InternetAgent
from app.agents.telecom_agent import TelecomAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.vehicle_insurance_agent import VehicleInsuranceAgent
from app.agents.credit_card_agent import CreditCardAgent
from app.agents.employment_clt_agent import EmploymentCLTAgent
from app.agents.vehicle_financing_agent import VehicleFinancingAgent
from app.agents.consortium_agent import ConsortiumAgent
from app.agents.tv_subscription_agent import TVSubscriptionAgent
from app.agents.life_insurance_agent import LifeInsuranceAgent
from app.agents.energy_agent import EnergyAgent
from app.agents.mobile_agent import MobileAgent
from app.agents.education_agent import EducationAgent
from app.agents.ecommerce_agent import EcommerceAgent
from app.agents.gas_agent import GasAgent

class AgentFactory:
    """Factory for creating specialized contract analysis agents"""
    
    def __init__(self, claude_client, rag_service, db_session=None):
        self.claude_client = claude_client
        self.rag_service = rag_service
        self.db_session = db_session
        self.classifier = ClassifierAgent(claude_client, rag_service)
        
        # Extended agent registry with ALL specialized agents
        self._agents = {
            # HABITAÇÃO
            "locacao": RentalAgent,  # Backward compatibility
            "rental_residential": RentalAgent,
            "rental_commercial": RentalCommercialAgent,
            "real_estate": RealEstateAgent,
            "housing_financing": PersonalLoanAgent,
            
            # FINANCEIRO
            "financeiro": FinancialAgent,  # Backward compatibility  
            "personal_loan": PersonalLoanAgent,
            "credit_card": CreditCardAgent,
            "vehicle_financing": VehicleFinancingAgent,
            "consortium": ConsortiumAgent,
            
            # TELECOMUNICAÇÕES
            "telecom": TelecomAgent,  # Backward compatibility
            "internet": InternetAgent,
            "mobile": MobileAgent,
            "tv_subscription": TVSubscriptionAgent,
            
            # SAÚDE & SEGUROS
            "health_insurance": HealthInsuranceAgent,
            "life_insurance": LifeInsuranceAgent,
            "vehicle_insurance": VehicleInsuranceAgent,
            
            # ENERGIA
            "electricity": EnergyAgent,
            "gas_supply": GasAgent,
            
            # TRANSPORTE
            "vehicle_rental": RentalAgent,
            
            # EDUCAÇÃO
            "higher_education": EducationAgent,
            "professional_course": EducationAgent,
            
            # TRABALHO
            "employment_clt": EmploymentCLTAgent,
            "service_contract": FinancialAgent,
            
            # CONSUMO
            "ecommerce": EcommerceAgent,
            "subscription_service": TelecomAgent,
        }
    
    async def create_agent(self, contract_text: str) -> BaseContractAgent:
        """
        Classify contract and return appropriate specialized agent
        
        Args:
            contract_text: The contract text to analyze
            
        Returns:
            Specialized agent instance for the contract type
        """
        # First, classify the contract
        classification = await self.classifier.classify_contract(contract_text)
        contract_type = classification["contract_type"]
        
        # Create the appropriate specialized agent
        if contract_type in self._agents:
            agent_class = self._agents[contract_type]
            return agent_class(self.claude_client, self.rag_service, self.db_session)
        else:
            # Fallback to a generic agent or raise an error
            raise ValueError(f"No specialized agent available for contract type: {contract_type}")
    
    async def analyze_contract_intelligent(self, contract_text: str, question: str = "", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        NEW: Intelligent contract analysis with automatic detection
        Uses the new intelligent classifier for better accuracy
        
        Args:
            contract_text: The contract text to analyze
            question: User's specific question
            context: Additional context for analysis
            
        Returns:
            Complete analysis with intelligent classification and specialized response
        """
        try:
            # Use intelligent factory for automatic classification and response
            result = intelligent_agent_factory.classify_and_create_agent(
                text=contract_text,
                question=question
            )
            
            return {
                "classification": {
                    "contract_type": result['classification'],
                    "agent_type": result['agent_type'], 
                    "confidence": result['confidence'],
                    "method": result['method'],
                    "is_automatic": result['is_automatic'],
                    "matched_keywords": result.get('matched_keywords', [])
                },
                "agent_info": {
                    "name": result['agent_name'],
                    "icon": result['agent_icon'],
                    "type": result['agent_type']
                },
                "response": result['response'],
                "question": result['question'],
                "has_context": result['has_context'],
                "status": "success",
                "version": "intelligent_v1"
            }
            
        except Exception as e:
            return {
                "classification": None,
                "agent_info": None,
                "response": f"Erro na análise inteligente: {str(e)}",
                "status": "error",
                "error": str(e),
                "version": "intelligent_v1"
            }
    
    async def analyze_contract_intelligent_with_entities(self, contract_text: str, 
                                                       question: str = "", 
                                                       context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        NOVA: Análise inteligente completa com classificação de entidades (CPF/CNPJ)
        
        Identifica tanto o tipo de contrato quanto o tipo de entidade e aplica 
        o framework jurídico adequado (CDC para B2C, Código Civil para B2B/P2P)
        
        Args:
            contract_text: The contract text to analyze
            question: User's specific question
            context: Additional context for analysis
            
        Returns:
            Complete analysis with entity context and legal framework
        """
        try:
            # Use NEW intelligent factory with entity analysis
            result = intelligent_agent_factory.classify_and_create_agent_with_entities(
                text=contract_text,
                question=question
            )
            
            return {
                "classification": {
                    "contract_type": result['classification'],
                    "agent_type": result['agent_type'], 
                    "confidence": result['confidence'],
                    "method": result['method'],
                    "is_automatic": result['is_automatic'],
                    "matched_keywords": result.get('matched_keywords', [])
                },
                "entity_analysis": result.get('entity_analysis', {}),
                "legal_context": result.get('legal_context', 'Genérico'),
                "agent_specialization": result.get('agent_specialization', 'general'),
                "agent_info": {
                    "name": result['agent_name'],
                    "icon": result['agent_icon'],
                    "type": result['agent_type']
                },
                "response": result['response'],
                "question": result['question'],
                "has_context": result['has_context'],
                "has_question": result.get('has_question', False),
                "status": "success",
                "version": "intelligent_entities_v1"
            }
            
        except Exception as e:
            return {
                "classification": None,
                "entity_analysis": None,
                "legal_context": None,
                "agent_info": None,
                "response": f"Erro na análise inteligente com entidades: {str(e)}",
                "status": "error",
                "error": str(e),
                "version": "intelligent_entities_v1"
            }
    
    async def analyze_contract(self, contract_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Complete contract analysis workflow:
        1. Classify contract type
        2. Create specialized agent
        3. Perform analysis
        
        Args:
            contract_text: The contract text to analyze
            context: Additional context for analysis
            
        Returns:
            Complete analysis results including classification and detailed analysis
        """
        # Step 1: Classify the contract
        classification = await self.classifier.classify_contract(contract_text)
        
        # Step 2: Create specialized agent
        try:
            agent = await self.create_agent(contract_text)
            
            # Step 3: Perform specialized analysis
            analysis = await agent.analyze_contract(contract_text, context)
            
            return {
                "classification": classification,
                "analysis": analysis.dict(),
                "agent_type": agent.agent_type,
                "status": "success"
            }
            
        except ValueError as e:
            # Handle unsupported contract types
            return {
                "classification": classification,
                "analysis": None,
                "agent_type": None,
                "status": "error",
                "error": str(e),
                "message": "Tipo de contrato não suportado para análise especializada"
            }
        except Exception as e:
            # Handle other errors
            return {
                "classification": classification,
                "analysis": None,
                "agent_type": None,
                "status": "error",
                "error": str(e),
                "message": "Erro durante análise do contrato"
            }
    
    def get_supported_contract_types(self) -> list:
        """Get list of supported contract types"""
        return list(self._agents.keys())
    
    async def analyze_contract_ethically(self, 
                                       contract_text: str,
                                       user_id: str,
                                       user_type_str: str = "CPF",  # "CPF" ou "CNPJ"
                                       context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Ponto de entrada principal com conformidade ética completa
        
        Implementa todo o pipeline ético:
        1. Verificação de consentimento LGPD
        2. Classificação inteligente com entidades
        3. Análise por agente especializado 
        4. Auditoria de viés automatizada
        5. Aplicação de disclaimers legais
        """
        
        # Mapeia tipo de usuário para enum
        user_type = UserType.INDIVIDUAL_CPF if user_type_str == "CPF" else UserType.SMALL_BUSINESS_CNPJ
        
        # Verifica se requer consentimento explícito
        if terms_service.should_require_explicit_consent(ServiceType.CONTRACT_ANALYSIS, user_type):
            if not privacy_service.check_consent_valid(user_id, ProcessingPurpose.CONTRACT_ANALYSIS):
                return {
                    "requires_consent": True,
                    "consent_text": privacy_service._generate_consent_text([
                        ProcessingPurpose.CONTRACT_ANALYSIS,
                        ProcessingPurpose.SERVICE_PROVISION
                    ]),
                    "pre_analysis_warning": terms_service.get_pre_analysis_warning(user_type),
                    "user_type": user_type.value,
                    "status": "awaiting_consent"
                }
        
        # Executa análise inteligente com entidades
        try:
            result = await intelligent_agent_factory.analyze_contract_intelligent_with_entities(
                contract_text=contract_text,
                context=context or {}
            )
            
            if result.get("status") == "error":
                return result
            
            # Obtém o agente usado
            agent_type = result.get("agent_type")
            agent = self.create_agent(agent_type) if agent_type else None
            
            if agent and hasattr(agent, 'analyze_contract_with_ethics'):
                # Usa análise ética completa do agente
                ethical_result = await agent.analyze_contract_with_ethics(
                    contract_text=contract_text,
                    user_id=user_id,
                    user_type=user_type,
                    context=context
                )
                
                # Combina resultados
                result["ethical_analysis"] = ethical_result
                result["compliance_status"] = ethical_result.get("compliance_status", "approved")
                result["bias_audit"] = ethical_result.get("bias_audit")
                result["processing_record_id"] = ethical_result.get("processing_record_id")
            
            # Adiciona informações de conformidade
            result["user_type"] = user_type.value
            result["terms_version"] = terms_service.version
            result["privacy_compliant"] = True
            result["timestamp"] = privacy_service.datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Erro durante análise ética do contrato",
                "user_type": user_type.value,
                "timestamp": privacy_service.datetime.now().isoformat()
            }
    
    def record_user_consent(self, user_id: str, purposes: List[ProcessingPurpose],
                           ip_address: str = "", user_agent: str = "") -> Dict[str, Any]:
        """Registra consentimento do usuário"""
        try:
            consent_id = privacy_service.record_consent(
                user_id=user_id,
                purposes=purposes,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            return {
                "consent_id": consent_id,
                "status": "success",
                "message": "Consentimento registrado com sucesso",
                "purposes": [p.value for p in purposes],
                "timestamp": privacy_service.datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Erro ao registrar consentimento"
            }
    
    def get_user_data_summary(self, user_id: str) -> Dict[str, Any]:
        """Exporta dados do usuário para conformidade LGPD"""
        try:
            return privacy_service.export_user_data(user_id)
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Erro ao exportar dados do usuário"
            }
    
    def delete_user_data(self, user_id: str) -> Dict[str, Any]:
        """Exerce direito de eliminação do usuário"""
        try:
            return privacy_service.delete_user_data(user_id)
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "message": "Erro ao deletar dados do usuário"
            }
    
    def get_compliance_report(self) -> Dict[str, Any]:
        """Gera relatório completo de conformidade"""
        return {
            "terms_of_service": terms_service.export_terms_summary(),
            "privacy_compliance": privacy_service.generate_compliance_report(),
            "bias_audit": privacy_service.bias_auditor.export_audit_report(),
            "supported_agents": self.get_supported_contract_types(),
            "factory_version": "1.0.0-ethical",
            "generated_at": privacy_service.datetime.now().isoformat()
        }

    def register_agent(self, contract_type: str, agent_class: type):
        """Register a new agent type"""
        self._agents[contract_type] = agent_class
