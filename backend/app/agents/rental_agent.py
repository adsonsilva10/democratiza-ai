from typing import Dict, Any, List
import json
from app.agents.base_agent import BaseContractAgent, ContractAnalysis

class RentalAgent(BaseContractAgent):
    """Specialized agent for rental/lease contract analysis"""
    
    def __init__(self, claude_client, rag_service):
        super().__init__(claude_client, rag_service)
        self.agent_type = "locacao"
    
    async def analyze_contract(self, contract_text: str, context: Dict[str, Any] = None) -> ContractAnalysis:
        """Analyze rental contract with specialized knowledge"""
        
        # Get relevant RAG context
        rag_context = await self.get_rag_context(contract_text)
        
        # Create specialized prompt
        prompt = self.get_specialized_prompt(contract_text, rag_context)
        
        try:
            response = await self.claude_client.completions.create(
                model="claude-3-sonnet-20240229",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.1
            )
            
            # Parse structured response
            analysis_data = json.loads(response.content[0].text.strip())
            
            return ContractAnalysis(
                contract_type="locacao",
                risk_level=self._calculate_risk_level(analysis_data.get("risk_factors", [])),
                summary=analysis_data.get("summary", ""),
                key_findings=analysis_data.get("key_findings", []),
                risk_factors=analysis_data.get("risk_factors", []),
                recommendations=analysis_data.get("recommendations", []),
                clauses_analysis=analysis_data.get("clauses_analysis", []),
                confidence_score=analysis_data.get("confidence_score", 0.0)
            )
            
        except Exception as e:
            # Fallback analysis
            return self._create_fallback_analysis(contract_text, str(e))
    
    def get_specialized_prompt(self, contract_text: str, rag_context: str = "") -> str:
        """Get rental-specific analysis prompt"""
        
        return f"""
        Você é um especialista em contratos de locação imobiliária no Brasil. Analise o seguinte contrato de locação considerando a legislação brasileira (Lei do Inquilinato - Lei 8.245/91) e práticas do mercado.

        Contexto de conhecimento especializado:
        {rag_context}

        Contrato para análise:
        {contract_text}

        Analise os seguintes aspectos específicos de contratos de locação:

        1. **Valor do aluguel e reajustes**: Verificar se os valores e índices de reajuste estão adequados
        2. **Caução e garantias**: Analisar tipos de garantia exigidos e valores
        3. **Prazo de locação**: Verificar se está de acordo com a Lei do Inquilinato
        4. **Responsabilidades de conservação**: Distribuição entre locador e locatário
        5. **Cláusulas de rescisão**: Condições para término antecipado
        6. **Multas e penalidades**: Verificar se estão dentro dos limites legais
        7. **Reformas e benfeitorias**: Direitos e obrigações
        8. **Sublocação**: Permissões e restrições
        9. **IPTU e taxas**: Responsabilidade pelo pagamento
        10. **Vistoria**: Procedimentos de entrada e saída

        Identifique cláusulas potencialmente abusivas segundo o CDC e Lei do Inquilinato.

        Responda APENAS com um JSON válido no seguinte formato:
        {{
            "summary": "Resumo executivo do contrato",
            "key_findings": ["achado1", "achado2", "achado3"],
            "risk_factors": [
                {{
                    "type": "tipo_do_risco",
                    "description": "descrição detalhada",
                    "severity": "high|medium|low",
                    "clause": "cláusula específica",
                    "recommendation": "recomendação específica"
                }}
            ],
            "recommendations": ["recomendação1", "recomendação2"],
            "clauses_analysis": [
                {{
                    "clause": "texto da cláusula",
                    "analysis": "análise jurídica",
                    "risk_level": "alto|médio|baixo",
                    "legal_basis": "base legal aplicável"
                }}
            ],
            "confidence_score": 0.95
        }}
        """
    
    def _create_fallback_analysis(self, contract_text: str, error: str) -> ContractAnalysis:
        """Create basic analysis when Claude fails"""
        
        # Basic keyword-based analysis
        high_risk_keywords = ["multa", "penalidade", "rescisão", "caução alta"]
        medium_risk_keywords = ["reajuste", "reforma", "sublocação"]
        
        contract_lower = contract_text.lower()
        
        risk_factors = []
        for keyword in high_risk_keywords:
            if keyword in contract_lower:
                risk_factors.append({
                    "type": "clausula_identificada",
                    "description": f"Identificada menção a {keyword}",
                    "severity": "high",
                    "clause": f"Contém termo: {keyword}",
                    "recommendation": "Revisar com especialista"
                })
        
        return ContractAnalysis(
            contract_type="locacao",
            risk_level=self._calculate_risk_level(risk_factors),
            summary="Análise básica por falha na análise especializada",
            key_findings=["Análise limitada por erro técnico"],
            risk_factors=risk_factors,
            recommendations=["Solicitar análise completa novamente"],
            clauses_analysis=[],
            confidence_score=0.3
        )
