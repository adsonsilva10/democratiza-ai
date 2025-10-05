"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict
from pydantic import BaseModel

from app.services.cross_product.persona_detection_service import PersonaDetectionService
from app.models.cross_product.unified_user import UserPersona
from app.db.database import get_dbAPI Endpoints
Detect and manage user personas
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional
from pydantic import BaseModel

from app.services.cross_product.persona_detection_service import PersonaDetectionService
from app.models.cross_product.unified_user import UserPersona
from app.db.database import get_db

router = APIRouter(prefix="/persona", tags=["Cross-Product"])


class PersonaResponse(BaseModel):
    """Persona detection response"""
    persona: str
    confidence: float
    reason: str


class PersonaUpdateRequest(BaseModel):
    """Request to manually update persona - accepts both 'persona' and 'detected_persona'"""
    user_id: str
    persona: Optional[str] = None
    detected_persona: Optional[str] = None  # Alias for persona
    confidence_score: Optional[float] = None
    reason: Optional[str] = "Manual selection"
    detection_signals: Optional[Dict] = None
    
    def get_persona_value(self) -> str:
        """Get persona value from either field, fallback to 'individual'"""
        # Priority: persona > detected_persona > default
        if self.persona:
            return self.persona
        elif self.detected_persona:
            return self.detected_persona
        else:
            return "individual"


class ProductRecommendation(BaseModel):
    """Product recommendation based on persona"""
    product: str
    priority: int
    reason: str


@router.get("/{user_id}", response_model=PersonaResponse)
async def get_user_persona(
    user_id: str,
    force_recalculate: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's detected persona.
    
    **Personas:**
    - `individual`: Person física (default)
    - `business`: Small business / MEI
    - `lawyer`: Advogado
    - `educational`: Student / researcher
    
    **Query Parameters:**
    - `force_recalculate`: Force recalculation even if recently updated
    
    **Returns:**
    - Persona, confidence score, and reasoning
    """
    try:
        service = PersonaDetectionService(db)
        result = await service.detect_persona(
            user_id=user_id,
            force_recalculate=force_recalculate
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect persona: {str(e)}")


@router.get("/{user_id}/recommended-products", response_model=List[ProductRecommendation])
async def get_recommended_products(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get recommended products based on user's persona.
    
    **Returns:**
    - List of products ordered by priority for this persona
    """
    try:
        service = PersonaDetectionService(db)
        recommendations = await service.get_recommended_products(user_id=user_id)
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")


@router.post("/update", response_model=PersonaResponse)
async def update_persona_manually(
    request: PersonaUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Manually update user's persona.
    
    Use this endpoint when:
    - User explicitly selects their persona during onboarding
    - Admin override is needed
    - User changes their persona in settings
    
    **Returns:**
    - Updated persona information
    """
    try:
        # Validate persona
        persona_value = request.get_persona_value()
        try:
            persona_enum = UserPersona(persona_value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid persona: {persona_value}. Must be one of: {[p.value for p in UserPersona]}"
            )
        
        service = PersonaDetectionService(db)
        result = await service.update_persona_manually(
            user_id=request.user_id,
            persona=persona_enum,
            reason=request.reason
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update persona: {str(e)}")
