from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from backend.openrouter_client import get_openrouter_response

# Template and static file directories
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

app = FastAPI()

# Mount static files (if you have any static/css/js)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Jinja2 for HTML rendering
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Root route - serve index.html
@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Gurubaba server is running 🙏"}

# Chat endpoint
@app.post("/chat")
async def chat_with_gurubaba(request: Request):
    print("[INFO] POST /chat called")
    try:
        data = await request.json()
        user_message = data.get("message")

        if not user_message:
            return JSONResponse(status_code=400, content={"error": "No message provided"})

        reply = await get_openrouter_response(user_message)
        return JSONResponse(content={"reply": reply})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# For local dev (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
