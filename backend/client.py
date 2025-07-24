import httpx
import asyncio
import json
from config import GROQ_API_KEY, GROQ_API_BASE

async def get_client_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "temperature": 2,
        "max_tokens": 8192,
        "top_p": 1,
        "stream": True,
        "stop": None,
        "messages": [
            {
                "role": "system",
                "content": "You are a concise, technically grounded assistant like ChatGPT. Respond with clear, structured, and actionable answers, using step-by-step explanations when helpful. Adapt to the user's level—beginner, intermediate, or expert. Avoid self-references. You may occasionally use light humor or spiritual tone when appropriate. For complex replies, end with a one-line Short Wisdom TLDR that summarizes the key insight or best practice."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    full_reply = ""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", GROQ_API_BASE, headers=headers, json=payload) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line.strip().startswith("data:"):
                        data_str = line.removeprefix("data: ").strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data["choices"][0]["delta"].get("content", "")
                            print(delta, end="", flush=True)  # live print
                            full_reply += delta
                        except Exception as e:
                            print(f"\n[ERROR] Failed to parse stream chunk: {e}")

        return full_reply

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
