from typing import Dict, Any
from app.agents.classifier_agent import ClassifierAgent
from app.agents.rental_agent import RentalAgent
from app.agents.telecom_agent import TelecomAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.base_agent import BaseContractAgent

class AgentFactory:
    """Factory for creating specialized contract analysis agents"""
    
    def __init__(self, claude_client, rag_service, db_session=None):
        self.claude_client = claude_client
        self.rag_service = rag_service
        self.db_session = db_session
        self.classifier = ClassifierAgent(claude_client, rag_service)
        
        # Agent registry
        self._agents = {
            "locacao": RentalAgent,
            "telecom": TelecomAgent,
            "financeiro": FinancialAgent,
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
