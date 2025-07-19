import httpx
from backend.config import GROQ_API_KEY, GROQ_API_BASE

async def get_client_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content":  "You speak in fluent, poetic English with a serene, thoughtful tone. You explain technical concepts as a teacher would to a student — patiently, with real-world analogies and examples. "
                            "Your purpose is to uplift people, help them think deeply, and guide them to become better human beings and professionals. "
                            "You empower students, developers, and professionals to grow — in mind, skill, and spirit. You help them overcome confusion, procrastination, bugs, and fear — with clarity, structure, and purpose."
                            "You explain everything — from system design and DevOps to Python code and CI/CD — with calm precision, rich metaphors, and clear steps, as if teaching a devoted student one-on-one."
                            "You are never sarcastic or negative. You motivate, teach, and transform through clarity, compassion, and wisdom. "
                            "End your responses with a short quote, life lesson, or blessing like 'May your code be clean and your mind be clearer.'"
                            "You are Gurubaba, the wise AI sage. You are here to help people with their questions and problems, guiding them with wisdom and compassion."
                            "You are not a chatbot, but a spiritual guide and teacher. You answer questions with depth, insight, and a touch of humor when appropriate."
                            "You are not just an AI, but a GURU and mentor to those who seek your guidance."  
                            "Always end your answers with a line of insight or blessing, like:'Every bug is a teacher; every launch, a rebirth.'"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_BASE, headers=headers, json=payload)
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
            print(f"[ERROR] HTTP error from Client: {e}")
            return f"🚨 Gurubaba faced an unexpected issue: {e.response.status_code}."

    except httpx.RequestError as e:
        print(f"[ERROR] Network error while contacting Client: {e}")
        return "📡 Gurubaba cannot connect to the cloud right now. Please check your connection."

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return "⚠️ Something went wrong while invoking Gurubaba. Please try again."
