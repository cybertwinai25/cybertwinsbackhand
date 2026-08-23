import os
from google import genai
from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.prompts import build_prompt

router = APIRouter(prefix="/advisor", tags=["advisor"])

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.5-flash"

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    risk_score = 68
    risk_breakdown = {"passwords": -15, "breaches": -10, "device": 0}
    conversation_history = ""

    prompt = build_prompt(
        risk_score=risk_score,
        risk_breakdown=risk_breakdown,
        conversation_history=conversation_history,
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
    return ChatResponse(reply=reply_text)
