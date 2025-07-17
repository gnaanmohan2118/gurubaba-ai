from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from backend.openrouter_client import get_openrouter_response

# Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "../frontend")
STATIC_DIR = os.path.join(BASE_DIR, "../frontend")

print(f"[INFO] BASE_DIR set to: {BASE_DIR}")
print(f"[INFO] TEMPLATES_DIR set to: {TEMPLATES_DIR}")
print(f"[INFO] STATIC_DIR set to: {STATIC_DIR}")

app = FastAPI()
print("[INFO] FastAPI app initialized.")

# Serve static and HTML
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
print("[INFO] Static and template directories mounted.")

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    print("[INFO] GET / called - Serving index.html")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Gurubaba server is running 🙏"}


@app.post("/chat")
async def chat_with_gurubaba(request: Request):
    print("[INFO] POST /chat called")

    try:
        data = await request.json()
        user_message = data.get("message")
        print(f"[INFO] Received message: {user_message}")

        if not user_message:
            print("[WARN] No message provided in request.")
            return JSONResponse(status_code=400, content={"error": "No message provided"})

        print("[INFO] Sending message to OpenRouter API...")
        reply = await get_openrouter_response(user_message)
        print(f"[INFO] Received reply: {reply}")

        return JSONResponse(content={"reply": reply})

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# Optional: if running directly with python main.py
if __name__ == "__main__":
    import uvicorn
    print("[INFO] Running app with uvicorn...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
