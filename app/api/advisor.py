import os
from google import genai
from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.prompts import build_prompt
from app.risk_engine import calculate_risk_score

router = APIRouter(prefix="/advisor", tags=["advisor"])

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")

client = genai.Client(api_key=api_key)
MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-3.5-flash")

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    risk_data = calculate_risk_score(request.email)
    risk_score = risk_data["total_score"]
    risk_breakdown = risk_data["breakdown"]
    
    formatted_history = ""
    for msg in request.history[-10:]:
        role = "User" if msg.is_user else "CyberTwin AI"
        formatted_history += f"{role}: {msg.text}\n"

    prompt = build_prompt(
        risk_score=risk_score,
        risk_breakdown=risk_breakdown,
        conversation_history=formatted_history,
        user_message=request.message,
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini request failed: {e}")

    reply_text = response.text if response and response.text else "I am sorry, I couldn't process that."
    return ChatResponse(
        reply=reply_text,
        risk_score=risk_score,
        risk_breakdown=risk_breakdown
    )
