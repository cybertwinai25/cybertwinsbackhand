from pydantic import BaseModel
from typing import Dict, Any

class RiskScoreResponse(BaseModel):
    risk_score: int
    risk_breakdown: Dict[str, Any]
