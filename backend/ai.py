import os
import httpx

OPENROUTER_URL = os.getenv("OPENROUTER_API_URL", "https://api.openrouter.ai/v1/chat/completions")


async def call_openrouter(prompt: str, model: str = "openai/gpt-oss-120b:free") -> dict:
    """Call OpenRouter chat completions; if no API key present, return a mock result.

    Returns a dict: {"mock": bool, "output": str}
    """
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        # Return deterministic mock for tests/local runs
        return {"mock": True, "output": "4"}
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(OPENROUTER_URL, json=payload, headers=headers)
            resp.raise_for_status()
            j = resp.json()
        except httpx.HTTPStatusError as e:
            return {"mock": False, "output": f"HTTP error: {e.response.status_code} {e.response.text}", "error": True}
        except httpx.RequestError as e:
            return {"mock": False, "output": f"Request error: {str(e)}", "error": True}
        except Exception as e:
            return {"mock": False, "output": f"Unexpected error: {str(e)}", "error": True}

        # Try several common response shapes to extract text
        content = None
        try:
            if isinstance(j, dict) and "choices" in j and len(j["choices"]) > 0:
                choice = j["choices"][0]
                # OpenRouter/OpenAI style
                if isinstance(choice.get("message"), dict) and "content" in choice["message"]:
                    content = choice["message"]["content"]
                elif "text" in choice:
                    content = choice["text"]
            # Some vendors return a top-level message
            if content is None and isinstance(j, dict) and "message" in j and isinstance(j["message"], dict):
                content = j["message"].get("content")
        except Exception:
            content = None

        if content is None:
            # fallback to a compact JSON string
            try:
                import json as _json

                content = _json.dumps(j)
            except Exception:
                content = str(j)

        return {"mock": False, "output": content}
