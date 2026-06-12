from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.ai import call_openrouter

router = APIRouter()


class AIQuery(BaseModel):
    prompt: Optional[str] = None


@router.post("/api/ai/test")
async def ai_test(query: AIQuery):
    prompt = query.prompt or "What is 2+2?"
    res = await call_openrouter(prompt)
    # If the helper returned an error flag, surface it in a 502-friendly manner
    if res.get("error"):
        raise HTTPException(status_code=502, detail=res.get("output"))
    return {"result": res.get("output"), "mock": res.get("mock", False)}
