"""
Journey API Endpoints
Track and retrieve user journey across products
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Optional
from pydantic import BaseModel

from app.services.cross_product.journey_tracking_service import JourneyTrackingService
from app.models.cross_product.unified_user import ProductUsage
from app.db.database import get_db

router = APIRouter(prefix="/journey", tags=["Cross-Product"])


class TrackEventRequest(BaseModel):
    """Request to track an event"""
    user_id: str
    product: str
    event_type: str
    event_data: Dict


@router.post("/track")
async def track_event(
    request: TrackEventRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Track a user event across products.
    
    **Products:**
    - `direito_claro`
    - `contrato_seguro`
    - `contrato_facil`
    - `advogado_certo`
    
    **Event Types (examples):**
    - Direito Claro: `article_read`, `calculator_used`, `clara_chat`
    - Contrato Seguro: `analysis_started`, `analysis_completed`
    - Contrato Fácil: `contract_created`, `subscription_upgraded`
    - Advogado Certo: `consultation_booked`, `case_created`
    
    **Example Request:**
    ```json
    {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "product": "contrato_seguro",
        "event_type": "analysis_completed",
        "event_data": {
            "risk_score": 8.5,
            "contract_type": "rental",
            "issues_found": 3
        }
    }
    ```
    
    **Returns:**
    - Success confirmation
    """
    try:
        # Validate product
        try:
            product_enum = ProductUsage(request.product)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid product: {request.product}. Must be one of: {[p.value for p in ProductUsage]}"
            )
        
        service = JourneyTrackingService(db)
        await service.track_event(
            user_id=request.user_id,
            product=product_enum,
            event_type=request.event_type,
            event_data=request.event_data
        )
        
        return {
            "success": True,
            "message": "Event tracked successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track event: {str(e)}")


@router.get("/{user_id}")
async def get_user_journey(
    user_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's journey timeline across all products.
    
    **Query Parameters:**
    - `limit`: Maximum number of events to return (default: 50)
    
    **Returns:**
    - User journey with timeline, persona, engagement score, and conversion signals
    
    **Example Response:**
    ```json
    {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "persona": "individual",
        "engagement_score": 65.5,
        "lifetime_value": 29.90,
        "timeline": [
            {
                "product": "direito_claro",
                "type": "article_read",
                "timestamp": "2025-10-01T10:00:00",
                "data": {"topic": "rescisão trabalhista"}
            },
            {
                "product": "contrato_seguro",
                "type": "analysis_completed",
                "timestamp": "2025-10-02T14:30:00",
                "data": {"risk_score": 8.5}
            }
        ],
        "conversion_signals": {
            "direito_claro_to_contrato_seguro": [
                {
                    "detected_at": "2025-10-01T10:05:00",
                    "confidence": 0.7
                }
            ]
        }
    }
    ```
    """
    try:
        service = JourneyTrackingService(db)
        journey = await service.get_user_journey(
            user_id=user_id,
            limit=limit
        )
        
        return journey
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get journey: {str(e)}")
