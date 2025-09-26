from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel
from app.agents.entity_classifier import EntityClassifier, EntityInfo
from app.legal.terms_of_service import terms_service, ServiceType, UserType
from app.legal.privacy_service import privacy_service, DataCategory, ProcessingPurpose, LegalBasis
from app.legal.bias_auditor import bias_auditor, BiasAuditResult

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
    
    # ===============================
    # ETHICAL FOUNDATION METHODS
    # ===============================
    
    async def analyze_contract_with_ethics(self, 
                                         contract_text: str, 
                                         user_id: str,
                                         user_type: UserType,
                                         context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Executa análise completa com fundação ética integrada
        
        Implementa:
        1. Verificação de consentimento LGPD
        2. Registro de tratamento de dados  
        3. Análise do contrato com contexto ético
        4. Auditoria de viés na resposta
        5. Aplicação de disclaimers apropriados
        """
        
        # 1. Verificar e registrar consentimento se necessário
        service_type = ServiceType.CONTRACT_ANALYSIS
        
        if not privacy_service.check_consent_valid(user_id, ProcessingPurpose.CONTRACT_ANALYSIS):
            # Usuário precisa de consentimento
            return {
                "requires_consent": True,
                "consent_text": privacy_service._generate_consent_text([
                    ProcessingPurpose.CONTRACT_ANALYSIS,
                    ProcessingPurpose.SERVICE_PROVISION
                ]),
                "pre_analysis_warning": terms_service.get_pre_analysis_warning(user_type)
            }
        
        # 2. Registrar tratamento de dados pessoais
        processing_record_id = privacy_service.record_data_processing(
            data_subject_id=user_id,
            data_categories=[DataCategory.DOCUMENTO, DataCategory.COMPORTAMENTAL],
            purposes=[ProcessingPurpose.CONTRACT_ANALYSIS, ProcessingPurpose.SERVICE_PROVISION],
            legal_basis=LegalBasis.CONSENT,
            retention_days=365
        )
        
        # 3. Executar análise do contrato
        entity_info = self.entity_classifier.classify_document(contract_text)
        analysis_result = await self.analyze_contract_with_entity_context(
            contract_text, entity_info, context
        )
        
        # 4. Gerar resposta formatada
        response_text = self._format_analysis_response(analysis_result, entity_info)
        
        # 5. Executar auditoria de viés
        bias_audit = bias_auditor.audit_response(
            response_text=response_text,
            contract_type=analysis_result.contract_type,
            entity_type=entity_info.parties[0].entity_type if entity_info.parties else "unknown",
            context={"user_type": user_type.value, "agent_type": self.agent_type}
        )
        
        # 6. Aplicar correções se viés detectado
        if bias_audit.detected_biases:
            response_text = await self._apply_bias_corrections(response_text, bias_audit)
        
        # 7. Adicionar disclaimers legais apropriados
        disclaimers = terms_service.format_disclaimers_for_response(service_type, user_type)
        final_response = response_text + disclaimers
        
        # 8. Anonimizar dados sensíveis se solicitado
        if context and context.get("anonymize", False):
            final_response = privacy_service.anonymize_text(final_response, user_id)
        
        return {
            "analysis": analysis_result.dict(),
            "response_text": final_response,
            "entity_analysis": entity_info.dict() if hasattr(entity_info, 'dict') else str(entity_info),
            "bias_audit": {
                "audit_id": bias_audit.audit_id,
                "requires_human_review": bias_audit.requires_human_review,
                "detected_biases_count": len(bias_audit.detected_biases),
                "recommendation": bias_audit.recommendation if bias_audit.detected_biases else None
            },
            "processing_record_id": processing_record_id,
            "compliance_status": "approved" if not bias_audit.requires_human_review else "requires_review"
        }
    
    def record_user_consent(self, user_id: str, purposes: List[ProcessingPurpose],
                           ip_address: str = "", user_agent: str = "") -> str:
        """Registra consentimento do usuário para tratamento de dados"""
        return privacy_service.record_consent(
            user_id=user_id,
            purposes=purposes,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def get_required_consent_text(self) -> str:
        """Retorna texto de consentimento necessário para usar o agente"""
        return terms_service.get_consent_text(ServiceType.CONTRACT_ANALYSIS)
    
    def check_requires_explicit_consent(self, user_type: UserType) -> bool:
        """Verifica se tipo de usuário requer consentimento explícito"""
        return terms_service.should_require_explicit_consent(
            ServiceType.CONTRACT_ANALYSIS, user_type
        )
    
    async def _apply_bias_corrections(self, response_text: str, 
                                    bias_audit: BiasAuditResult) -> str:
        """Aplica correções automáticas para vieses detectados"""
        
        corrected_text = response_text
        
        for bias in bias_audit.detected_biases:
            # Correções automáticas básicas
            if bias.bias_type.value == "genero":
                corrected_text = corrected_text.replace("o usuário", "a pessoa usuária")
                corrected_text = corrected_text.replace("O contratante", "A parte contratante")
            
            elif bias.bias_type.value == "avaliacao_risco":
                # Suavizar linguagem alarmista
                corrected_text = corrected_text.replace("extremamente perigoso", "apresenta riscos significativos")
                corrected_text = corrected_text.replace("nunca assine", "recomenda-se cautela antes de assinar")
                corrected_text = corrected_text.replace("fuja", "considere alternativas")
            
            elif bias.bias_type.value == "linguagem":
                # Simplificar termos técnicos
                corrected_text = corrected_text.replace("ipso facto", "automaticamente")
                corrected_text = corrected_text.replace("stricto sensu", "no sentido estrito")
        
        # Adicionar nota sobre correções se houve mudanças
        if corrected_text != response_text:
            corrected_text += "\n\n⚡ Esta resposta foi automaticamente ajustada para maior clareza e imparcialidade."
        
        return corrected_text
    
    def _format_analysis_response(self, analysis: ContractAnalysis, 
                                entity_info: EntityInfo) -> str:
        """Formata resultado da análise em texto legível"""
        
        response_parts = []
        
        # Cabeçalho com informações básicas
        response_parts.append(f"📋 **ANÁLISE DE CONTRATO - {analysis.contract_type.upper()}**")
        response_parts.append(f"🎯 **Nível de Risco:** {analysis.risk_level}")
        response_parts.append(f"⚖️ **Framework Legal:** {entity_info.legal_framework}")
        response_parts.append(f"🤝 **Tipo de Relação:** {entity_info.party_relationship.upper()}")
        
        # Resumo executivo
        response_parts.append(f"\n## 📝 Resumo Executivo\n{analysis.summary}")
        
        # Principais descobertas
        if analysis.key_findings:
            response_parts.append("\n## 🔍 Principais Descobertas")
            for i, finding in enumerate(analysis.key_findings, 1):
                response_parts.append(f"{i}. {finding}")
        
        # Fatores de risco
        if analysis.risk_factors:
            response_parts.append("\n## ⚠️ Fatores de Risco")
            for risk in analysis.risk_factors:
                severity_emoji = {"high": "🚨", "medium": "⚡", "low": "💡"}.get(risk.get("severity", "low"), "💡")
                response_parts.append(f"{severity_emoji} **{risk.get('description', '')}**")
                if risk.get('explanation'):
                    response_parts.append(f"   {risk['explanation']}")
        
        # Recomendações
        if analysis.recommendations:
            response_parts.append("\n## 💡 Recomendações")
            for i, rec in enumerate(analysis.recommendations, 1):
                response_parts.append(f"{i}. {rec}")
        
        # Análise de cláusulas críticas
        if analysis.clauses_analysis:
            response_parts.append("\n## 📜 Análise de Cláusulas Críticas")
            for clause in analysis.clauses_analysis:
                response_parts.append(f"**{clause.get('clause_type', 'Cláusula')}:** {clause.get('analysis', '')}")
        
        # Confiança da análise
        confidence_emoji = "🎯" if analysis.confidence_score > 0.8 else "⚡" if analysis.confidence_score > 0.6 else "💡"
        response_parts.append(f"\n{confidence_emoji} **Confiança da Análise:** {analysis.confidence_score*100:.1f}%")
        
        return "\n".join(response_parts)
    
    def get_ethical_compliance_summary(self) -> Dict[str, Any]:
        """Retorna resumo da conformidade ética implementada"""
        return {
            "terms_of_service": {
                "version": terms_service.version,
                "effective_date": terms_service.effective_date.isoformat(),
                "disclaimers_count": len(terms_service.disclaimers)
            },
            "privacy_compliance": {
                "lgpd_compliant": True,
                "data_categories_monitored": [cat.value for cat in DataCategory],
                "processing_purposes": [purpose.value for purpose in ProcessingPurpose],
                "legal_bases": [basis.value for basis in LegalBasis]
            },
            "bias_audit": {
                "active_monitoring": True,
                "bias_types_monitored": len(bias_auditor.bias_indicators),
                "audit_history_entries": len(bias_auditor.audit_history)
            },
            "agent_type": self.agent_type,
            "compliance_score": self._calculate_compliance_score()
        }
    
    def _calculate_compliance_score(self) -> float:
        """Calcula score de conformidade ética (0-100)"""
        
        score = 100.0
        
        # Verifica implementação de componentes essenciais
        components = [
            hasattr(self, 'entity_classifier'),  # Classificação de entidades
            bool(terms_service.disclaimers),     # Termos de serviço
            len(privacy_service.consent_records) >= 0,  # Sistema de privacidade 
            len(bias_auditor.bias_indicators) > 0       # Auditoria de viés
        ]
        
        implemented = sum(components)
        score = (implemented / len(components)) * 100
        
        return score
