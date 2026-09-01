from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, risk, advisor, reports

def verify_api_key(x_app_key: str = Header(None)):
    expected_key = os.environ.get("APP_SECRET_KEY")
    if not expected_key:
        raise HTTPException(status_code=500, detail="Server configuration error: APP_SECRET_KEY is not set")
    if not x_app_key or x_app_key != expected_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

app = FastAPI(title="Cybertwin Backend Stub", dependencies=[Depends(verify_api_key)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(risk.router)
app.include_router(advisor.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": "Backend stub is running"}
