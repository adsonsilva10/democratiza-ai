"""
Recommendations API Endpoints
Get personalized product recommendations
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional
from pydantic import BaseModel

from app.services.cross_product.recommendation_engine import RecommendationEngine
from app.db.database import get_db

router = APIRouter(prefix="/recommendations", tags=["Cross-Product"])


class RecommendationResponse(BaseModel):
    """Recommendation response model"""
    product: str
    title: str
    description: str
    cta: str
    reason: str
    score: float
    urgency: str
    type: str


class RecommendationsRequest(BaseModel):
    """Request model for recommendations"""
    user_id: str
    current_product: Optional[str] = None  # Added for compatibility
    context: Optional[Dict] = None
    max_recommendations: int = 3
    limit: Optional[int] = None  # Alias for max_recommendations


class InteractionTrackRequest(BaseModel):
    """Request to track recommendation interaction"""
    user_id: str
    recommended_product: str
    interaction_type: str  # 'viewed', 'clicked', 'dismissed'
    context: Optional[Dict] = None


@router.post("/", response_model=List[RecommendationResponse])
async def get_recommendations(
    request: RecommendationsRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized product recommendations for a user.
    
    **Context examples:**
    - `{"current_product": "contrato_seguro", "current_action": "analysis_completed", "risk_score": 8}`
    - `{"current_product": "direito_claro", "current_action": "article_read", "article_topic": "contratos"}`
    
    **Returns:**
    - List of recommendations sorted by relevance score
    """
    try:
        engine = RecommendationEngine(db)
        recommendations = await engine.get_recommendations(
            user_id=request.user_id,
            context=request.context,
            max_recommendations=request.max_recommendations
        )
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")


@router.post("/track-interaction")
async def track_recommendation_interaction(
    request: InteractionTrackRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Track user interaction with a recommendation.
    
    **Interaction Types:**
    - `viewed`: Recommendation was shown to user
    - `clicked`: User clicked on recommendation
    - `dismissed`: User dismissed/closed recommendation
    
    **Example Request:**
    ```json
    {
        "user_id": "123",
        "recommended_product": "contrato_facil",
        "interaction_type": "clicked",
        "context": {
            "source": "contrato_seguro_analysis_page",
            "position": 1
        }
    }
    ```
    
    **Returns:**
    - Success confirmation
    """
    try:
        engine = RecommendationEngine(db)
        # Map recommended_product to recommendation_id for internal tracking
        await engine.track_recommendation_interaction(
            user_id=request.user_id,
            recommendation_id=request.recommended_product,  # Using product as ID
            action=request.interaction_type,
            metadata=request.context
        )
        
        return {"success": True, "message": "Interaction tracked"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track interaction: {str(e)}")
