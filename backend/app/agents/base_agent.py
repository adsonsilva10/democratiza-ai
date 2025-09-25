from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class ContractAnalysis(BaseModel):
    """Standard contract analysis response format"""
    contract_type: str
    risk_level: str  # "Alto Risco", "Médio Risco", "Baixo Risco"
    summary: str
    key_findings: List[str]
    risk_factors: List[Dict[str, Any]]
    recommendations: List[str]
    clauses_analysis: List[Dict[str, Any]]
    confidence_score: float

class BaseContractAgent(ABC):
    """Base class for all contract analysis agents with RAG integration"""
    
    def __init__(self, claude_client, rag_service, db_session=None):
        self.claude_client = claude_client
        self.rag_service = rag_service
        self.db = db_session
        self.agent_type = self.__class__.__name__.replace("Agent", "").lower()
    
    @abstractmethod
    async def analyze_contract(self, contract_text: str, context: Dict[str, Any] = None) -> ContractAnalysis:
        """Analyze a contract and return structured results"""
        pass
    
    @abstractmethod
    def get_specialized_prompt(self, contract_text: str, rag_context: str = "") -> str:
        """Get the specialized prompt for this agent type"""
        pass
    
    async def get_enriched_context(self, contract_text: str, analysis_type: str = "analysis") -> Dict[str, Any]:
        """Get enriched context from RAG knowledge base"""
        if not self.db:
            # Fallback to basic search
            return await self.get_rag_context(contract_text)
        
        # Use advanced RAG context building
        context = await self.rag_service.build_context_for_agent(
            query=contract_text[:1000],  # First 1000 chars for context
            contract_type=self.agent_type,
            context_type=analysis_type,
            max_context_length=4000,
            db=self.db
        )
        
        return context
    
    async def get_rag_context(self, contract_text: str) -> str:
        """Retrieve relevant context from RAG knowledge base (legacy method)"""
        # Extract key terms for RAG search
        search_terms = await self._extract_search_terms(contract_text)
        
        # Query RAG service for relevant context
        rag_results = await self.rag_service.search(
            query=" ".join(search_terms),
            contract_type=self.agent_type,
            limit=5,
            db=self.db
        )
        
        return "\n".join([result["content"] for result in rag_results])
    
    async def get_legal_precedents(self, contract_clause: str) -> List[Dict[str, Any]]:
        """Get legal precedents for specific contract clauses"""
        if not self.db:
            return []
        
        return await self.rag_service.get_legal_precedents(
            contract_clause=contract_clause,
            contract_type=self.agent_type,
            limit=3,
            db=self.db
        )
    
    async def _extract_search_terms(self, contract_text: str) -> List[str]:
        """Extract relevant search terms for RAG queries"""
        # This would typically use NER or keyword extraction
        # For now, return basic terms
        return contract_text.split()[:20]  # First 20 words as search terms
    
    def _calculate_risk_level(self, risk_factors: List[Dict[str, Any]]) -> str:
        """Calculate overall risk level based on individual risk factors"""
        high_risk_count = len([f for f in risk_factors if f.get("severity") == "high"])
        medium_risk_count = len([f for f in risk_factors if f.get("severity") == "medium"])
        
        if high_risk_count >= 2:
            return "Alto Risco"
        elif high_risk_count >= 1 or medium_risk_count >= 3:
            return "Médio Risco"
        else:
            return "Baixo Risco"
