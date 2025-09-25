from typing import Dict, Any, Optional
from app.agents.classifier_agent import ClassifierAgent
from app.agents.intelligent_factory import agent_factory as intelligent_agent_factory
from app.agents.base_agent import BaseContractAgent

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
            "vehicle_financing": FinancialAgent,
            "consortium": FinancialAgent,
            
            # TELECOMUNICAÇÕES
            "telecom": TelecomAgent,  # Backward compatibility
            "internet": InternetAgent,
            "mobile": TelecomAgent,
            "tv_subscription": TelecomAgent,
            
            # SAÚDE & SEGUROS
            "health_insurance": HealthInsuranceAgent,
            "life_insurance": FinancialAgent,
            "vehicle_insurance": VehicleInsuranceAgent,
            
            # ENERGIA
            "electricity": TelecomAgent,
            "gas_supply": TelecomAgent,
            
            # TRANSPORTE
            "vehicle_rental": RentalAgent,
            
            # EDUCAÇÃO
            "higher_education": FinancialAgent,
            "professional_course": FinancialAgent,
            
            # TRABALHO
            "employment_clt": EmploymentCLTAgent,
            "service_contract": FinancialAgent,
            
            # CONSUMO
            "ecommerce": FinancialAgent,
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
    
    def register_agent(self, contract_type: str, agent_class: type):
        """Register a new agent type"""
        self._agents[contract_type] = agent_class
