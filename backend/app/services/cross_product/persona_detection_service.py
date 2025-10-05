"""
Persona Detection Service
Automatically detects user persona based on behavior patterns
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


class PersonaDetectionService:
    """
    Detects and updates user persona based on behavior.
    
    Persona Rules:
    - LAWYER: Registered as lawyer in Advogado Certo
    - BUSINESS: High frequency in Contrato Fácil + subscription
    - EDUCATIONAL: Only uses Direito Claro, no transactions
    - INDIVIDUAL: Default, mixed usage
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def detect_persona(
        self,
        user_id: str,
        force_recalculate: bool = False
    ) -> Dict[str, any]:
        """
        Detect user persona based on behavior patterns.
        
        Args:
            user_id: User UUID
            force_recalculate: Force recalculation even if recently updated
            
        Returns:
            Dict with persona, confidence, and reasoning
        """
        
        result = await self.db.execute(
            select(UnifiedUserProfile).where(
                UnifiedUserProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            logger.warning(f"persona_detection_no_profile for user_id={user_id}")
            return {
                "persona": UserPersona.INDIVIDUAL.value,
                "confidence": 0.5,
                "reason": "No profile found, using default"
            }
        
        # Check if we need to recalculate
        if not force_recalculate and profile.persona_updated_at:
            time_since_update = datetime.utcnow() - profile.persona_updated_at
            if time_since_update < timedelta(days=7):
                return {
                    "persona": profile.detected_persona.value,
                    "confidence": profile.persona_confidence,
                    "reason": "Using cached persona (updated recently)"
                }
        
        # Detect new persona
        detection_result = self._analyze_behavior(profile)
        
        # Update profile if persona changed or confidence improved
        if (detection_result["persona"] != profile.detected_persona.value or
            detection_result["confidence"] > profile.persona_confidence):
            
            profile.detected_persona = UserPersona(detection_result["persona"])
            profile.persona_confidence = detection_result["confidence"]
            profile.persona_updated_at = datetime.utcnow()
            
            await self.db.commit()
            
            logger.info(
                "persona_updated",
                user_id=user_id,
                old_persona=profile.detected_persona.value,
                new_persona=detection_result["persona"],
                confidence=detection_result["confidence"]
            )
        
        return detection_result
    
    def _analyze_behavior(self, profile: UnifiedUserProfile) -> Dict[str, any]:
        """Analyze user behavior to determine persona"""
        
        usage = profile.product_usage
        
        # RULE 1: Lawyer persona
        ac_data = usage.get("advogado_certo", {})
        if ac_data.get("role") == "lawyer":
            return {
                "persona": UserPersona.LAWYER.value,
                "confidence": 1.0,
                "reason": "Registered as lawyer in marketplace",
                "signals": ["lawyer_registration"]
            }
        
        # RULE 2: Business persona
        cf_data = usage.get("contrato_facil", {})
        cf_contracts = cf_data.get("contracts_created", 0)
        cf_subscription = cf_data.get("subscription_tier")
        
        if cf_contracts >= 5 or cf_subscription in ["pro", "enterprise"]:
            business_score = 0.0
            signals = []
            
            if cf_contracts >= 10:
                business_score += 0.4
                signals.append(f"high_contract_volume:{cf_contracts}")
            elif cf_contracts >= 5:
                business_score += 0.3
                signals.append(f"medium_contract_volume:{cf_contracts}")
            
            if cf_subscription == "enterprise":
                business_score += 0.4
                signals.append("enterprise_subscription")
            elif cf_subscription == "pro":
                business_score += 0.3
                signals.append("pro_subscription")
            
            # Check Contrato Seguro usage
            cs_data = usage.get("contrato_seguro", {})
            if cs_data.get("analyses_count", 0) >= 5:
                business_score += 0.2
                signals.append("frequent_analysis")
            
            if business_score >= 0.6:
                return {
                    "persona": UserPersona.BUSINESS.value,
                    "confidence": min(business_score, 0.95),
                    "reason": "High contract creation volume and/or subscription",
                    "signals": signals
                }
        
        # RULE 3: Educational persona
        dc_data = usage.get("direito_claro", {})
        dc_topics = len(dc_data.get("topics_read", []))
        dc_calculators = len(dc_data.get("calculators_used", []))
        
        cs_data = usage.get("contrato_seguro", {})
        cs_analyses = cs_data.get("analyses_count", 0)
        
        # Only uses Direito Claro, never transacted
        if dc_topics >= 5 and cs_analyses == 0 and cf_contracts == 0:
            educational_score = 0.0
            signals = []
            
            if dc_topics >= 10:
                educational_score += 0.4
                signals.append(f"high_reading:{dc_topics}")
            elif dc_topics >= 5:
                educational_score += 0.3
                signals.append(f"medium_reading:{dc_topics}")
            
            if dc_calculators >= 3:
                educational_score += 0.3
                signals.append(f"calculator_usage:{dc_calculators}")
            
            if profile.lifetime_value == 0:
                educational_score += 0.2
                signals.append("no_transactions")
            
            if educational_score >= 0.5:
                return {
                    "persona": UserPersona.EDUCATIONAL.value,
                    "confidence": min(educational_score, 0.85),
                    "reason": "Focused on learning, no transactions",
                    "signals": signals
                }
        
        # RULE 4: Individual (default)
        individual_score = 0.5
        signals = ["default_persona"]
        
        # Boost confidence if there's mixed usage
        total_activity = dc_topics + cs_analyses + cf_contracts
        if total_activity >= 3:
            individual_score += 0.2
            signals.append("mixed_usage")
        
        if cs_analyses >= 1 and cs_analyses <= 3:
            individual_score += 0.15
            signals.append("occasional_analysis")
        
        return {
            "persona": UserPersona.INDIVIDUAL.value,
            "confidence": min(individual_score, 0.8),
            "reason": "General mixed usage pattern",
            "signals": signals
        }
    
    async def get_recommended_products(
        self,
        user_id: str
    ) -> List[Dict[str, any]]:
        """
        Get recommended products based on persona.
        
        Returns:
            List of recommended product configurations
        """
        
        result = await self.db.execute(
            select(UnifiedUserProfile).where(
                UnifiedUserProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            # Return default recommendations
            return self._get_default_recommendations()
        
        # Get persona-specific recommendations
        persona = profile.detected_persona
        
        if persona == UserPersona.BUSINESS:
            return [
                {
                    "product": "contrato_facil",
                    "priority": 1,
                    "reason": "Your main tool for contract creation"
                },
                {
                    "product": "advogado_certo",
                    "priority": 2,
                    "reason": "Legal consultation when needed"
                },
                {
                    "product": "contrato_seguro",
                    "priority": 3,
                    "reason": "Validate third-party contracts"
                }
            ]
        
        elif persona == UserPersona.LAWYER:
            return [
                {
                    "product": "advogado_certo",
                    "priority": 1,
                    "reason": "Your marketplace dashboard"
                }
            ]
        
        elif persona == UserPersona.EDUCATIONAL:
            return [
                {
                    "product": "direito_claro",
                    "priority": 1,
                    "reason": "Continue learning about your rights"
                },
                {
                    "product": "contrato_seguro",
                    "priority": 2,
                    "reason": "When you need to analyze a contract"
                }
            ]
        
        else:  # INDIVIDUAL
            return [
                {
                    "product": "direito_claro",
                    "priority": 1,
                    "reason": "Learn about your rights"
                },
                {
                    "product": "contrato_seguro",
                    "priority": 2,
                    "reason": "Analyze contracts before signing"
                },
                {
                    "product": "contrato_facil",
                    "priority": 3,
                    "reason": "Create your own contracts"
                },
                {
                    "product": "advogado_certo",
                    "priority": 4,
                    "reason": "Connect with lawyers when needed"
                }
            ]
    
    def _get_default_recommendations(self) -> List[Dict[str, any]]:
        """Default recommendations for new users"""
        return [
            {
                "product": "direito_claro",
                "priority": 1,
                "reason": "Start by learning about your rights"
            },
            {
                "product": "contrato_seguro",
                "priority": 2,
                "reason": "Analyze contracts safely"
            },
            {
                "product": "contrato_facil",
                "priority": 3,
                "reason": "Create professional contracts"
            },
            {
                "product": "advogado_certo",
                "priority": 4,
                "reason": "Find specialized lawyers"
            }
        ]
    
    async def update_persona_manually(
        self,
        user_id: str,
        persona: UserPersona,
        reason: str = "Manual override"
    ) -> Dict[str, any]:
        """
        Manually set user persona (admin override or user selection).
        
        Args:
            user_id: User UUID
            persona: Desired persona
            reason: Reason for manual update
            
        Returns:
            Updated persona information
        """
        
        result = await self.db.execute(
            select(UnifiedUserProfile).where(
                UnifiedUserProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise ValueError(f"Profile not found for user {user_id}")
        
        old_persona = profile.detected_persona.value
        profile.detected_persona = persona
        profile.persona_confidence = 0.95  # High confidence for manual
        profile.persona_updated_at = datetime.utcnow()
        
        await self.db.commit()
        
        logger.info(
            "persona_manually_updated",
            user_id=user_id,
            old_persona=old_persona,
            new_persona=persona.value,
            reason=reason
        )
        
        return {
            "persona": persona.value,
            "confidence": 0.95,
            "reason": reason,
            "updated_at": datetime.utcnow().isoformat()
        }
