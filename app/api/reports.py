from fastapi import APIRouter, Response
from app.schemas.risk import RiskScoreRequest
from app.risk_engine import calculate_risk_score
from app.report_generator import generate_report_pdf

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/generate")
async def generate_report(request: RiskScoreRequest):
    risk_data = calculate_risk_score(request.email, request.device_info)
    
    pdf_bytes = generate_report_pdf(
        email=request.email,
        risk_score=risk_data["total_score"],
        risk_breakdown=risk_data["breakdown"]
    )
    
    return Response(content=pdf_bytes, media_type="application/pdf")
