from typing import Dict, Any, List
import json
from app.agents.base_agent import BaseContractAgent, ContractAnalysis
from app.services.cnpj_service import CNPJService

class TelecomAgent(BaseContractAgent):
    """Specialized agent for telecommunications contract analysis"""
    
    def __init__(self, claude_client, rag_service):
        super().__init__(claude_client, rag_service)
        self.cnpj_service = CNPJService()
        self.agent_type = "telecom"
    
    async def analyze_contract(self, contract_text: str, context: Dict[str, Any] = None) -> ContractAnalysis:
        """Analyze telecom contract with specialized knowledge"""
        
        # 1. Análise de CNPJ da empresa prestadora
        cnpj = self.cnpj_service.extract_cnpj_from_text(contract_text)
        company_analysis = None
        if cnpj:
            company_data = await self.cnpj_service.get_company_data(cnpj)
            company_analysis = self.cnpj_service.analyze_company_risk(
                company_data, 
                {"contract_type": "telecom"}
            )
        
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
            
            # Integrar análise da empresa (CNPJ) se disponível
            if company_analysis:
                # Adicionar riscos da empresa aos riscos do contrato
                company_risk_factors = []
                for risk_factor in company_analysis.get("risk_factors", []):
                    company_risk_factors.append({
                        "type": "empresa_prestadora",
                        "description": risk_factor,
                        "severity": "high" if company_analysis["risk_level"] == "high" else "medium",
                        "clause": "Dados da empresa prestadora",
                        "recommendation": "; ".join(company_analysis.get("recommendations", []))
                    })
                
                # Combinar risk factors
                all_risk_factors = analysis_data.get("risk_factors", []) + company_risk_factors
                
                # Ajustar nível de risco geral se empresa tem problema
                contract_risk_level = self._calculate_risk_level(analysis_data.get("risk_factors", []))
                if company_analysis["risk_level"] == "high":
                    final_risk_level = "Alto Risco"
                elif company_analysis["risk_level"] == "medium" and contract_risk_level != "Alto Risco":
                    final_risk_level = "Médio Risco"
                else:
                    final_risk_level = contract_risk_level
                
                # Adicionar informações da empresa ao summary
                company_info = company_analysis.get("company_info", {})
                enhanced_summary = f"{analysis_data.get('summary', '')}\n\n📋 EMPRESA: {company_info.get('razao_social', 'N/A')} | Situação: {company_info.get('situacao', 'N/A')} | Porte: {company_info.get('porte', 'N/A')}"
                
            else:
                all_risk_factors = analysis_data.get("risk_factors", [])
                final_risk_level = self._calculate_risk_level(analysis_data.get("risk_factors", []))
                enhanced_summary = analysis_data.get("summary", "")
            
            return ContractAnalysis(
                contract_type="telecom",
                risk_level=final_risk_level,
                summary=enhanced_summary,
                key_findings=analysis_data.get("key_findings", []),
                risk_factors=all_risk_factors,
                recommendations=analysis_data.get("recommendations", []),
                clauses_analysis=analysis_data.get("clauses_analysis", []),
                confidence_score=analysis_data.get("confidence_score", 0.0)
            )
            
        except Exception as e:
            # Fallback analysis
            return self._create_fallback_analysis(contract_text, str(e))
    
    def get_specialized_prompt(self, contract_text: str, rag_context: str = "") -> str:
        """Get telecom-specific analysis prompt"""
        
        return f"""
        Você é um especialista em contratos de telecomunicações no Brasil. Analise o seguinte contrato considerando a regulamentação da ANATEL, Lei Geral de Telecomunicações (Lei 9.472/97), Marco Civil da Internet e direitos do consumidor.

        Contexto de conhecimento especializado:
        {rag_context}

        Contrato para análise:
        {contract_text}

        Analise os seguintes aspectos específicos de contratos de telecomunicações:

        1. **Planos e velocidades**: Verificar se as velocidades prometidas são claras e realistas
        2. **Franquia de dados**: Limites de uso e consequências do excesso
        3. **Fidelização**: Períodos de carência e multas por rescisão
        4. **Qualidade do serviço**: SLA, disponibilidade e compensações
        5. **Cobrança**: Valores, taxas adicionais e formas de pagamento
        6. **Instalação**: Custos, prazos e responsabilidades
        7. **Suporte técnico**: Canais de atendimento e prazos de resposta
        8. **Rescisão**: Procedimentos e custos para cancelamento
        9. **Alterações contratuais**: Como e quando podem ser feitas
        10. **Privacidade de dados**: Uso e proteção de dados pessoais (LGPD)

        Identifique cláusulas abusivas segundo CDC e regulamentação ANATEL.

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
                    "analysis": "análise regulatória",
                    "risk_level": "alto|médio|baixo",
                    "legal_basis": "base legal/regulatória aplicável"
                }}
            ],
            "confidence_score": 0.95
        }}
        """
    
    def _create_fallback_analysis(self, contract_text: str, error: str) -> ContractAnalysis:
        """Create basic analysis when Claude fails"""
        
        # Basic keyword-based analysis for telecom
        high_risk_keywords = ["fidelidade", "multa", "velocidade mínima", "bloqueio"]
        medium_risk_keywords = ["franquia", "taxa de instalação", "reajuste"]
        
        contract_lower = contract_text.lower()
        
        risk_factors = []
        for keyword in high_risk_keywords:
            if keyword in contract_lower:
                risk_factors.append({
                    "type": "clausula_telecom",
                    "description": f"Identificada menção a {keyword}",
                    "severity": "high",
                    "clause": f"Contém termo: {keyword}",
                    "recommendation": "Verificar com ANATEL"
                })
        
        return ContractAnalysis(
            contract_type="telecom",
            risk_level=self._calculate_risk_level(risk_factors),
            summary="Análise básica por falha na análise especializada",
            key_findings=["Análise limitada por erro técnico"],
            risk_factors=risk_factors,
            recommendations=["Solicitar análise completa novamente"],
            clauses_analysis=[],
            confidence_score=0.3
        )
