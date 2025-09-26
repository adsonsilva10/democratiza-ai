from typing import Dict, Any, List
import json
from app.agents.base_agent import BaseContractAgent, ContractAnalysis

class RentalAgent(BaseContractAgent):
    """Specialized agent for rental/lease contract analysis with entity context support"""
    
    def __init__(self, claude_client, rag_service, db_session=None):
        super().__init__(claude_client, rag_service, db_session)
        self.agent_type = "locacao"
        self.specialization = "Locação Residencial"
        self.icon = "🏠"
    
    async def analyze_contract(self, contract_text: str, context: Dict[str, Any] = None) -> ContractAnalysis:
        """Analyze rental contract with specialized knowledge and entity context"""
        
        # Perform entity analysis first
        entity_info = self.entity_classifier.identify_entities(contract_text)
        
        # Get enriched RAG context
        enriched_context = await self.get_enriched_context(
            contract_text, 
            analysis_type="rental_analysis"
        )
        
        # Format context for prompt
        rag_context = self._format_context_for_prompt(enriched_context)
        
        # Get entity-specific context
        entity_context = self._get_entity_context_for_prompt(entity_info)
        
        # Create specialized prompt with entity context
        prompt = self.get_specialized_prompt(contract_text, rag_context, entity_context)
        
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
    
    def _get_entity_context_for_prompt(self, entity_info) -> str:
        """Generate entity-specific context for rental analysis"""
        
        if not entity_info:
            return ""
        
        if entity_info.consumer_protection:
            # B2C Rental - Individual renting from company/professional landlord
            return """
            CONTEXTO JURÍDICO ESPECÍFICO - LOCAÇÃO B2C:
            - PROTEÇÃO DO CONSUMIDOR: Este contrato está sujeito ao CDC (Código de Defesa do Consumidor)
            - LOCATÁRIO PESSOA FÍSICA: Aplicar proteções especiais ao inquilino consumidor
            - LOCADOR EMPRESARIAL: Maior responsabilidade sobre informações e cláusulas
            - CLÁUSULAS ABUSIVAS: Verificar rigorosamente cláusulas que limitem direitos do locatário
            - FORO COMPETENTE: Deve ser o domicílio do consumidor (locatário)
            - TRANSPARÊNCIA: Todas as informações sobre custos devem ser claras e adequadas
            - GARANTIAS: Não podem ser excessivas ou desproporcionais
            """
        elif entity_info.party_relationship == "b2b":
            # B2B Rental - Company to company
            return """
            CONTEXTO JURÍDICO ESPECÍFICO - LOCAÇÃO COMERCIAL B2B:
            - RELAÇÃO EMPRESARIAL: Paridade entre as partes contraentes
            - LIBERDADE CONTRATUAL: Maior autonomia para negociar condições especiais
            - FORO DE ELEIÇÃO: Válido se não prejudicar o equilíbrio contratual
            - GARANTIAS: Podem ser proporcionais ao porte e risco do negócio
            - CLÁUSULAS ESPECIAIS: Permitidas cláusulas comerciais específicas
            - ONEROSIDADE: Possibilidade de revisão por mudanças econômicas significativas
            """
        elif entity_info.party_relationship == "p2p":
            # P2P Rental - Individual to individual
            return """
            CONTEXTO JURÍDICO ESPECÍFICO - LOCAÇÃO ENTRE PARTICULARES:
            - CÓDIGO CIVIL: Relação regida pelo direito civil e Lei do Inquilinato
            - BOA-FÉ OBJETIVA: Princípio fundamental nas obrigações
            - EQUILÍBRIO: Verificar se obrigações estão equilibradas
            - GARANTIAS: Devem ser proporcionais e razoáveis
            - FUNÇÃO SOCIAL: Contrato deve cumprir função social
            - VULNERABILIDADE: Proteger a parte mais vulnerável economicamente
            """
        else:
            return """
            CONTEXTO JURÍDICO GERAL - LOCAÇÃO:
            - Aplicação da Lei do Inquilinato (8.245/91) e Código Civil
            - Verificar equilíbrio entre direitos e deveres das partes
            - Analisar proporcionalidade de garantias e obrigações
            """
    
    def get_specialized_prompt(self, contract_text: str, rag_context: str = "", entity_context: str = "") -> str:
        """Get rental-specific analysis prompt with entity awareness"""
        
        base_intro = "Você é um especialista em contratos de locação imobiliária no Brasil. Analise o seguinte contrato de locação considerando a legislação brasileira (Lei do Inquilinato - Lei 8.245/91) e práticas do mercado."
        
        # Add entity-specific context if available
        if entity_context:
            intro = f"{base_intro}\n\n{entity_context}"
        else:
            intro = base_intro
        
        return f"""
        {intro}

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
    
    def _format_context_for_prompt(self, enriched_context: Dict[str, Any]) -> str:
        """Format enriched RAG context for use in prompts"""
        
        if isinstance(enriched_context, str):
            return enriched_context  # Fallback for legacy format
        
        formatted_context = ""
        
        # Add legal framework
        if enriched_context.get("legal_framework"):
            formatted_context += "## LEGISLAÇÃO APLICÁVEL:\n"
            for law in enriched_context["legal_framework"]:
                formatted_context += f"- {law['source']}: {law['content']}\n"
            formatted_context += "\n"
        
        # Add jurisprudence
        if enriched_context.get("jurisprudence"):
            formatted_context += "## JURISPRUDÊNCIA:\n"
            for case in enriched_context["jurisprudence"]:
                formatted_context += f"- {case['source']}: {case['content']}\n"
            formatted_context += "\n"
        
        # Add recommendations
        if enriched_context.get("recommendations"):
            formatted_context += "## DIRETRIZES ESPECIALIZADAS:\n"
            for rec in enriched_context["recommendations"]:
                formatted_context += f"- {rec['title']}: {rec['content']}\n"
            formatted_context += "\n"
        
        return formatted_context
    
    async def analyze_specific_clause(self, clause_text: str, clause_type: str) -> Dict[str, Any]:
        """Analyze a specific rental contract clause with legal precedents"""
        
        # Get legal precedents for this clause
        precedents = await self.get_legal_precedents(f"{clause_type} {clause_text}")
        
        # Build analysis context
        context = f"Cláusula: {clause_text}\n\nTipo: {clause_type}\n\n"
        
        if precedents:
            context += "PRECEDENTES LEGAIS:\n"
            for precedent in precedents:
                context += f"- {precedent['court']}: {precedent['content'][:200]}...\n"
        
        prompt = f"""
        Analise esta cláusula específica de contrato de locação:

        {context}

        Forneça uma análise detalhada considerando:
        1. Legalidade da cláusula
        2. Riscos para o locatário
        3. Riscos para o locador
        4. Precedentes jurisprudenciais aplicáveis
        5. Recomendações de alteração

        Responda em formato JSON:
        {{
            "legality": "legal|questionável|ilegal",
            "tenant_risks": ["risco1", "risco2"],
            "landlord_risks": ["risco1", "risco2"],
            "legal_basis": "base legal aplicável",
            "recommendations": ["recomendação1", "recomendação2"],
            "severity": "alta|média|baixa"
        }}
        """
        
        try:
            response = await self.claude_client.completions.create(
                model="claude-3-sonnet-20240229",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.1
            )
            
            return json.loads(response.content[0].text.strip())
            
        except Exception as e:
            return {
                "legality": "questionável",
                "tenant_risks": ["Análise indisponível devido a erro técnico"],
                "landlord_risks": [],
                "legal_basis": "Não disponível",
                "recommendations": ["Solicitar análise manual"],
                "severity": "média"
            }
    
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Generate specialized rental response with entity context awareness"""
        
        # Analyze entities if contract text is provided
        entity_info = None
        if contract_text:
            entity_info = self.entity_classifier.identify_entities(contract_text)
        
        if not question:
            base_response = """🏠 **Locação Residencial - Análise Especializada**

Olá! Sou especialista em contratos de locação imobiliária. Posso ajudar com:

**📋 Principais Análises:**
• Valores de aluguel e reajustes
• Garantias e cauções exigidas
• Cláusulas de rescisão e multas
• Responsabilidades de conservação
• Direitos e deveres do locatário

**⚠️ Pontos Críticos Comuns:**
• Valores de caução excessivos
• Cláusulas de reajuste abusivas
• Multas desproporcionais
• Transferência inadequada de responsabilidades

**⚖️ Base Legal:**
Lei do Inquilinato (8.245/91) + Código Civil"""

            # Add entity-specific information if available
            if entity_info:
                if entity_info.consumer_protection:
                    base_response += """

**🛡️ PROTEÇÃO ESPECIAL - B2C:**
Este contrato está sujeito ao CDC. Como locatário consumidor, você tem:
• Proteção contra cláusulas abusivas
• Direito a informações claras e adequadas
• Foro competente no seu domicílio
• Garantias proporcionais e razoáveis"""
                elif entity_info.party_relationship == "b2b":
                    base_response += """

**🏢 LOCAÇÃO COMERCIAL - B2B:**
Relação entre empresas com maior liberdade contratual:
• Negociação paritária de condições
• Cláusulas comerciais específicas permitidas
• Garantias adequadas ao porte empresarial
• Foro de eleição válido"""
                elif entity_info.party_relationship == "p2p":
                    base_response += """

**👥 LOCAÇÃO ENTRE PARTICULARES - P2P:**
Relação civil regida pelo Código Civil:
• Princípio da boa-fé objetiva
• Equilíbrio entre direitos e deveres
• Função social do contrato
• Proteção da parte mais vulnerável"""
            
            return base_response + "\n\nComo posso ajudar com sua situação específica?"
        
        # Handle specific questions with entity context
        question_lower = question.lower()
        
        # Add entity context to responses
        entity_context = ""
        if entity_info and entity_info.consumer_protection:
            entity_context = "\n\n**⚖️ Contexto Jurídico:** Como este é um contrato B2C (empresa→pessoa física), aplicam-se as proteções do CDC além da Lei do Inquilinato."
        elif entity_info and entity_info.party_relationship == "b2b":
            entity_context = "\n\n**⚖️ Contexto Jurídico:** Como este é um contrato B2B (empresa→empresa), há maior liberdade contratual, mas deve haver equilíbrio entre as partes."
        elif entity_info and entity_info.party_relationship == "p2p":
            entity_context = "\n\n**⚖️ Contexto Jurídico:** Como este é um contrato entre particulares, aplicam-se os princípios do Código Civil e boa-fé objetiva."
        
        # Return base response with context
        base_response = "🏠 **Locação - Orientação Especializada**\n\n"
        base_response += f"Sobre sua pergunta: \"{question}\"\n\n"
        base_response += "Posso ajudar com análise detalhada de contratos de locação considerando:\n"
        base_response += "• Lei do Inquilinato (8.245/91)\n"
        base_response += "• Código de Defesa do Consumidor (quando aplicável)\n"  
        base_response += "• Jurisprudência específica sobre locações\n"
        base_response += entity_context
        
        return base_response
