"""
Recommendation Engine
Suggests next products and actions based on user behavior
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.models.cross_product.unified_user import (
    UnifiedUserProfile,
    UserPersona,
    ProductUsage
)

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Recommends products and actions based on user behavior and context.
    
    Uses:
    - Conversion signals from journey tracking
    - Persona-based preferences
    - Recent activity patterns
    - User's current stage in journey
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_recommendations(
        self,
        user_id: str,
        context: Optional[Dict] = None,
        max_recommendations: int = 3
    ) -> List[Dict]:
        """
        Get personalized product recommendations.
        
        Args:
            user_id: User UUID
            context: Optional context (e.g., current page, recent action)
            max_recommendations: Maximum number of recommendations
            
        Returns:
            List of recommendations with priority and reasoning
        """
        
        result = await self.db.execute(
            select(UnifiedUserProfile).where(
                UnifiedUserProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            return self._get_default_recommendations(max_recommendations)
        
        recommendations = []
        
        # Check conversion signals (highest priority)
        signal_recs = self._get_signal_based_recommendations(profile)
        recommendations.extend(signal_recs)
        
        # Check engagement patterns
        engagement_recs = self._get_engagement_based_recommendations(profile)
        recommendations.extend(engagement_recs)
        
        # Check persona preferences
        persona_recs = self._get_persona_based_recommendations(profile)
        recommendations.extend(persona_recs)
        
        # Add context-specific recommendations
        if context:
            context_recs = self._get_context_based_recommendations(profile, context)
            recommendations.extend(context_recs)
        
        # Deduplicate and sort by score
        seen = set()
        unique_recs = []
        for rec in recommendations:
            product = rec["product"]
            if product not in seen:
                seen.add(product)
                unique_recs.append(rec)
        
        # Sort by score (descending)
        unique_recs.sort(key=lambda x: x["score"], reverse=True)
        
        return unique_recs[:max_recommendations]
    
    def _get_signal_based_recommendations(
        self,
        profile: UnifiedUserProfile
    ) -> List[Dict]:
        """Get recommendations based on conversion signals"""
        
        recommendations = []
        signals = profile.conversion_signals
        
        # Direito Claro → Contrato Seguro
        dc_to_cs = signals.get("direito_claro_to_contrato_seguro", [])
        if dc_to_cs:
            latest_signal = dc_to_cs[-1]
            confidence = latest_signal.get("confidence", 0)
            
            recommendations.append({
                "product": "contrato_seguro",
                "title": "Tem um contrato para analisar?",
                "description": "Nossa IA detecta cláusulas abusivas gratuitamente",
                "cta": "Analisar Contrato",
                "reason": f"Você leu sobre {latest_signal.get('topic', 'contratos')}",
                "score": 90 + (confidence * 10),
                "urgency": "medium",
                "type": "conversion_signal"
            })
        
        # Contrato Seguro → Advogado Certo (high risk)
        cs_to_ac = signals.get("contrato_seguro_to_advogado_certo", [])
        if cs_to_ac:
            latest_signal = cs_to_ac[-1]
            risk_score = latest_signal.get("risk_score", 0)
            
            recommendations.append({
                "product": "advogado_certo",
                "title": "Precisa de ajuda profissional?",
                "description": "Seu contrato apresenta riscos. Conectamos você com especialistas",
                "cta": "Consultar Advogado",
                "reason": f"Contrato com score de risco {risk_score}/10",
                "score": 85 + risk_score,
                "urgency": "high" if risk_score >= 8 else "medium",
                "type": "conversion_signal"
            })
        
        # Contrato Seguro → Contrato Fácil (frequent user)
        cs_to_cf = signals.get("contrato_seguro_to_contrato_facil", [])
        if cs_to_cf:
            latest_signal = cs_to_cf[-1]
            analyses_count = latest_signal.get("analyses_count", 0)
            
            recommendations.append({
                "product": "contrato_facil",
                "title": "Cansado de revisar contratos de terceiros?",
                "description": "Crie seus próprios contratos profissionais em minutos",
                "cta": "Criar Contrato",
                "reason": f"Você já analisou {analyses_count} contratos",
                "score": 70 + (analyses_count * 2),
                "urgency": "low",
                "type": "conversion_signal"
            })
        
        return recommendations
    
    def _get_engagement_based_recommendations(
        self,
        profile: UnifiedUserProfile
    ) -> List[Dict]:
        """Get recommendations based on engagement patterns"""
        
        recommendations = []
        usage = profile.product_usage
        
        # User reads a lot but never analyzed
        dc_data = usage.get("direito_claro", {})
        cs_data = usage.get("contrato_seguro", {})
        
        topics_read = len(dc_data.get("topics_read", []))
        analyses_count = cs_data.get("analyses_count", 0)
        
        if topics_read >= 3 and analyses_count == 0:
            recommendations.append({
                "product": "contrato_seguro",
                "title": "Pronto para aplicar o que aprendeu?",
                "description": "Analise um contrato com nossa IA",
                "cta": "Fazer Primeira Análise",
                "reason": f"Você leu {topics_read} artigos sobre direitos",
                "score": 60,
                "urgency": "low",
                "type": "engagement_pattern"
            })
        
        # Analyzed contracts but never created one
        cf_data = usage.get("contrato_facil", {})
        contracts_created = cf_data.get("contracts_created", 0)
        
        if analyses_count >= 2 and contracts_created == 0:
            recommendations.append({
                "product": "contrato_facil",
                "title": "Que tal criar seu próprio contrato?",
                "description": "Templates profissionais + IA personalizada",
                "cta": "Ver Templates",
                "reason": "Você já sabe o que procurar em contratos",
                "score": 55,
                "urgency": "low",
                "type": "engagement_pattern"
            })
        
        # Never consulted a lawyer despite having cases
        ac_data = usage.get("advogado_certo", {})
        consultations = len(ac_data.get("consultations", []))
        avg_risk = cs_data.get("avg_score", 0)
        
        if analyses_count >= 3 and consultations == 0 and avg_risk >= 6:
            recommendations.append({
                "product": "advogado_certo",
                "title": "Seus contratos têm riscos médios/altos",
                "description": "Uma consulta de 30min pode economizar milhares",
                "cta": "Buscar Advogado",
                "reason": f"Score médio de risco: {avg_risk:.1f}/10",
                "score": 50 + (avg_risk * 3),
                "urgency": "medium",
                "type": "engagement_pattern"
            })
        
        return recommendations
    
    def _get_persona_based_recommendations(
        self,
        profile: UnifiedUserProfile
    ) -> List[Dict]:
        """Get recommendations based on user persona"""
        
        recommendations = []
        persona = profile.detected_persona
        usage = profile.product_usage
        
        if persona == UserPersona.EDUCATIONAL:
            # Encourage transition to practical usage
            cs_analyses = usage.get("contrato_seguro", {}).get("analyses_count", 0)
            if cs_analyses == 0:
                recommendations.append({
                    "product": "contrato_seguro",
                    "title": "Teste grátis na prática",
                    "description": "Análise básica sem custo",
                    "cta": "Analisar Gratuitamente",
                    "reason": "Aplique o que você aprendeu",
                    "score": 40,
                    "urgency": "low",
                    "type": "persona_growth"
                })
        
        elif persona == UserPersona.BUSINESS:
            # Encourage lawyer consultation for complex cases
            ac_consultations = len(usage.get("advogado_certo", {}).get("consultations", []))
            if ac_consultations == 0:
                recommendations.append({
                    "product": "advogado_certo",
                    "title": "Suporte jurídico para seu negócio",
                    "description": "Advogados especializados em empresas",
                    "cta": "Conhecer Especialistas",
                    "reason": "Empresas precisam de respaldo jurídico",
                    "score": 45,
                    "urgency": "low",
                    "type": "persona_fit"
                })
        
        elif persona == UserPersona.INDIVIDUAL:
            # Balanced recommendations - already handled by other methods
            pass
        
        return recommendations
    
    def _get_context_based_recommendations(
        self,
        profile: UnifiedUserProfile,
        context: Dict
    ) -> List[Dict]:
        """Get recommendations based on current context"""
        
        recommendations = []
        current_product = context.get("current_product")
        current_action = context.get("current_action")
        
        # After completing analysis
        if current_product == "contrato_seguro" and current_action == "analysis_completed":
            risk_score = context.get("risk_score", 0)
            
            if risk_score >= 7:
                recommendations.append({
                    "product": "advogado_certo",
                    "title": "Este contrato precisa de atenção",
                    "description": "Fale com um advogado especialista agora",
                    "cta": "Buscar Especialista",
                    "reason": "Score de risco alto detectado",
                    "score": 95,
                    "urgency": "high",
                    "type": "contextual"
                })
            elif risk_score <= 3:
                recommendations.append({
                    "product": "contrato_facil",
                    "title": "Este é um bom modelo!",
                    "description": "Use-o como base para seus contratos",
                    "cta": "Criar Similar",
                    "reason": "Contrato seguro identificado",
                    "score": 50,
                    "urgency": "low",
                    "type": "contextual"
                })
        
        # Reading article about specific topic
        if current_product == "direito_claro" and current_action == "article_read":
            article_topic = context.get("article_topic", "").lower()
            
            if "contrato" in article_topic or "documento" in article_topic:
                recommendations.append({
                    "product": "contrato_seguro",
                    "title": "Tem um contrato sobre isso?",
                    "description": "Analise agora com nossa IA",
                    "cta": "Analisar",
                    "reason": f"Artigo relacionado: {article_topic}",
                    "score": 65,
                    "urgency": "medium",
                    "type": "contextual"
                })
        
        return recommendations
    
    def _get_default_recommendations(
        self,
        max_recommendations: int = 3
    ) -> List[Dict]:
        """Default recommendations for new users"""
        
        defaults = [
            {
                "product": "direito_claro",
                "title": "Comece aprendendo sobre seus direitos",
                "description": "1000+ artigos em português claro",
                "cta": "Explorar Conteúdo",
                "reason": "Recomendado para novos usuários",
                "score": 100,
                "urgency": "low",
                "type": "default"
            },
            {
                "product": "contrato_seguro",
                "title": "Tem um contrato para assinar?",
                "description": "Analise gratuitamente com nossa IA",
                "cta": "Analisar Grátis",
                "reason": "Proteção antes da assinatura",
                "score": 90,
                "urgency": "medium",
                "type": "default"
            },
            {
                "product": "contrato_facil",
                "title": "Precisa criar um contrato?",
                "description": "Templates validados + personalização IA",
                "cta": "Ver Templates",
                "reason": "Criação rápida e profissional",
                "score": 80,
                "urgency": "low",
                "type": "default"
            }
        ]
        
        return defaults[:max_recommendations]
    
    async def track_recommendation_interaction(
        self,
        user_id: str,
        recommendation_id: str,
        action: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Track user interaction with recommendations.
        
        Args:
            user_id: User UUID
            recommendation_id: Recommendation identifier
            action: Action taken ("viewed", "clicked", "dismissed")
            metadata: Additional interaction data
        """
        
        # TODO: Store recommendation interactions for ML improvement
        logger.info(
            "recommendation_interaction",
            user_id=user_id,
            recommendation_id=recommendation_id,
            action=action,
            metadata=metadata
        )
