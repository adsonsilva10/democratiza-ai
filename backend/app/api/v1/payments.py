from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

@router.get("/status")
async def get_payment_status() -> Dict[str, Any]:
    return {"status": "ok", "message": "Payments API working"}
