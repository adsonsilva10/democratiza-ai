"""
Democratiza AI - Roteador Inteligente de LLMs
Analisa complexidade do contrato e roteia para o modelo mais eficiente
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import re
import asyncio
from datetime import datetime

class ComplexityLevel(Enum):
    """Níveis de complexidade de contratos"""
    SIMPLES = "simples"
    MEDIO = "medio" 
    COMPLEXO = "complexo"
    ESPECIALIZADO = "especializado"

class LLMProvider(Enum):
    """Provedores de LLM disponíveis"""
    GEMINI_FLASH = "gemini_flash"       # Ultra-barato - triagem rápida
    GROQ_LLAMA = "groq_llama"           # Mais barato - contratos simples
    GEMINI_PRO = "gemini_pro"           # Econômico - contratos médios
    ANTHROPIC_HAIKU = "anthropic_haiku" # Custo médio - contratos médios
    ANTHROPIC_SONNET = "anthropic_sonnet" # Alto custo - contratos complexos
    ANTHROPIC_OPUS = "anthropic_opus"   # Máximo custo - casos especializados

@dataclass
class LLMConfig:
    """Configuração de cada modelo LLM"""
    provider: LLMProvider
    model_name: str
    cost_per_1k_tokens: float  # Custo em USD por 1k tokens
    max_context: int           # Tamanho máximo do contexto
    best_for: List[str]        # Tipos de contrato ideais
    speed: str                 # fast, medium, slow
    quality: str               # basic, good, excellent

class ContractComplexityAnalyzer:
    """Analisador de complexidade de contratos"""
    
    def __init__(self):
        # Palavras-chave que indicam complexidade
        self.complexity_indicators = {
            ComplexityLevel.ESPECIALIZADO: [
                'previdência', 'aposentadoria', 'benefício', 'pecúlio',
                'fusão', 'aquisição', 'incorporação', 'cisão',
                'propriedade intelectual', 'patente', 'marca',
                'joint venture', 'consórcio', 'sociedade em conta de participação',
                'derivativos', 'swap', 'opções', 'futuros',
                'securitização', 'factoring', 'leasing financeiro'
            ],
            
            ComplexityLevel.COMPLEXO: [
                'cláusula penal', 'multa compensatória', 'perdas e danos',
                'rescisão unilateral', 'resolução', 'resilição',
                'força maior', 'caso fortuito', 'hardship',
                'arbitragem', 'mediação', 'foro de eleição',
                'garantia real', 'hipoteca', 'penhor', 'alienação fiduciária',
                'cessão de crédito', 'novação', 'sub-rogação',
                'sociedade limitada', 'sociedade anônima', 'MEI'
            ],
            
            ComplexityLevel.MEDIO: [
                'prestação de serviços', 'fornecimento', 'distribuição',
                'representação comercial', 'agência', 'franquia',
                'locação comercial', 'locação residencial',
                'compra e venda', 'mútuo', 'comodato',
                'seguro', 'financiamento', 'empréstimo',
                'trabalho', 'estágio', 'terceirização'
            ],
            
            ComplexityLevel.SIMPLES: [
                'assinatura', 'mensalidade', 'plano básico',
                'serviço simples', 'produto', 'delivery',
                'streaming', 'aplicativo', 'básico'
            ]
        }
        
        # Padrões que aumentam complexidade
        self.complexity_patterns = {
            'clausulas_multiplas': r'Art\.|Cláusula|Parágrafo.*?§',
            'valores_monetarios': r'R\$\s*[\d,.]+',
            'prazos_multiplos': r'\d+\s*(dias?|meses?|anos?)',
            'referencias_legais': r'Lei\s*n?º?\s*[\d.]+|Código\s*Civil|CDC',
            'formulas_complexas': r'[\+\-\*/]\s*\d+%|[a-zA-Z]+\s*=\s*[a-zA-Z\d\+\-\*/]+',
            'multiplas_partes': r'CONTRATANTE|CONTRATADO|INTERVENIENTE|ANUENTE'
        }

    def analyze_complexity(self, contract_text: str, contract_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analisa a complexidade de um contrato
        
        Args:
            contract_text: Texto do contrato
            contract_metadata: Metadados adicionais (tipo, valor, etc.)
            
        Returns:
            Dict com análise de complexidade
        """
        text_lower = contract_text.lower()
        
        # Contadores de complexidade
        complexity_scores = {level: 0 for level in ComplexityLevel}
        found_indicators = {level: [] for level in ComplexityLevel}
        
        # 1. Análise por palavras-chave
        for level, keywords in self.complexity_indicators.items():
            for keyword in keywords:
                if keyword in text_lower:
                    complexity_scores[level] += 1
                    found_indicators[level].append(keyword)
        
        # 2. Análise por padrões estruturais
        pattern_scores = {}
        for pattern_name, pattern in self.complexity_patterns.items():
            matches = re.findall(pattern, contract_text, re.IGNORECASE)
            pattern_scores[pattern_name] = len(matches)
        
        # 3. Análise de tamanho e estrutura
        text_length = len(contract_text)
        word_count = len(contract_text.split())
        paragraph_count = len(contract_text.split('\n\n'))
        
        # 4. Score baseado em metadados
        metadata_complexity = 0
        if contract_metadata:
            # Valor do contrato
            contract_value = contract_metadata.get('valor', 0)
            if contract_value > 1000000:  # > 1M
                metadata_complexity += 2
            elif contract_value > 100000:  # > 100K
                metadata_complexity += 1
            
            # Duração do contrato
            duration = contract_metadata.get('duracao_meses', 0)
            if duration > 60:  # > 5 anos
                metadata_complexity += 2
            elif duration > 12:  # > 1 ano
                metadata_complexity += 1
        
        # 5. Cálculo de complexidade final
        total_specialized = complexity_scores[ComplexityLevel.ESPECIALIZADO] * 4
        total_complex = complexity_scores[ComplexityLevel.COMPLEXO] * 3
        total_medium = complexity_scores[ComplexityLevel.MEDIO] * 2
        total_simple = complexity_scores[ComplexityLevel.SIMPLES] * 1
        
        # Score estrutural
        structural_score = 0
        if word_count > 5000:
            structural_score += 3
        elif word_count > 2000:
            structural_score += 2
        elif word_count > 500:
            structural_score += 1
        
        # Score de padrões
        pattern_score = sum(min(score, 3) for score in pattern_scores.values())
        
        # Score total
        total_score = (
            total_specialized + total_complex + 
            total_medium + total_simple + 
            structural_score + pattern_score + 
            metadata_complexity
        )
        
        # Determinação do nível final
        if total_specialized >= 1 or total_score >= 15:
            final_level = ComplexityLevel.ESPECIALIZADO
        elif total_complex >= 2 or total_score >= 10:
            final_level = ComplexityLevel.COMPLEXO  
        elif total_medium >= 2 or total_score >= 5:
            final_level = ComplexityLevel.MEDIO
        else:
            final_level = ComplexityLevel.SIMPLES
        
        return {
            'complexity_level': final_level,
            'total_score': total_score,
            'breakdown': {
                'specialized_score': total_specialized,
                'complex_score': total_complex,
                'medium_score': total_medium,
                'simple_score': total_simple,
                'structural_score': structural_score,
                'pattern_score': pattern_score,
                'metadata_score': metadata_complexity
            },
            'found_indicators': found_indicators,
            'pattern_analysis': pattern_scores,
            'document_stats': {
                'word_count': word_count,
                'character_count': text_length,
                'paragraph_count': paragraph_count
            },
            'reasoning': self._get_complexity_reasoning(
                final_level, found_indicators, pattern_scores, total_score
            )
        }
    
    def _get_complexity_reasoning(
        self, 
        level: ComplexityLevel, 
        indicators: Dict[ComplexityLevel, List[str]],
        patterns: Dict[str, int],
        score: int
    ) -> str:
        """Gera explicação da classificação de complexidade"""
        
        reasons = []
        
        if indicators[ComplexityLevel.ESPECIALIZADO]:
            reasons.append(f"Termos especializados detectados: {', '.join(indicators[ComplexityLevel.ESPECIALIZADO][:3])}")
        
        if indicators[ComplexityLevel.COMPLEXO]:
            reasons.append(f"Cláusulas complexas: {', '.join(indicators[ComplexityLevel.COMPLEXO][:3])}")
        
        if patterns['referencias_legais'] > 0:
            reasons.append(f"{patterns['referencias_legais']} referências legais")
        
        if patterns['valores_monetarios'] > 2:
            reasons.append("Múltiplos valores monetários")
        
        if patterns['clausulas_multiplas'] > 10:
            reasons.append("Estrutura jurídica complexa")
        
        return '; '.join(reasons) if reasons else f"Score total: {score}"

class LLMRouter:
    """Roteador principal de LLMs baseado em complexidade"""
    
    def __init__(self):
        self.complexity_analyzer = ContractComplexityAnalyzer()
        
        # Configurações dos modelos disponíveis
        self.llm_configs = {
            LLMProvider.GEMINI_FLASH: LLMConfig(
                provider=LLMProvider.GEMINI_FLASH,
                model_name="gemini-1.5-flash",
                cost_per_1k_tokens=0.00015,  # $0.00015 por 1k tokens - ULTRA BARATO
                max_context=1000000,  # 1M tokens
                best_for=["triagem inicial", "contratos padronizados", "análise rápida"],
                speed="very_fast",
                quality="good"
            ),
            
            LLMProvider.GEMINI_PRO: LLMConfig(
                provider=LLMProvider.GEMINI_PRO,
                model_name="gemini-1.5-pro",
                cost_per_1k_tokens=0.0035,  # $0.0035 por 1k tokens
                max_context=2000000,  # 2M tokens
                best_for=["contratos médios", "locação", "análise balanceada"],
                speed="fast",
                quality="very_good"
            ),
            
            LLMProvider.GROQ_LLAMA: LLMConfig(
                provider=LLMProvider.GROQ_LLAMA,
                model_name="llama-3.1-70b-versatile",
                cost_per_1k_tokens=0.0005,  # $0.0005 por 1k tokens
                max_context=32000,
                best_for=["contratos simples", "análise básica", "classificação"],
                speed="fast",
                quality="good"
            ),
            
            LLMProvider.ANTHROPIC_HAIKU: LLMConfig(
                provider=LLMProvider.ANTHROPIC_HAIKU,
                model_name="claude-3-haiku-20240307",
                cost_per_1k_tokens=0.0015,  # $0.0015 por 1k tokens
                max_context=200000,
                best_for=["contratos médios", "análise jurídica", "relatórios"],
                speed="medium",
                quality="good"
            ),
            
            LLMProvider.ANTHROPIC_SONNET: LLMConfig(
                provider=LLMProvider.ANTHROPIC_SONNET,
                model_name="claude-3-5-sonnet-20240620",
                cost_per_1k_tokens=0.015,   # $0.015 por 1k tokens
                max_context=200000,
                best_for=["contratos complexos", "análise detalhada", "riscos"],
                speed="medium",
                quality="excellent"
            ),
            
            LLMProvider.ANTHROPIC_OPUS: LLMConfig(
                provider=LLMProvider.ANTHROPIC_OPUS,
                model_name="claude-3-opus-20240229",
                cost_per_1k_tokens=0.075,   # $0.075 por 1k tokens
                max_context=200000,
                best_for=["casos especializados", "previdência", "M&A"],
                speed="slow",
                quality="excellent"
            )
        }
        
        # Mapeamento complexidade -> modelo (estratégia híbrida otimizada)
        self.complexity_to_model = {
            ComplexityLevel.SIMPLES: LLMProvider.GEMINI_FLASH,      # Ultra-econômico
            ComplexityLevel.MEDIO: LLMProvider.GEMINI_PRO,          # Econômico + qualidade
            ComplexityLevel.COMPLEXO: LLMProvider.ANTHROPIC_SONNET, # Qualidade superior
            ComplexityLevel.ESPECIALIZADO: LLMProvider.ANTHROPIC_OPUS # Máxima qualidade
        }
        
        # Estatísticas de uso
        self.usage_stats = {
            'total_requests': 0,
            'requests_by_model': {provider: 0 for provider in LLMProvider},
            'total_cost_saved': 0.0,
            'cost_by_model': {provider: 0.0 for provider in LLMProvider}
        }

    async def analyze_complexity(self, contract_text: str, contract_metadata: Dict[str, Any] = None) -> ComplexityLevel:
        """Analisa a complexidade de um contrato"""
        analysis = self.complexity_analyzer.analyze_complexity(contract_text, contract_metadata)
        return analysis['complexity_level']

    async def route_to_best_model(self, contract_text: str, contract_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Roteia para o melhor modelo baseado na complexidade"""
        complexity_analysis = self.complexity_analyzer.analyze_complexity(contract_text, contract_metadata)
        complexity_level = complexity_analysis['complexity_level']
        
        selected_model = self._select_optimal_model(complexity_level, contract_metadata or {})
        config = self.llm_configs[selected_model]
        
        return {
            'provider': selected_model,
            'model': config.model_name,
            'complexity': complexity_level.value,
            'cost_per_1k': config.cost_per_1k_tokens,
            'reasoning': complexity_analysis.get('reasoning', '')
        }

    async def route_contract_analysis(
        self, 
        contract_text: str, 
        contract_metadata: Dict[str, Any] = None,
        force_model: Optional[LLMProvider] = None,
        analysis_type: str = "full"
    ) -> Dict[str, Any]:
        """
        Roteia análise de contrato para o modelo mais adequado
        
        Args:
            contract_text: Texto do contrato
            contract_metadata: Metadados do contrato
            force_model: Forçar uso de modelo específico
            analysis_type: Tipo de análise (quick, standard, full, detailed)
            
        Returns:
            Dict com roteamento e análise
        """
        
        start_time = datetime.now()
        
        # 1. Análise de complexidade
        complexity_analysis = self.complexity_analyzer.analyze_complexity(
            contract_text, contract_metadata
        )
        
        complexity_level = complexity_analysis['complexity_level']
        
        # 2. Determinar modelo baseado na complexidade e tipo de análise
        if force_model:
            selected_model = force_model
            reason = "Modelo forçado pelo usuário"
        else:
            selected_model = self._select_optimal_model(
                complexity_level, analysis_type, len(contract_text)
            )
            reason = "Seleção automática baseada em complexidade"
        
        # 3. Configuração do modelo selecionado
        model_config = self.llm_configs[selected_model]
        
        # 4. Estimativa de custo
        estimated_tokens = self._estimate_tokens(contract_text, analysis_type)
        estimated_cost = (estimated_tokens / 1000) * model_config.cost_per_1k_tokens
        
        # 5. Comparação de custo com modelo mais caro
        opus_cost = (estimated_tokens / 1000) * self.llm_configs[LLMProvider.ANTHROPIC_OPUS].cost_per_1k_tokens
        cost_saved = opus_cost - estimated_cost
        
        # 6. Atualizar estatísticas
        self.usage_stats['total_requests'] += 1
        self.usage_stats['requests_by_model'][selected_model] += 1
        self.usage_stats['cost_by_model'][selected_model] += estimated_cost
        self.usage_stats['total_cost_saved'] += cost_saved
        
        routing_result = {
            'selected_model': selected_model,
            'model_config': model_config,
            'complexity_analysis': complexity_analysis,
            'routing_decision': {
                'reason': reason,
                'complexity_level': complexity_level.value,
                'analysis_type': analysis_type,
                'selection_time_ms': (datetime.now() - start_time).total_seconds() * 1000
            },
            'cost_analysis': {
                'estimated_tokens': estimated_tokens,
                'estimated_cost_usd': round(estimated_cost, 4),
                'cost_vs_opus': round(cost_saved, 4),
                'savings_percentage': round((cost_saved / opus_cost) * 100, 1) if opus_cost > 0 else 0
            },
            'recommendations': self._get_routing_recommendations(
                complexity_level, selected_model, estimated_cost
            )
        }
        
        return routing_result
    
    def _select_optimal_model(
        self, 
        complexity: ComplexityLevel, 
        analysis_type: str, 
        text_length: int
    ) -> LLMProvider:
        """Seleciona o modelo mais adequado baseado em múltiplos fatores"""
        
        # Modelo base pela complexidade
        base_model = self.complexity_to_model[complexity]
        
        # Ajustes baseados no tipo de análise
        if analysis_type == "quick":
            # Para análise rápida, usar modelo mais barato se possível
            if complexity == ComplexityLevel.MEDIO:
                return LLMProvider.GROQ_LLAMA
            elif complexity == ComplexityLevel.COMPLEXO:
                return LLMProvider.ANTHROPIC_HAIKU
        
        elif analysis_type == "detailed":
            # Para análise detalhada, usar modelo superior
            if complexity == ComplexityLevel.SIMPLES:
                return LLMProvider.ANTHROPIC_HAIKU
            elif complexity == ComplexityLevel.MEDIO:
                return LLMProvider.ANTHROPIC_SONNET
        
        # Ajuste baseado no tamanho do texto
        if text_length > 50000:  # Textos muito grandes
            if base_model == LLMProvider.GROQ_LLAMA:
                return LLMProvider.ANTHROPIC_HAIKU  # Melhor para contextos longos
        
        return base_model
    
    def _estimate_tokens(self, text: str, analysis_type: str) -> int:
        """Estima quantidade de tokens necessários"""
        
        # Estimativa básica: ~4 caracteres por token
        input_tokens = len(text) // 4
        
        # Tokens de output baseados no tipo de análise
        output_tokens = {
            'quick': 500,
            'standard': 1500, 
            'full': 3000,
            'detailed': 5000
        }.get(analysis_type, 1500)
        
        return input_tokens + output_tokens
    
    def _get_routing_recommendations(
        self,
        complexity: ComplexityLevel,
        selected_model: LLMProvider,
        estimated_cost: float
    ) -> List[str]:
        """Gera recomendações sobre o roteamento"""
        
        recommendations = []
        
        if complexity == ComplexityLevel.SIMPLES and estimated_cost > 0.01:
            recommendations.append("💡 Considere análise 'quick' para contratos simples")
        
        if complexity == ComplexityLevel.ESPECIALIZADO:
            recommendations.append("⚖️ Contrato especializado detectado - usando modelo premium")
        
        if selected_model == LLMProvider.ANTHROPIC_OPUS:
            recommendations.append("💰 Alto custo - revisar se complexidade justifica")
        
        if selected_model == LLMProvider.GROQ_LLAMA:
            recommendations.append("⚡ Análise econômica e rápida selecionada")
        
        return recommendations
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso do roteador"""
        
        if self.usage_stats['total_requests'] == 0:
            return {"message": "Nenhuma requisição processada ainda"}
        
        avg_cost_per_request = sum(self.usage_stats['cost_by_model'].values()) / self.usage_stats['total_requests']
        
        model_distribution = {
            provider.value: {
                'requests': count,
                'percentage': round((count / self.usage_stats['total_requests']) * 100, 1),
                'total_cost': round(self.usage_stats['cost_by_model'][provider], 4)
            }
            for provider, count in self.usage_stats['requests_by_model'].items()
            if count > 0
        }
        
        return {
            'summary': {
                'total_requests': self.usage_stats['total_requests'],
                'total_cost_saved_usd': round(self.usage_stats['total_cost_saved'], 4),
                'average_cost_per_request': round(avg_cost_per_request, 4)
            },
            'model_distribution': model_distribution,
            'cost_efficiency': {
                'total_actual_cost': round(sum(self.usage_stats['cost_by_model'].values()), 4),
                'cost_if_all_opus': round(
                    self.usage_stats['total_requests'] * 0.075, 4
                ),
                'savings_percentage': round(
                    (self.usage_stats['total_cost_saved'] / 
                     (sum(self.usage_stats['cost_by_model'].values()) + self.usage_stats['total_cost_saved'])) * 100, 1
                )
            }
        }

# Factory function para criar instância do roteador
def create_llm_router() -> LLMRouter:
    """Cria instância configurada do roteador de LLMs"""
    return LLMRouter()