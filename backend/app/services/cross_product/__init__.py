"""
Cross-Product Services
Services for ecosystem-wide features and integration
"""

from .journey_tracking_service import JourneyTrackingService
from .persona_detection_service import PersonaDetectionService
from .recommendation_engine import RecommendationEngine

__all__ = [
    "JourneyTrackingService",
    "PersonaDetectionService",
    "RecommendationEngine",
]
