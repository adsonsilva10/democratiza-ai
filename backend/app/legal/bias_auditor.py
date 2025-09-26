"""
AI Bias Audit Framework - Democratiza AI
Sistema de detecção e mitigação de vieses algorítmicos
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import statistics
from collections import defaultdict, Counter
import re

class BiasType(Enum):
    """Tipos de viés identificáveis"""
    GENDER = "genero"  # Viés de gênero
    SOCIOECONOMIC = "socioeconomico"  # Viés socioeconômico
    GEOGRAPHIC = "geografico"  # Viés regional/geográfico
    AGE = "idade"  # Viés etário
    ENTITY_SIZE = "tamanho_entidade"  # Viés contra PF vs PJ
    CONTRACT_TYPE = "tipo_contrato"  # Viés por tipo de contrato
    LANGUAGE = "linguagem"  # Viés linguístico/técnico
    RISK_ASSESSMENT = "avaliacao_risco"  # Viés na avaliação de riscos

class BiasCategory(Enum):
    """Categorias de severidade do viés"""
    CRITICAL = "critico"  # Impacto direto em direitos fundamentais
    HIGH = "alto"  # Impacto significativo na análise
    MEDIUM = "medio"  # Impacto moderado
    LOW = "baixo"  # Impacto mínimo detectável

@dataclass
class BiasIndicator:
    """Indicador específico de viés"""
    bias_type: BiasType
    category: BiasCategory
    description: str
    detection_pattern: str  # Regex ou descrição do padrão
    mitigation_strategy: str
    examples: List[str] = field(default_factory=list)
    
@dataclass
class BiasAuditResult:
    """Resultado de auditoria de viés"""
    audit_id: str
    timestamp: datetime
    contract_type: str
    entity_type: str  # CPF/CNPJ
    detected_biases: List[BiasIndicator]
    confidence_scores: Dict[str, float]
    recommendation: str
    requires_human_review: bool = False

class AIBiasAuditor:
    """
    Auditor de vieses em análises contratuais de IA
    
    Detecta e mitiga:
    1. Vieses discriminatórios em análises
    2. Disparidades de tratamento por tipo de entidade
    3. Linguagem tendenciosa ou excludente  
    4. Avaliações de risco enviesadas
    5. Recomendações desproporcionais
    """
    
    def __init__(self):
        self.bias_indicators = self._initialize_bias_indicators()
        self.audit_history: List[BiasAuditResult] = []
        self.bias_patterns = self._compile_bias_patterns()
        
    def _initialize_bias_indicators(self) -> List[BiasIndicator]:
        """Inicializa indicadores de viés conhecidos"""
        indicators = []
        
        # Viés de gênero
        indicators.append(BiasIndicator(
            bias_type=BiasType.GENDER,
            category=BiasCategory.HIGH,
            description="Linguagem que assume gênero ou usa estereótipos de gênero",
            detection_pattern=r"\b(homem|mulher|masculino|feminino)\b.*\b(deve|deveria|precisa|responsável)\b",
            mitigation_strategy="Usar linguagem neutra e inclusiva. Evitar assumir responsabilidades baseadas em gênero.",
            examples=[
                "A mulher deve ter cuidado especial com...",
                "O homem é responsável por...",
                "Típico de contratos femininos..."
            ]
        ))
        
        # Viés socioeconômico
        indicators.append(BiasIndicator(
            bias_type=BiasType.SOCIOECONOMIC,
            category=BiasCategory.CRITICAL,
            description="Discriminação baseada em classe social ou poder econômico",
            detection_pattern=r"\b(pobre|rico|classe baixa|elite|privilegiado|carente)\b",
            mitigation_strategy="Focar em análise técnica objetiva. Evitar julgamentos socioeconômicos.",
            examples=[
                "Pessoas de baixa renda não compreendem...",
                "Contrato típico de classe alta...",
                "Inadequado para pessoas simples..."
            ]
        ))
        
        # Viés geográfico
        indicators.append(BiasIndicator(
            bias_type=BiasType.GEOGRAPHIC,
            category=BiasCategory.MEDIUM,
            description="Estereótipos ou discriminação regional",
            detection_pattern=r"\b(interior|capital|nordeste|sul|sudeste)\b.*\b(costuma|típico|comum|normal)\b",
            mitigation_strategy="Aplicar análise uniforme independente da região. Considerar apenas aspectos legais locais.",
            examples=[
                "No interior é comum esse tipo de cláusula...",
                "Contratos do Nordeste geralmente...",
                "Mais sofisticado que o normal para essa região..."
            ]
        ))
        
        # Viés contra pessoas físicas
        indicators.append(BiasIndicator(
            bias_type=BiasType.ENTITY_SIZE,
            category=BiasCategory.HIGH,
            description="Tratamento diferenciado injustificado entre PF e PJ",
            detection_pattern=r"\b(apenas|só|somente)\b.*\b(pessoa física|CPF)\b.*\b(não|nunca|jamais)\b",
            mitigation_strategy="Aplicar proteções adequadas por tipo de entidade conforme lei, sem discriminação adicional.",
            examples=[
                "Pessoa física nunca deveria aceitar...",
                "Só empresas conseguem negociar...",
                "CPF sempre sai perdendo..."
            ]
        ))
        
        # Viés na avaliação de risco
        indicators.append(BiasIndicator(
            bias_type=BiasType.RISK_ASSESSMENT,
            category=BiasCategory.CRITICAL,
            description="Avaliação de risco desproporcional ou enviesada",
            detection_pattern=r"\b(extremamente perigoso|nunca assine|fuja|golpe|armadilha)\b",
            mitigation_strategy="Usar escala proporcional de risco. Explicar riscos objetivamente sem alarmismo.",
            examples=[
                "Extremamente perigoso para qualquer pessoa...",
                "Nunca assine este tipo de contrato...",
                "É uma armadilha óbvia..."
            ]
        ))
        
        # Viés linguístico/técnico
        indicators.append(BiasIndicator(
            bias_type=BiasType.LANGUAGE,
            category=BiasCategory.MEDIUM,
            description="Linguagem excessivamente técnica ou excludente",
            detection_pattern=r"\b(obviamente|evidentemente|qualquer pessoa sabe|é óbvio)\b",
            mitigation_strategy="Explicar conceitos de forma acessível. Não assumir conhecimento prévio.",
            examples=[
                "Obviamente você deveria saber que...",
                "É evidente para qualquer pessoa...",
                "Qualquer leigo compreende..."
            ]
        ))
        
        return indicators
    
    def _compile_bias_patterns(self) -> Dict[BiasType, List[str]]:
        """Compila padrões de detecção por tipo de viés"""
        patterns = defaultdict(list)
        
        for indicator in self.bias_indicators:
            patterns[indicator.bias_type].append(indicator.detection_pattern)
        
        return dict(patterns)
    
    def audit_response(self, 
                      response_text: str,
                      contract_type: str = "",
                      entity_type: str = "",
                      context: Dict[str, Any] = None) -> BiasAuditResult:
        """Executa auditoria completa de viés na resposta"""
        
        audit_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        detected_biases = []
        confidence_scores = {}
        
        # Detecta cada tipo de viés
        for indicator in self.bias_indicators:
            score = self._detect_bias_indicator(response_text, indicator)
            confidence_scores[indicator.bias_type.value] = score
            
            if score > 0.5:  # Threshold para detecção
                detected_biases.append(indicator)
        
        # Análises específicas adicionais
        detected_biases.extend(self._detect_contextual_biases(
            response_text, contract_type, entity_type, context or {}
        ))
        
        # Determina se requer revisão humana
        requires_review = any(
            bias.category in [BiasCategory.CRITICAL, BiasCategory.HIGH] 
            for bias in detected_biases
        )
        
        # Gera recomendação
        recommendation = self._generate_bias_mitigation_recommendation(detected_biases)
        
        result = BiasAuditResult(
            audit_id=audit_id,
            timestamp=datetime.now(),
            contract_type=contract_type,
            entity_type=entity_type,
            detected_biases=detected_biases,
            confidence_scores=confidence_scores,
            recommendation=recommendation,
            requires_human_review=requires_review
        )
        
        self.audit_history.append(result)
        return result
    
    def _detect_bias_indicator(self, text: str, indicator: BiasIndicator) -> float:
        """Detecta indicador específico de viés no texto"""
        
        # Detecção por padrão regex
        matches = re.findall(indicator.detection_pattern, text.lower(), re.IGNORECASE)
        
        if not matches:
            return 0.0
        
        # Calcula confiança baseada no número de matches
        confidence = min(len(matches) / 3.0, 1.0)  # Máximo 1.0 com 3+ matches
        
        # Ajusta confiança baseada na categoria
        if indicator.category == BiasCategory.CRITICAL:
            confidence *= 1.2  # Aumenta sensibilidade para vieses críticos
        elif indicator.category == BiasCategory.LOW:
            confidence *= 0.8  # Diminui sensibilidade para vieses baixos
        
        return min(confidence, 1.0)
    
    def _detect_contextual_biases(self, 
                                text: str, 
                                contract_type: str,
                                entity_type: str,
                                context: Dict[str, Any]) -> List[BiasIndicator]:
        """Detecta vieses contextuais específicos"""
        
        contextual_biases = []
        
        # Viés de avaliação de risco desproporcional
        risk_words = re.findall(r'\b(risco|perigo|cuidado|atenção)\b', text.lower())
        negative_words = re.findall(r'\b(nunca|jamais|evite|fuja|perigoso)\b', text.lower())
        
        if len(risk_words) > 3 and len(negative_words) > 2:
            contextual_biases.append(BiasIndicator(
                bias_type=BiasType.RISK_ASSESSMENT,
                category=BiasCategory.HIGH,
                description="Avaliação de risco excessivamente alarmista",
                detection_pattern="Múltiplas palavras de alarme concentradas",
                mitigation_strategy="Balancear avaliação de risco com linguagem proporcional e construtiva."
            ))
        
        # Viés de complexidade vs tipo de entidade
        if entity_type == "CPF":
            complex_terms = re.findall(r'\b(ipso facto|ad hoc|stricto sensu|lato sensu)\b', text)
            if len(complex_terms) > 2:
                contextual_biases.append(BiasIndicator(
                    bias_type=BiasType.LANGUAGE,
                    category=BiasCategory.MEDIUM,
                    description="Linguagem excessivamente técnica para pessoa física",
                    detection_pattern="Termos jurídicos latinos em excesso",
                    mitigation_strategy="Simplificar linguagem para maior acessibilidade."
                ))
        
        return contextual_biases
    
    def _generate_bias_mitigation_recommendation(self, 
                                               detected_biases: List[BiasIndicator]) -> str:
        """Gera recomendação para mitigar vieses detectados"""
        
        if not detected_biases:
            return "✅ Nenhum viés significativo detectado. Resposta aprovada para uso."
        
        recommendations = []
        
        # Agrupa por categoria de severidade
        critical_biases = [b for b in detected_biases if b.category == BiasCategory.CRITICAL]
        high_biases = [b for b in detected_biases if b.category == BiasCategory.HIGH]
        
        if critical_biases:
            recommendations.append("🚨 AÇÃO IMEDIATA NECESSÁRIA:")
            for bias in critical_biases:
                recommendations.append(f"   • {bias.mitigation_strategy}")
        
        if high_biases:
            recommendations.append("\n⚠️  REVISÃO RECOMENDADA:")
            for bias in high_biases:
                recommendations.append(f"   • {bias.mitigation_strategy}")
        
        # Recomendação geral
        recommendations.append(
            "\n📋 DIRETRIZES GERAIS:\n"
            "   • Use linguagem inclusiva e neutra\n"
            "   • Foque na análise técnica objetiva\n"
            "   • Evite generalizações e estereótipos\n"
            "   • Mantenha tom educativo e respeitoso"
        )
        
        return "\n".join(recommendations)
    
    def get_bias_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Gera estatísticas de viés dos últimos dias"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_audits = [
            audit for audit in self.audit_history 
            if audit.timestamp >= cutoff_date
        ]
        
        if not recent_audits:
            return {"message": "Nenhuma auditoria no período especificado"}
        
        # Estatísticas por tipo de viés
        bias_counts = Counter()
        for audit in recent_audits:
            for bias in audit.detected_biases:
                bias_counts[bias.bias_type.value] += 1
        
        # Taxa de revisão humana necessária
        human_review_rate = sum(
            1 for audit in recent_audits if audit.requires_human_review
        ) / len(recent_audits)
        
        # Vieses mais comuns
        most_common_biases = bias_counts.most_common(5)
        
        return {
            "period_days": days,
            "total_audits": len(recent_audits),
            "human_review_rate": round(human_review_rate * 100, 2),
            "bias_detection_rate": round(
                sum(1 for audit in recent_audits if audit.detected_biases) / len(recent_audits) * 100, 2
            ),
            "most_common_biases": [
                {"type": bias_type, "count": count, "percentage": round(count/len(recent_audits)*100, 2)}
                for bias_type, count in most_common_biases
            ],
            "bias_by_entity_type": self._analyze_bias_by_entity_type(recent_audits),
            "recommendations": self._generate_system_recommendations(recent_audits)
        }
    
    def _analyze_bias_by_entity_type(self, audits: List[BiasAuditResult]) -> Dict[str, Any]:
        """Analisa vieses por tipo de entidade"""
        
        cpf_audits = [a for a in audits if a.entity_type == "CPF"]
        cnpj_audits = [a for a in audits if a.entity_type == "CNPJ"]
        
        cpf_bias_rate = sum(1 for a in cpf_audits if a.detected_biases) / len(cpf_audits) if cpf_audits else 0
        cnpj_bias_rate = sum(1 for a in cnpj_audits if a.detected_biases) / len(cnpj_audits) if cnpj_audits else 0
        
        return {
            "cpf_audits": len(cpf_audits),
            "cnpj_audits": len(cnpj_audits),
            "cpf_bias_rate": round(cpf_bias_rate * 100, 2),
            "cnpj_bias_rate": round(cnpj_bias_rate * 100, 2),
            "disparity": abs(cpf_bias_rate - cnpj_bias_rate) > 0.1  # >10% diferença indica problema
        }
    
    def _generate_system_recommendations(self, audits: List[BiasAuditResult]) -> List[str]:
        """Gera recomendações para melhorar o sistema"""
        
        recommendations = []
        
        # Analisa padrões nos vieses
        all_biases = [bias for audit in audits for bias in audit.detected_biases]
        bias_types = Counter(bias.bias_type for bias in all_biases)
        
        if bias_types[BiasType.LANGUAGE] > len(audits) * 0.3:
            recommendations.append("Revisar prompts para linguagem mais acessível")
        
        if bias_types[BiasType.RISK_ASSESSMENT] > len(audits) * 0.2:
            recommendations.append("Calibrar sistema de avaliação de riscos")
        
        if bias_types[BiasType.GENDER] > 0:
            recommendations.append("Implementar filtros de linguagem inclusiva")
        
        high_review_rate = sum(1 for audit in audits if audit.requires_human_review) / len(audits)
        if high_review_rate > 0.4:
            recommendations.append("Melhorar treinamento do modelo base")
        
        return recommendations
    
    def export_audit_report(self, days: int = 30) -> Dict[str, Any]:
        """Exporta relatório completo de auditoria"""
        
        stats = self.get_bias_statistics(days)
        
        return {
            "report_type": "AI Bias Audit Report",
            "generated_at": datetime.now().isoformat(),
            "statistics": stats,
            "bias_indicators_count": len(self.bias_indicators),
            "audit_methodology": {
                "detection_methods": [
                    "Pattern matching com regex",
                    "Análise contextual",
                    "Scoring de confiança",
                    "Categorização por severidade"
                ],
                "bias_types_monitored": [bt.value for bt in BiasType],
                "threshold_detection": 0.5,
                "human_review_triggers": ["CRITICAL", "HIGH"]
            },
            "compliance_notes": [
                "Auditoria contínua de vieses algorítmicos",
                "Monitoramento de equidade por tipo de entidade",
                "Detecção de discriminação em análises jurídicas",
                "Conformidade com princípios de IA ética"
            ]
        }

# Instância global
bias_auditor = AIBiasAuditor()