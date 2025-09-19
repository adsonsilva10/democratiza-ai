from typing import Dict, Any, List
import json
from app.agents.base_agent import BaseContractAgent, ContractAnalysis

class FinancialAgent(BaseContractAgent):
    """Specialized agent for financial contract analysis"""
    
    def __init__(self, claude_client, rag_service):
        super().__init__(claude_client, rag_service)
        self.agent_type = "financeiro"
    
    async def analyze_contract(self, contract_text: str, context: Dict[str, Any] = None) -> ContractAnalysis:
        """Analyze financial contract with specialized knowledge"""
        
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
                contract_type="financeiro",
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
        """Get financial-specific analysis prompt"""
        
        return f"""
        Você é um especialista em contratos financeiros no Brasil. Analise o seguinte contrato considerando a regulamentação do Banco Central (BACEN), Conselho Monetário Nacional (CMN), Código de Defesa do Consumidor e legislação específica do setor financeiro.

        Contexto de conhecimento especializado:
        {rag_context}

        Contrato para análise:
        {contract_text}

        Analise os seguintes aspectos específicos de contratos financeiros:

        1. **Taxa de juros**: Verificar se estão dentro dos limites legais e market standards
        2. **CET (Custo Efetivo Total)**: Transparência na divulgação de todos os custos
        3. **Garantias**: Tipos exigidos e proporcionalidade
        4. **Seguros**: Obrigatoriedade e custos
        5. **Amortização**: Sistema utilizado (SAC, Price, etc.) e impactos
        6. **Vencimento antecipado**: Condições que permitem cobrança integral
        7. **Comissão de permanência**: Aplicação e limitações legais
        8. **Taxas e tarifas**: Legalidade e transparência das cobranças
        9. **Quitação antecipada**: Direitos do devedor e desconto proporcional
        10. **Renegociação**: Condições para refinanciamento
        11. **Dados pessoais**: Uso em bureaus de crédito e proteção (LGPD)
        12. **Execução**: Procedimentos em caso de inadimplência

        Identifique cláusulas abusivas segundo CDC e normativas BACEN.

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
                    "analysis": "análise financeira/jurídica",
                    "risk_level": "alto|médio|baixo",
                    "legal_basis": "base legal/normativa aplicável"
                }}
            ],
            "confidence_score": 0.95
        }}
        """
    
    def _create_fallback_analysis(self, contract_text: str, error: str) -> ContractAnalysis:
        """Create basic analysis when Claude fails"""
        
        # Basic keyword-based analysis for financial contracts
        high_risk_keywords = ["taxa abusiva", "anatocismo", "comissão permanência", "execução sumária"]
        medium_risk_keywords = ["juros", "multa", "seguro", "cet"]
        
        contract_lower = contract_text.lower()
        
        risk_factors = []
        for keyword in high_risk_keywords:
            if keyword in contract_lower:
                risk_factors.append({
                    "type": "clausula_financeira",
                    "description": f"Identificada menção a {keyword}",
                    "severity": "high",
                    "clause": f"Contém termo: {keyword}",
                    "recommendation": "Consultar especialista financeiro"
                })
        
        return ContractAnalysis(
            contract_type="financeiro",
            risk_level=self._calculate_risk_level(risk_factors),
            summary="Análise básica por falha na análise especializada",
            key_findings=["Análise limitada por erro técnico"],
            risk_factors=risk_factors,
            recommendations=["Solicitar análise completa novamente"],
            clauses_analysis=[],
            confidence_score=0.3
        )
