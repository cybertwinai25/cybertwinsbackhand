from fastapi import APIRouter
from app.schemas.risk import RiskScoreRequest, RiskScoreResponse
from app.risk_engine import calculate_risk_score

router = APIRouter(prefix="/risk", tags=["risk"])

@router.post("/score", response_model=RiskScoreResponse)
async def get_risk_score(request: RiskScoreRequest):
    # Calls the dynamic calculation engine with device info if provided
    risk_data = calculate_risk_score(request.email, request.device_info)
    
    return RiskScoreResponse(
        risk_score=risk_data["total_score"],
        risk_breakdown=risk_data["breakdown"]
    )
