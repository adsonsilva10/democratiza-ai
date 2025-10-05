"""
Democratiza AI - Serviço Inteligente de Análise de Contratos
Integra roteador de LLM com análise jurídica especializada
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass

from .llm_router import LLMRouter, ComplexityLevel
from .llm_client import UnifiedLLMService, LLMRequest, LLMResponse
from .rag_service import get_rag_service

@dataclass
class ContractAnalysisResult:
    """Resultado completo da análise de contrato"""
    contract_id: str
    analysis_summary: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    legal_insights: Dict[str, Any]
    recommendations: List[str]
    cost_breakdown: Dict[str, Any]
    processing_metadata: Dict[str, Any]

class ContractAnalysisService:
    """Serviço principal de análise de contratos com roteamento inteligente"""
    
    def __init__(self):
        self.llm_router = LLMRouter()
        self.llm_service = UnifiedLLMService()
        self.rag_service = get_rag_service()  # Lazy initialization
        
        # Templates de prompts especializados
        self.analysis_prompts = {
            'classification': self._get_classification_prompt(),
            'risk_analysis': self._get_risk_analysis_prompt(),
            'legal_review': self._get_legal_review_prompt(),
            'recommendations': self._get_recommendations_prompt()
        }
    
    async def analyze_contract(
        self,
        contract_text: str,
        contract_metadata: Optional[Dict[str, Any]] = None,
        analysis_depth: str = "standard",
        force_model: Optional[str] = None,
        include_rag: bool = True
    ) -> ContractAnalysisResult:
        """
        Análise completa de contrato com roteamento inteligente
        
        Args:
            contract_text: Texto do contrato
            contract_metadata: Metadados adicionais
            analysis_depth: quick, standard, detailed, comprehensive
            force_model: Forçar modelo específico
            include_rag: Incluir consulta à base de conhecimento
        """
        
        start_time = datetime.now()
        contract_id = f"contract_{int(datetime.now().timestamp())}"
        
        try:
            # 1. Roteamento inteligente
            routing_result = await self.llm_router.route_contract_analysis(
                contract_text=contract_text,
                contract_metadata=contract_metadata,
                analysis_type=analysis_depth
            )
            
            selected_provider = routing_result['selected_model']
            complexity_level = routing_result['complexity_analysis']['complexity_level']
            
            # 2. Consulta RAG se solicitado
            rag_context = ""
            if include_rag:
                rag_context = await self._get_rag_context(contract_text, complexity_level)
            
            # 3. Análise por etapas com prompts especializados
            analysis_results = {}
            
            # Etapa 1: Classificação e estrutura
            classification_result = await self._run_classification_analysis(
                contract_text, selected_provider, rag_context
            )
            analysis_results['classification'] = classification_result
            
            # Etapa 2: Análise de riscos
            risk_result = await self._run_risk_analysis(
                contract_text, selected_provider, rag_context, classification_result
            )
            analysis_results['risk_assessment'] = risk_result
            
            # Etapa 3: Revisão legal (apenas para contratos médios/complexos)
            if complexity_level in [ComplexityLevel.MEDIO, ComplexityLevel.COMPLEXO, ComplexityLevel.ESPECIALIZADO]:
                legal_result = await self._run_legal_review(
                    contract_text, selected_provider, rag_context, risk_result
                )
                analysis_results['legal_review'] = legal_result
            
            # Etapa 4: Recomendações
            recommendations_result = await self._run_recommendations_analysis(
                contract_text, selected_provider, analysis_results, rag_context
            )
            analysis_results['recommendations'] = recommendations_result
            
            # 4. Consolidação dos resultados
            consolidated_analysis = self._consolidate_analysis_results(analysis_results)
            
            # 5. Cálculo de custos total
            total_cost = sum([
                result.get('cost_usd', 0) for result in analysis_results.values()
                if isinstance(result, dict)
            ])
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ContractAnalysisResult(
                contract_id=contract_id,
                analysis_summary=consolidated_analysis['summary'],
                risk_assessment=consolidated_analysis['risk_assessment'],
                legal_insights=consolidated_analysis['legal_insights'],
                recommendations=consolidated_analysis['recommendations'],
                cost_breakdown={
                    'total_cost_usd': round(total_cost, 4),
                    'model_used': selected_provider.value,
                    'complexity_level': complexity_level.value,
                    'cost_breakdown_by_stage': {
                        stage: result.get('cost_usd', 0) 
                        for stage, result in analysis_results.items()
                        if isinstance(result, dict)
                    },
                    'estimated_savings': routing_result['cost_analysis']['cost_vs_opus']
                },
                processing_metadata={
                    'processing_time_seconds': round(processing_time, 2),
                    'complexity_analysis': routing_result['complexity_analysis'],
                    'routing_decision': routing_result['routing_decision'],
                    'rag_enabled': include_rag,
                    'analysis_depth': analysis_depth,
                    'total_tokens_used': sum([
                        result.get('tokens_used', {}).get('total', 0) 
                        for result in analysis_results.values()
                        if isinstance(result, dict) and 'tokens_used' in result
                    ])
                }
            )
        
        except Exception as e:
            # Log do erro e retorno de análise básica
            return self._create_fallback_analysis(
                contract_id, contract_text, str(e), start_time
            )
    
    async def _get_rag_context(self, contract_text: str, complexity: ComplexityLevel) -> str:
        """Obtém contexto relevante da base de conhecimento jurídico"""
        
        try:
            # Extrair termos-chave do contrato para busca
            key_terms = self._extract_legal_terms(contract_text)
            
            # Buscar documentos relevantes baseado na complexidade
            search_limit = {
                ComplexityLevel.SIMPLES: 2,
                ComplexityLevel.MEDIO: 3,
                ComplexityLevel.COMPLEXO: 4,
                ComplexityLevel.ESPECIALIZADO: 5
            }.get(complexity, 3)
            
            # Simulação da consulta RAG (implementar com rag_service real)
            rag_results = await self._mock_rag_search(key_terms, search_limit)
            
            return "\n\n".join([
                f"**{result['source']}**: {result['content'][:500]}..."
                for result in rag_results
            ])
        
        except Exception:
            return ""
    
    async def _run_classification_analysis(
        self, 
        contract_text: str, 
        provider, 
        rag_context: str
    ) -> Dict[str, Any]:
        """Análise de classificação e estrutura do contrato"""
        
        prompt = self.analysis_prompts['classification'].format(
            contract_text=contract_text[:4000],  # Limitar tamanho
            rag_context=rag_context[:2000] if rag_context else "Contexto não disponível"
        )
        
        request = LLMRequest(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.3
        )
        
        response = await self.llm_service.generate_response(provider, request)
        
        # Parse da resposta JSON
        try:
            parsed_result = json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback se não conseguir parsear JSON
            parsed_result = {
                "contract_type": "Indefinido",
                "main_parties": "Não identificado",
                "key_clauses": ["Análise indisponível"],
                "contract_value": "Não especificado",
                "duration": "Não especificado"
            }
        
        return {
            **parsed_result,
            'tokens_used': response.tokens_used,
            'cost_usd': response.cost_usd,
            'response_time_ms': response.response_time_ms
        }
    
    async def _run_risk_analysis(
        self, 
        contract_text: str, 
        provider, 
        rag_context: str,
        classification_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Análise detalhada de riscos"""
        
        contract_type = classification_result.get('contract_type', 'Genérico')
        
        prompt = self.analysis_prompts['risk_analysis'].format(
            contract_text=contract_text[:5000],
            contract_type=contract_type,
            rag_context=rag_context[:2000] if rag_context else "Contexto não disponível"
        )
        
        request = LLMRequest(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.2
        )
        
        response = await self.llm_service.generate_response(provider, request)
        
        # Parse da resposta
        try:
            parsed_result = json.loads(response.content)
        except json.JSONDecodeError:
            parsed_result = {
                "overall_risk_score": 50,
                "risk_level": "MÉDIO",
                "high_risk_clauses": [],
                "legal_compliance": "Parcial",
                "financial_risks": []
            }
        
        return {
            **parsed_result,
            'tokens_used': response.tokens_used,
            'cost_usd': response.cost_usd,
            'response_time_ms': response.response_time_ms
        }
    
    async def _run_legal_review(
        self, 
        contract_text: str, 
        provider, 
        rag_context: str,
        risk_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Revisão legal especializada"""
        
        prompt = self.analysis_prompts['legal_review'].format(
            contract_text=contract_text[:4000],
            risk_summary=json.dumps(risk_result, ensure_ascii=False)[:1000],
            rag_context=rag_context[:2000] if rag_context else ""
        )
        
        request = LLMRequest(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500,
            temperature=0.1
        )
        
        response = await self.llm_service.generate_response(provider, request)
        
        try:
            parsed_result = json.loads(response.content)
        except json.JSONDecodeError:
            parsed_result = {
                "legal_validity": "Válido com ressalvas",
                "regulatory_compliance": [],
                "jurisprudence_analysis": "Não disponível",
                "legal_precedents": []
            }
        
        return {
            **parsed_result,
            'tokens_used': response.tokens_used,
            'cost_usd': response.cost_usd,
            'response_time_ms': response.response_time_ms
        }
    
    async def _run_recommendations_analysis(
        self, 
        contract_text: str, 
        provider,
        analysis_results: Dict[str, Any],
        rag_context: str
    ) -> Dict[str, Any]:
        """Gera recomendações baseadas em toda a análise"""
        
        analysis_summary = {
            'classification': analysis_results.get('classification', {}),
            'risk_assessment': analysis_results.get('risk_assessment', {}),
            'legal_review': analysis_results.get('legal_review', {})
        }
        
        prompt = self.analysis_prompts['recommendations'].format(
            analysis_summary=json.dumps(analysis_summary, ensure_ascii=False)[:2000],
            rag_context=rag_context[:1000] if rag_context else ""
        )
        
        request = LLMRequest(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.4
        )
        
        response = await self.llm_service.generate_response(provider, request)
        
        try:
            parsed_result = json.loads(response.content)
        except json.JSONDecodeError:
            parsed_result = {
                "immediate_actions": ["Revisar análise detalhada"],
                "negotiation_points": ["Solicitar esclarecimentos"],
                "legal_advice": ["Consultar advogado se necessário"],
                "priority_level": "MÉDIA"
            }
        
        return {
            **parsed_result,
            'tokens_used': response.tokens_used,
            'cost_usd': response.cost_usd,
            'response_time_ms': response.response_time_ms
        }
    
    def _consolidate_analysis_results(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Consolida todos os resultados de análise em estrutura unificada"""
        
        classification = analysis_results.get('classification', {})
        risk_assessment = analysis_results.get('risk_assessment', {})
        legal_review = analysis_results.get('legal_review', {})
        recommendations = analysis_results.get('recommendations', {})
        
        return {
            'summary': {
                'contract_type': classification.get('contract_type', 'Não identificado'),
                'overall_risk_level': risk_assessment.get('risk_level', 'MÉDIO'),
                'risk_score': risk_assessment.get('overall_risk_score', 50),
                'legal_validity': legal_review.get('legal_validity', 'A analisar'),
                'main_parties': classification.get('main_parties', 'Não identificado'),
                'contract_value': classification.get('contract_value', 'Não especificado'),
                'duration': classification.get('duration', 'Não especificado')
            },
            'risk_assessment': {
                'high_risk_clauses': risk_assessment.get('high_risk_clauses', []),
                'financial_risks': risk_assessment.get('financial_risks', []),
                'legal_compliance': risk_assessment.get('legal_compliance', 'Parcial'),
                'regulatory_issues': legal_review.get('regulatory_compliance', [])
            },
            'legal_insights': {
                'key_clauses': classification.get('key_clauses', []),
                'legal_precedents': legal_review.get('legal_precedents', []),
                'jurisprudence_analysis': legal_review.get('jurisprudence_analysis', 'Não disponível')
            },
            'recommendations': {
                'immediate_actions': recommendations.get('immediate_actions', []),
                'negotiation_points': recommendations.get('negotiation_points', []),
                'legal_advice': recommendations.get('legal_advice', []),
                'priority_level': recommendations.get('priority_level', 'MÉDIA')
            }
        }
    
    def _create_fallback_analysis(
        self, 
        contract_id: str, 
        contract_text: str, 
        error_msg: str,
        start_time: datetime
    ) -> ContractAnalysisResult:
        """Cria análise de fallback em caso de erro"""
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ContractAnalysisResult(
            contract_id=contract_id,
            analysis_summary={
                'contract_type': 'Análise indisponível',
                'overall_risk_level': 'MÉDIO',
                'risk_score': 50,
                'error': error_msg
            },
            risk_assessment={
                'high_risk_clauses': ['Análise de risco indisponível devido a erro técnico'],
                'financial_risks': [],
                'legal_compliance': 'Não analisado'
            },
            legal_insights={
                'key_clauses': ['Análise jurídica indisponível'],
                'legal_precedents': [],
                'jurisprudence_analysis': 'Erro na análise'
            },
            recommendations=[
                'Revisar configuração do sistema',
                'Tentar análise novamente',
                'Consultar suporte técnico se problema persistir'
            ],
            cost_breakdown={
                'total_cost_usd': 0.0,
                'error': True
            },
            processing_metadata={
                'processing_time_seconds': round(processing_time, 2),
                'error': error_msg,
                'fallback_analysis': True
            }
        )
    
    async def _mock_rag_search(self, terms: List[str], limit: int) -> List[Dict[str, Any]]:
        """Mock da busca RAG (substituir pela implementação real)"""
        
        mock_results = [
            {
                'source': 'CDC Art. 51',
                'content': 'São nulas de pleno direito as cláusulas contratuais que estabeleçam obrigações consideradas iníquas, abusivas...',
                'category': 'consumer_protection'
            },
            {
                'source': 'Lei 8.245/91',
                'content': 'O locador é obrigado a entregar ao locatário o imóvel alugado em estado de servir ao uso...',
                'category': 'rental_law'
            },
            {
                'source': 'Código Civil',
                'content': 'A manifestação de vontade subsiste ainda que o seu autor haja feito a reserva mental...',
                'category': 'civil_contracts'
            }
        ]
        
        return mock_results[:limit]
    
    def _extract_legal_terms(self, contract_text: str) -> List[str]:
        """Extrai termos jurídicos relevantes do contrato"""
        
        import re
        
        legal_terms = [
            'locação', 'aluguel', 'previdência', 'aposentadoria', 
            'seguro', 'financiamento', 'prestação de serviços',
            'cláusula penal', 'multa', 'rescisão', 'garantia'
        ]
        
        found_terms = []
        text_lower = contract_text.lower()
        
        for term in legal_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _get_classification_prompt(self) -> str:
        """Template para análise de classificação"""
        return """
Analise o contrato abaixo e forneça uma classificação estruturada em formato JSON.

CONTRATO:
{contract_text}

CONTEXTO JURÍDICO:
{rag_context}

Forneça a resposta EXCLUSIVAMENTE em formato JSON válido com a seguinte estrutura:
{{
    "contract_type": "tipo do contrato (ex: Locação Residencial, Previdência Privada, etc)",
    "main_parties": "partes principais do contrato",
    "key_clauses": ["lista", "das", "principais", "cláusulas"],
    "contract_value": "valor do contrato ou 'Não especificado'",
    "duration": "prazo do contrato ou 'Não especificado'",
    "complexity_indicators": ["indicadores", "de", "complexidade"]
}}
"""
    
    def _get_risk_analysis_prompt(self) -> str:
        """Template para análise de riscos"""
        return """
Realize uma análise detalhada de riscos do contrato tipo "{contract_type}".

CONTRATO:
{contract_text}

CONTEXTO JURÍDICO:
{rag_context}

Analise os riscos e forneça resposta EXCLUSIVAMENTE em JSON válido:
{{
    "overall_risk_score": 0-100,
    "risk_level": "BAIXO|MÉDIO|ALTO|CRÍTICO",
    "high_risk_clauses": ["cláusula 1", "cláusula 2"],
    "legal_compliance": "Conforme|Parcial|Não conforme",
    "financial_risks": ["risco financeiro 1", "risco financeiro 2"],
    "consumer_protection_issues": ["questão 1", "questão 2"]
}}
"""
    
    def _get_legal_review_prompt(self) -> str:
        """Template para revisão legal"""
        return """
Realize uma revisão legal especializada considerando a legislação brasileira.

CONTRATO:
{contract_text}

ANÁLISE DE RISCOS PRÉVIA:
{risk_summary}

CONTEXTO JURÍDICO:
{rag_context}

Forneça análise legal EXCLUSIVAMENTE em JSON válido:
{{
    "legal_validity": "Válido|Válido com ressalvas|Inválido",
    "regulatory_compliance": ["norma 1", "norma 2"],
    "jurisprudence_analysis": "análise da jurisprudência aplicável",
    "legal_precedents": ["precedente 1", "precedente 2"],
    "constitutional_aspects": ["aspecto 1", "aspecto 2"]
}}
"""
    
    def _get_recommendations_prompt(self) -> str:
        """Template para recomendações"""
        return """
Com base na análise completa do contrato, forneça recomendações práticas.

RESUMO DA ANÁLISE:
{analysis_summary}

CONTEXTO JURÍDICO:
{rag_context}

Forneça recomendações EXCLUSIVAMENTE em JSON válido:
{{
    "immediate_actions": ["ação imediata 1", "ação imediata 2"],
    "negotiation_points": ["ponto de negociação 1", "ponto 2"],
    "legal_advice": ["conselho jurídico 1", "conselho 2"],
    "priority_level": "BAIXA|MÉDIA|ALTA|URGENTE",
    "next_steps": ["próximo passo 1", "próximo passo 2"]
}}
"""

# Instância global do serviço
contract_analysis_service = ContractAnalysisService()