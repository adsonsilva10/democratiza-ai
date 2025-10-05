"""
Journey Tracking Service
Tracks user journey across all products in the ecosystem
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import logging

from app.models.cross_product.unified_user import (
    UnifiedUserProfile,
    ProductUsage,
    UserPersona
)

logger = logging.getLogger(__name__)


class JourneyTrackingService:
    """
    Tracks user journey across all products.
    Core service for cross-product analytics and personalization.
    
    Responsibilities:
    - Track events from all products
    - Update unified user profile
    - Detect conversion signals
    - Calculate engagement scores
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def track_event(
        self,
        user_id: str,
        product: ProductUsage,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """
        Track any user event across products.
        
        Args:
            user_id: User UUID
            product: Product where event occurred
            event_type: Type of event (e.g., "article_read", "analysis_completed")
            event_data: Event-specific data
            
        Examples:
            >>> await service.track_event(
            ...     user_id="123e4567-e89b-12d3-a456-426614174000",
            ...     product=ProductUsage.DIREITO_CLARO,
            ...     event_type="article_read",
            ...     event_data={"topic": "rescisão trabalhista", "duration": 120}
            ... )
        """
        
        try:
            # Get or create unified profile
            profile = await self._get_or_create_profile(user_id)
            
            # Update product-specific data
            product_key = product.value
            
            # Ensure product data exists
            if product_key not in profile.product_usage:
                profile.product_usage[product_key] = self._get_default_product_data(product)
            
            # Update based on event type
            await self._handle_event(profile, product, event_type, event_data)
            
            # Update activity timestamp
            profile.last_active_at = datetime.utcnow()
            profile.total_sessions += 1
            
            # Recalculate engagement score
            profile.update_engagement_score()
            
            # Log BEFORE commit (to avoid accessing attributes after session closes)
            engagement_score = profile.engagement_score  # Cache value before commit
            
            # Save changes
            await self.db.commit()
            
            logger.info(
                f"event_tracked: user_id={user_id}, product={product.value}, "
                f"event_type={event_type}, engagement_score={engagement_score}"
            )
            
        except Exception as e:
            await self.db.rollback()
            logger.error(
                f"event_tracking_failed: user_id={user_id}, product={product.value}, "
                f"event_type={event_type}, error={str(e)}"
            )
            raise
    
    async def _handle_event(
        self,
        profile: UnifiedUserProfile,
        product: ProductUsage,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """Handle specific event types for each product"""
        
        product_key = product.value
        
        # Direito Claro events
        if product == ProductUsage.DIREITO_CLARO:
            await self._handle_direito_claro_event(profile, event_type, event_data)
        
        # Contrato Seguro events
        elif product == ProductUsage.CONTRATO_SEGURO:
            await self._handle_contrato_seguro_event(profile, event_type, event_data)
        
        # Contrato Fácil events
        elif product == ProductUsage.CONTRATO_FACIL:
            await self._handle_contrato_facil_event(profile, event_type, event_data)
        
        # Advogado Certo events
        elif product == ProductUsage.ADVOGADO_CERTO:
            await self._handle_advogado_certo_event(profile, event_type, event_data)
    
    async def _handle_direito_claro_event(
        self,
        profile: UnifiedUserProfile,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """Handle Direito Claro specific events"""
        
        dc_data = profile.product_usage.get("direito_claro", {})
        
        if event_type == "article_read":
            topic = event_data.get("topic", "")
            dc_data["topics_read"].append({
                "topic": topic,
                "timestamp": datetime.utcnow().isoformat(),
                "duration": event_data.get("duration", 0)
            })
            dc_data["last_visit"] = datetime.utcnow().isoformat()
            
            # Check for conversion signals to Contrato Seguro
            if self._detect_contrato_seguro_intent(topic):
                self._add_conversion_signal(
                    profile,
                    "direito_claro_to_contrato_seguro",
                    {
                        "detected_at": datetime.utcnow().isoformat(),
                        "source": "article_read",
                        "topic": topic,
                        "confidence": 0.7
                    }
                )
        
        elif event_type == "calculator_used":
            calc_type = event_data.get("calculator_type", "")
            dc_data["calculators_used"].append({
                "type": calc_type,
                "timestamp": datetime.utcnow().isoformat(),
                "result": event_data.get("result")
            })
        
        elif event_type == "clara_chat":
            dc_data["chat_sessions"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "message_count": event_data.get("message_count", 0),
                "topics": event_data.get("topics", [])
            })
        
        profile.product_usage["direito_claro"] = dc_data
    
    async def _handle_contrato_seguro_event(
        self,
        profile: UnifiedUserProfile,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """Handle Contrato Seguro specific events"""
        
        cs_data = profile.product_usage.get("contrato_seguro", {})
        
        if event_type == "analysis_started":
            if not cs_data.get("first_analysis"):
                cs_data["first_analysis"] = datetime.utcnow().isoformat()
        
        elif event_type == "analysis_completed":
            cs_data["analyses_count"] = cs_data.get("analyses_count", 0) + 1
            cs_data["last_analysis"] = datetime.utcnow().isoformat()
            
            risk_score = event_data.get("risk_score", 0)
            cs_data["risk_scores"].append(risk_score)
            
            contract_type = event_data.get("contract_type", "")
            if contract_type not in cs_data.get("categories", []):
                cs_data.setdefault("categories", []).append(contract_type)
            
            # Calculate average risk score
            scores = cs_data["risk_scores"]
            cs_data["avg_score"] = sum(scores) / len(scores) if scores else 0
            
            # High risk = potential conversion to Advogado Certo
            if risk_score >= 7:
                self._add_conversion_signal(
                    profile,
                    "contrato_seguro_to_advogado_certo",
                    {
                        "detected_at": datetime.utcnow().isoformat(),
                        "source": "high_risk_analysis",
                        "risk_score": risk_score,
                        "contract_type": contract_type,
                        "confidence": 0.85
                    }
                )
            
            # Multiple analyses = potential business user
            if cs_data["analyses_count"] >= 3:
                self._add_conversion_signal(
                    profile,
                    "contrato_seguro_to_contrato_facil",
                    {
                        "detected_at": datetime.utcnow().isoformat(),
                        "source": "frequent_analyses",
                        "analyses_count": cs_data["analyses_count"],
                        "confidence": 0.65
                    }
                )
        
        profile.product_usage["contrato_seguro"] = cs_data
    
    async def _handle_contrato_facil_event(
        self,
        profile: UnifiedUserProfile,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """Handle Contrato Fácil specific events"""
        
        cf_data = profile.product_usage.get("contrato_facil", {})
        
        if event_type == "contract_created":
            cf_data["contracts_created"] = cf_data.get("contracts_created", 0) + 1
            
            if not cf_data.get("first_contract"):
                cf_data["first_contract"] = datetime.utcnow().isoformat()
            
            cf_data["last_contract"] = datetime.utcnow().isoformat()
            
            template = event_data.get("template_type", "")
            cf_data.setdefault("templates_used", []).append(template)
            
            # Update MRR if subscription
            if event_data.get("subscription_tier"):
                cf_data["subscription_tier"] = event_data["subscription_tier"]
                cf_data["mrr"] = event_data.get("mrr", 0)
        
        elif event_type == "subscription_upgraded":
            cf_data["subscription_tier"] = event_data.get("tier")
            cf_data["mrr"] = event_data.get("mrr", 0)
            profile.lifetime_value += event_data.get("upgrade_value", 0)
        
        profile.product_usage["contrato_facil"] = cf_data
    
    async def _handle_advogado_certo_event(
        self,
        profile: UnifiedUserProfile,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """Handle Advogado Certo specific events"""
        
        ac_data = profile.product_usage.get("advogado_certo", {})
        
        if event_type == "consultation_booked":
            ac_data.setdefault("consultations", []).append({
                "timestamp": datetime.utcnow().isoformat(),
                "specialty": event_data.get("specialty"),
                "price": event_data.get("price", 0)
            })
            
            if not ac_data.get("first_consultation"):
                ac_data["first_consultation"] = datetime.utcnow().isoformat()
            
            ac_data["last_consultation"] = datetime.utcnow().isoformat()
            
            # Update total spent
            ac_data["total_spent"] = ac_data.get("total_spent", 0) + event_data.get("price", 0)
            profile.lifetime_value += event_data.get("price", 0)
            profile.total_transactions += 1
            
            # Track preferred specialties
            specialty = event_data.get("specialty")
            if specialty:
                ac_data.setdefault("preferred_specialties", []).append(specialty)
        
        profile.product_usage["advogado_certo"] = ac_data
    
    def _detect_contrato_seguro_intent(self, topic: str) -> bool:
        """Detect if user shows intent to use Contrato Seguro"""
        keywords = [
            "contrato", "cláusula", "analisar", "revisar",
            "assinar", "documento", "acordo"
        ]
        topic_lower = topic.lower()
        return any(keyword in topic_lower for keyword in keywords)
    
    def _add_conversion_signal(
        self,
        profile: UnifiedUserProfile,
        signal_type: str,
        signal_data: Dict[str, Any]
    ) -> None:
        """Add conversion signal to profile"""
        if signal_type not in profile.conversion_signals:
            profile.conversion_signals[signal_type] = []
        
        profile.conversion_signals[signal_type].append(signal_data)
        
        # Keep only last 10 signals per type
        profile.conversion_signals[signal_type] = \
            profile.conversion_signals[signal_type][-10:]
    
    def _get_default_product_data(self, product: ProductUsage) -> Dict[str, Any]:
        """Get default data structure for a product"""
        defaults = {
            ProductUsage.DIREITO_CLARO: {
                "first_visit": None,
                "last_visit": None,
                "topics_read": [],
                "calculators_used": [],
                "chat_sessions": [],
                "engagement_score": 0,
                "conversion_signals": []
            },
            ProductUsage.CONTRATO_SEGURO: {
                "first_analysis": None,
                "last_analysis": None,
                "analyses_count": 0,
                "risk_scores": [],
                "categories": [],
                "avg_score": 0
            },
            ProductUsage.CONTRATO_FACIL: {
                "first_contract": None,
                "last_contract": None,
                "contracts_created": 0,
                "templates_used": [],
                "subscription_tier": None,
                "mrr": 0
            },
            ProductUsage.ADVOGADO_CERTO: {
                "first_consultation": None,
                "last_consultation": None,
                "consultations": [],
                "preferred_specialties": [],
                "budget_range": None,
                "total_spent": 0
            }
        }
        return defaults.get(product, {})
    
    async def _get_or_create_profile(self, user_id: str) -> UnifiedUserProfile:
        """Get existing profile or create new one"""
        
        result = await self.db.execute(
            select(UnifiedUserProfile).where(
                UnifiedUserProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            # TODO: Get email from user table
            profile = UnifiedUserProfile(
                user_id=user_id,
                email=f"user_{user_id}@temp.com"  # Temporary
            )
            self.db.add(profile)
            await self.db.flush()
            
            logger.info(f"unified_profile_created for user_id={user_id}")
        
        return profile
    
    async def get_user_journey(
        self,
        user_id: str,
        limit: int = 50
    ) -> Dict[str, Any]:
        """Get user's journey timeline across products"""
        
        profile = await self._get_or_create_profile(user_id)
        
        # Build timeline from all product activities
        timeline = []
        
        # Direito Claro events
        dc_data = profile.product_usage.get("direito_claro", {})
        for topic in dc_data.get("topics_read", []):
            timeline.append({
                "product": "direito_claro",
                "type": "article_read",
                "timestamp": topic.get("timestamp"),
                "data": topic
            })
        
        # Contrato Seguro events
        cs_data = profile.product_usage.get("contrato_seguro", {})
        if cs_data.get("last_analysis"):
            timeline.append({
                "product": "contrato_seguro",
                "type": "analysis",
                "timestamp": cs_data["last_analysis"],
                "data": {
                    "count": cs_data["analyses_count"],
                    "avg_score": cs_data["avg_score"]
                }
            })
        
        # Sort by timestamp
        timeline.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return {
            "user_id": user_id,
            "persona": profile.detected_persona.value,
            "engagement_score": profile.engagement_score,
            "lifetime_value": profile.lifetime_value,
            "timeline": timeline[:limit],
            "conversion_signals": profile.conversion_signals
        }
