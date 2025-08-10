from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uuid
import json
import redis.asyncio as aioredis  # Async Redis client

from client import get_client_response
from config import REDIS_URL

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

app = FastAPI()

# Redis connection
redis = aioredis.from_url(REDIS_URL, decode_responses=True)

# Serve static and HTML
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Gurubaba server is running 🙏"}

@app.get("/session/{session_id}")
async def get_session_history(session_id: str):
    """Fetch stored conversation for a session."""
    history_json = await redis.get(f"session:{session_id}")
    if not history_json:
        return {"session_id": session_id, "history": []}
    return {"session_id": session_id, "history": json.loads(history_json)}

@app.post("/chat")
async def chat_with_gurubaba(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message")
        session_id = data.get("session_id") or str(uuid.uuid4())

        if not user_message:
            return JSONResponse(status_code=400, content={"error": "No message provided"})

        # Load history from Redis
        history_key = f"session:{session_id}"
        history_json = await redis.get(history_key)
        history = json.loads(history_json) if history_json else []

        # Append user message
        history.append({"role": "user", "content": user_message})

        # Send full history to LLM
        reply = await get_client_response(history)

        # Append bot reply to history
        history.append({"role": "assistant", "content": reply})

        # Save updated history
        await redis.set(history_key, json.dumps(history), ex=86400)  # TTL = 1 day

        return JSONResponse(content={
            "session_id": session_id,
            "reply": reply
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Optional: run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
