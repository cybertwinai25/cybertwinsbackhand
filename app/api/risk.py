from fastapi import APIRouter
from app.schemas.risk import RiskScoreResponse
from app.risk_engine import calculate_risk_score

router = APIRouter(prefix="/risk", tags=["risk"])

@router.get("/score", response_model=RiskScoreResponse)
async def get_risk_score(email: str = "user@example.com"):
    # TODO: replace default email parameter value with real user email once accounts/auth exist
    
    # Calls the dynamic calculation engine
    risk_data = calculate_risk_score(email)
    
    # Maps the dynamic engine's output perfectly to the RiskScoreResponse schema
    return RiskScoreResponse(
        risk_score=risk_data["total_score"],
        risk_breakdown=risk_data["breakdown"]
    )
