from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel
from app.agents.entity_classifier import EntityClassifier, EntityInfo

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
        # Initialize entity classifier for CPF/CNPJ analysis
        self.entity_classifier = EntityClassifier()
    
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
    
    async def analyze_contract_with_entity_context(self, contract_text: str, 
                                                  context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enhanced analysis that considers entity types (CPF/CNPJ) and legal framework
        """
        # Identify entities first
        entity_info = self.entity_classifier.identify_entities(contract_text)
        
        # Perform base analysis
        base_analysis = await self.analyze_contract(contract_text, context)
        
        # Enhance analysis with entity-specific considerations
        enhanced_analysis = self._enhance_with_entity_context(base_analysis, entity_info)
        
        return enhanced_analysis
    
    def _enhance_with_entity_context(self, base_analysis: ContractAnalysis, 
                                   entity_info: EntityInfo) -> Dict[str, Any]:
        """Apply entity-specific legal analysis"""
        
        enhanced = base_analysis.dict()
        
        # Add entity context
        enhanced["entity_analysis"] = {
            "relationship_type": entity_info.party_relationship,
            "consumer_protection": entity_info.consumer_protection,
            "legal_framework": entity_info.legal_framework,
            "applicable_rights": self.entity_classifier.get_applicable_rights(entity_info),
            "confidence_score": entity_info.confidence_score,
            "identified_entities": entity_info.identified_entities
        }
        
        # Adjust risk assessment based on entity type
        if entity_info.consumer_protection:
            # B2C: More protective analysis focusing on consumer rights
            enhanced["risk_factors"] = self._enhance_b2c_risks(enhanced.get("risk_factors", []))
            enhanced["legal_context"] = "B2C - Proteção do Consumidor (CDC)"
        elif entity_info.party_relationship == "b2b":
            # B2B: Focus on commercial fairness and balance
            enhanced["risk_factors"] = self._enhance_b2b_risks(enhanced.get("risk_factors", []))
            enhanced["legal_context"] = "B2B - Relação Comercial (Código Civil + Comercial)"
        elif entity_info.party_relationship == "p2p":
            # P2P: Focus on civil law principles
            enhanced["risk_factors"] = self._enhance_p2p_risks(enhanced.get("risk_factors", []))
            enhanced["legal_context"] = "P2P - Relação Civil (Código Civil)"
        else:
            enhanced["legal_context"] = "Genérico - Análise Padrão"
        
        # Add entity-specific recommendations
        enhanced["recommendations"] = self._enhance_recommendations(
            enhanced.get("recommendations", []), entity_info
        )
        
        return enhanced
    
    def _enhance_b2c_risks(self, base_risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhanced risk analysis for B2C contracts (CDC protection)"""
        enhanced_risks = base_risks.copy()
        
        # Add CDC-specific risk checks
        b2c_specific_risks = [
            {
                "factor": "Cláusulas abusivas (art. 51 CDC)",
                "severity": "high", 
                "description": "Verificar se há cláusulas que limitam direitos básicos do consumidor",
                "legal_basis": "Art. 51 CDC"
            },
            {
                "factor": "Direito de arrependimento",
                "severity": "medium",
                "description": "Analisar se contrato à distância respeita prazo de 7 dias",
                "legal_basis": "Art. 49 CDC"
            },
            {
                "factor": "Informação adequada",
                "severity": "medium", 
                "description": "Confirmar se informações são claras e adequadas",
                "legal_basis": "Art. 6º, III CDC"
            },
            {
                "factor": "Foro de eleição",
                "severity": "high",
                "description": "Verificar se foro eleito prejudica acesso à justiça do consumidor",
                "legal_basis": "Art. 101 CDC"
            }
        ]
        
        enhanced_risks.extend(b2c_specific_risks)
        return enhanced_risks
    
    def _enhance_b2b_risks(self, base_risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhanced risk analysis for B2B contracts (commercial law)"""
        enhanced_risks = base_risks.copy()
        
        # Add B2B-specific risk checks
        b2b_specific_risks = [
            {
                "factor": "Equilíbrio contratual",
                "severity": "medium",
                "description": "Verificar se há desequilíbrio excessivo entre as partes",
                "legal_basis": "Princípio da boa-fé objetiva"
            },
            {
                "factor": "Cláusulas penais",
                "severity": "medium",
                "description": "Analisar proporcionalidade de multas e penalidades",
                "legal_basis": "Art. 412-413 CC"
            },
            {
                "factor": "Limitação de responsabilidade",
                "severity": "low",
                "description": "Verificar validade de limitações consensuais",
                "legal_basis": "Art. 927 CC"
            },
            {
                "factor": "Eleição de foro",
                "severity": "low",
                "description": "Confirmar validade da cláusula de foro",
                "legal_basis": "Art. 63 CPC"
            }
        ]
        
        enhanced_risks.extend(b2b_specific_risks)
        return enhanced_risks
    
    def _enhance_p2p_risks(self, base_risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhanced risk analysis for P2P contracts (civil law)"""
        enhanced_risks = base_risks.copy()
        
        # Add P2P-specific risk checks
        p2p_specific_risks = [
            {
                "factor": "Boa-fé objetiva",
                "severity": "medium",
                "description": "Verificar se contrato respeita princípios de boa-fé",
                "legal_basis": "Art. 422 CC"
            },
            {
                "factor": "Função social do contrato",
                "severity": "medium", 
                "description": "Analisar se contrato cumpre função social",
                "legal_basis": "Art. 421 CC"
            },
            {
                "factor": "Onerosidade excessiva",
                "severity": "low",
                "description": "Verificar riscos de onerosidade superveniente",
                "legal_basis": "Art. 478-480 CC"
            }
        ]
        
        enhanced_risks.extend(p2p_specific_risks)
        return enhanced_risks
    
    def _enhance_recommendations(self, base_recommendations: List[str], 
                               entity_info: EntityInfo) -> List[str]:
        """Add entity-specific recommendations"""
        enhanced_recommendations = base_recommendations.copy()
        
        if entity_info.consumer_protection:
            enhanced_recommendations.extend([
                "Verificar se todas as informações sobre o produto/serviço são claras e adequadas",
                "Confirmar que não há cláusulas que limitam direitos básicos do consumidor", 
                "Atentar para direito de arrependimento em contratos à distância (7 dias)",
                "Verificar se foro eleito não prejudica acesso à justiça do consumidor"
            ])
        elif entity_info.party_relationship == "b2b":
            enhanced_recommendations.extend([
                "Negociar cláusulas de forma paritária considerando interesses mútuos",
                "Verificar adequação de garantias e penalidades ao porte das empresas",
                "Considerar inserção de cláusulas de revisão contratual",
                "Avaliar necessidade de limitação consensual de responsabilidade"
            ])
        elif entity_info.party_relationship == "p2p":
            enhanced_recommendations.extend([
                "Certificar que obrigações estão equilibradas entre as partes",
                "Incluir cláusulas de resolução amigável de conflitos",
                "Prever situações de onerosidade excessiva superveniente",
                "Garantir clareza sobre direitos e deveres de cada parte"
            ])
        
        return enhanced_recommendations
