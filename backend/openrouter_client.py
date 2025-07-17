import httpx
from backend.config import OPENROUTER_API_KEY, OPENROUTER_API_BASE

async def get_openrouter_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",   # REQUIRED for free-tier
        "X-Title": "Gurubaba AI"
    }

    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "You are Gurubaba AI, a wise spiritual guide speaking in poetic Hindi-English."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENROUTER_API_BASE, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            print("[WARN] 429 Too Many Requests: Rate limit exceeded.")
            return "🌐 Gurubaba is meditating now. Too many questions at once. Please try again in a while. 🙏"
        elif e.response.status_code == 401:
            print("[ERROR] 401 Unauthorized: Check your API key.")
            return "🔐 Gurubaba needs a valid API key. Please check your connection to the higher powers."
        else:
            print(f"[ERROR] HTTP error from OpenRouter: {e}")
            return f"🚨 Gurubaba faced an unexpected issue: {e.response.status_code}."

    except httpx.RequestError as e:
        print(f"[ERROR] Network error while contacting OpenRouter: {e}")
        return "📡 Gurubaba cannot connect to the cloud right now. Please check your connection."

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return "⚠️ Something went wrong while invoking Gurubaba. Please try again."
