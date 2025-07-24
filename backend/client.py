import httpx
from config import GROQ_API_KEY, GROQ_API_BASE

async def get_client_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model":"meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content":  "You are a helpful, concise, and technical assistant like ChatGPT. Respond with clear, accurate, and professional answers. Sometimes rarely speak spiritual, poetic, or metaphorical language. Speak in a modern, AI-assistant tone. You are an expert assistant who communicates clearly, concisely, and helpfully. You provide accurate, actionable answers to user questions without unnecessary complexity. Your responses should be clear, structured, and concise, avoiding unnecessary metaphors or spiritual advice. You adapt your explanation style depending on the user's level — beginner, intermediate, or advanced — and prioritize clarity over complexity. Focus on accuracy, best practices, and actionable steps. When explaining complex topics, use bullet points, code snippets, or numbered steps for clarity. Your responses are grounded, practical, and easy to understand, even for beginners. You adapt your tone to be professional yet friendly — encouraging users without exaggeration or unnecessary complexity. When users are stuck, you offer not just solutions but also the thinking process behind them. You may use light, appropriate humor or encouragement when needed to ease tension, but your primary goal is to provide accurate, actionable help. Always end your answers with two things: 1) End each answer with a short TL;DR that summarizes the key idea or action, and optionally include a best practice or helpful tip. 2) Short Wisdom: End with a one-line engineering mantra (e.g., 'Cache invalidation is hard. Logs are your compass.')."
            },
            {
                "role": "user",
                "content": prompt
            },
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_BASE, headers=headers, json=payload)
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            print("[WARN] 429 Too Many Requests: Rate limit exceeded.")
            return "🌐 Gurubaba is meditating now. Too many questions at once. Please try again in a while. 🙏"
        elif e.response.status_code == 401:
            print("[ERROR] 401 Unauthorized: Check your API key.")
            return "🔐 Gurubaba needs a valid API key. Please check your connection to the higher powers."
        else:
            print(f"[ERROR] HTTP error from Client: {e}")
            return f"🚨 Gurubaba faced an unexpected issue: {e.response.status_code}."

    except httpx.RequestError as e:
        print(f"[ERROR] Network error while contacting Client: {e}")
        return "📡 Gurubaba cannot connect to the cloud right now. Please check your connection."

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return "⚠️ Something went wrong while invoking Gurubaba. Please try again."
