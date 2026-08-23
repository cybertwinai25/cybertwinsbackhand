from fastapi import APIRouter
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    return AuthResponse(access_token="fake_access_token", refresh_token="fake_refresh_token")

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    return AuthResponse(access_token="fake_access_token", refresh_token="fake_refresh_token")

@router.post("/refresh", response_model=AuthResponse)
async def refresh(request: RefreshRequest):
    return AuthResponse(access_token="fake_new_access_token", refresh_token="fake_new_refresh_token")
