"""
Cross-Product API Endpoints
Endpoints for ecosystem-wide features
"""

from .recommendations import router as recommendations_router
from .persona import router as persona_router
from .journey import router as journey_router

__all__ = [
    "recommendations_router",
    "persona_router",
    "journey_router",
]
