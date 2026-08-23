from pydantic import BaseModel
from typing import Dict, Any

class RiskScoreResponse(BaseModel):
    score: int
    breakdown: Dict[str, Any]
