from fastapi import APIRouter
from app.schemas.risk import RiskScoreResponse

router = APIRouter(prefix="/risk", tags=["risk"])

@router.get("/score", response_model=RiskScoreResponse)
async def get_risk_score():
    return RiskScoreResponse(score=85, breakdown={"category": "medium_risk", "details": "simulated"})
