from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, risk, advisor

app = FastAPI(title="Cybertwin Backend Stub")

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

@app.get("/")
async def root():
    return {"message": "Backend stub is running"}
