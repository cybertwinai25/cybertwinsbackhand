from pydantic import BaseModel
from typing import Dict, Any, Optional

class DeviceSecurityInput(BaseModel):
    is_lock_screen_secure: bool
    root_detected: bool
    is_outdated_os: bool

class RiskScoreRequest(BaseModel):
    email: str = "user@example.com"
    device_info: Optional[DeviceSecurityInput] = None

class RiskScoreResponse(BaseModel):
    risk_score: int
    risk_breakdown: Dict[str, Any]
