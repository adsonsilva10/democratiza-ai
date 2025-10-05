"""
Unified User Profile Model
Central model for tracking user behavior across all products
"""

from sqlalchemy import Column, String, JSON, DateTime, Float, Enum as SQLEnum, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
import uuid

from app.db.database import Base


class ProductUsage(enum.Enum):
    """Product identifiers for tracking"""
    DIREITO_CLARO = "direito_claro"
    CONTRATO_SEGURO = "contrato_seguro"
    CONTRATO_FACIL = "contrato_facil"
    ADVOGADO_CERTO = "advogado_certo"
    
    # Helper for SQLAlchemy to use values instead of names
    @classmethod
    def _sa_values(cls):
        return [e.value for e in cls]


class UserPersona(enum.Enum):
    """User persona types for adaptive UI"""
    INDIVIDUAL = "individual"           # Pessoa física
    BUSINESS = "business"               # Pequena empresa/MEI
    LAWYER = "lawyer"                   # Advogado
    EDUCATIONAL = "educational"         # Uso educacional


class UnifiedUserProfile(Base):
    """
    Unified user profile that tracks behavior across all products.
    Enables cross-product recommendations and personalization.
    
    This is the foundation for:
    - Persona detection
    - Product recommendations
    - Journey tracking
    - Engagement scoring
    - Churn prediction
    """
    __tablename__ = "unified_user_profiles"
    
    # Primary keys
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, unique=True, index=True)  # Changed from UUID to String for flexibility
    email = Column(String, unique=True, nullable=False, index=True)
    
    # Persona detection
    detected_persona = Column(
        SQLEnum(UserPersona, name='user_persona_enum', values_callable=lambda x: [e.value for e in x]),
        default=UserPersona.INDIVIDUAL,
        nullable=False,
        index=True
    )
    persona_confidence = Column(Float, default=0.0)  # 0-1 confidence score
    persona_updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Cross-product engagement tracking
    # JSONB structure for flexible product-specific data
    product_usage = Column(JSON, default={
        "direito_claro": {
            "first_visit": None,
            "last_visit": None,
            "topics_read": [],
            "calculators_used": [],
            "chat_sessions": [],
            "engagement_score": 0,
            "conversion_signals": []
        },
        "contrato_seguro": {
            "first_analysis": None,
            "last_analysis": None,
            "analyses_count": 0,
            "risk_scores": [],
            "categories": [],
            "avg_score": 0
        },
        "contrato_facil": {
            "first_contract": None,
            "last_contract": None,
            "contracts_created": 0,
            "templates_used": [],
            "subscription_tier": None,
            "mrr": 0
        },
        "advogado_certo": {
            "first_consultation": None,
            "last_consultation": None,
            "consultations": [],
            "preferred_specialties": [],
            "budget_range": None,
            "total_spent": 0
        }
    })
    
    # ML-powered insights
    inferred_needs = Column(JSON, default={
        "immediate": [],      # Needs detected from recent behavior
        "upcoming": [],       # Predicted future needs
        "confidence": {}      # Confidence scores per need
    })
    
    # Conversion tracking between products
    conversion_signals = Column(JSON, default={
        "direito_claro_to_contrato_seguro": [],
        "contrato_seguro_to_contrato_facil": [],
        "contrato_seguro_to_advogado_certo": [],
        "contrato_facil_to_advogado_certo": [],
        "conversion_scores": {}
    })
    
    # Engagement metrics
    lifetime_value = Column(Float, default=0.0)      # Total revenue
    engagement_score = Column(Float, default=0.0, index=True)   # 0-100 score
    churn_risk = Column(Float, default=0.0)          # 0-1 probability
    
    # Activity counters (for quick queries)
    total_sessions = Column(Integer, default=0)
    total_transactions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active_at = Column(DateTime)
    
    def __repr__(self):
        return f"<UnifiedUserProfile(user_id={self.user_id}, persona={self.detected_persona.value})>"
    
    def update_engagement_score(self):
        """Calculate engagement score based on activity across products"""
        score = 0
        
        # Direito Claro activity (max 20 points)
        dc_data = self.product_usage.get("direito_claro", {})
        topics = len(dc_data.get("topics_read", []))
        score += min(topics * 2, 20)
        
        # Contrato Seguro activity (max 40 points)
        cs_data = self.product_usage.get("contrato_seguro", {})
        analyses = cs_data.get("analyses_count", 0)
        score += min(analyses * 10, 40)
        
        # Contrato Fácil activity (max 30 points)
        cf_data = self.product_usage.get("contrato_facil", {})
        contracts = cf_data.get("contracts_created", 0)
        score += min(contracts * 15, 30)
        
        # Advogado Certo activity (max 10 points)
        ac_data = self.product_usage.get("advogado_certo", {})
        consultations = len(ac_data.get("consultations", []))
        score += min(consultations * 5, 10)
        
        self.engagement_score = min(score, 100)
        return self.engagement_score
