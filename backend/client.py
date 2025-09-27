import httpx
import json
import re
from backend.config import GROQ_API_KEY, GROQ_API_BASE

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        #style of content you wanted to tweak
    )
}

def clean_reply(text: str) -> str:
    # Remove markdown-like symbols
    text = re.sub(r"[#*`]+", "", text)
    # Collapse extra newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

async def get_client_response(history: list):
    """
    history: list of dicts [{"role": "user"/"assistant", "content": "..."}]
    Returns the assistant's reply as a string.
    """
    # Log user input in terminal
    if history and history[-1]["role"] == "user":
        print(f"\n[USER] {history[-1]['content']}\n")

    """
    history: list of dicts [{"role": "user"/"assistant", "content": "..."}]
    Returns the assistant's reply as a string.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # Ensure system prompt is always first
    messages = [SYSTEM_PROMPT] + history

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "temperature": 2,
        "max_tokens": 8192,
        "top_p": 1,
        "stream": True,
        "stop": None,
        "messages": messages
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
                            print(delta, end="", flush=True)  # Live print for dev
                            full_reply += delta
                        except Exception as e:
                            print(f"\n[ERROR] Failed to parse stream chunk: {e}")

        return clean_reply(full_reply)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            return "🌐 Gurubaba is meditating now. Too many questions at once. Please try again later. 🙏"
        elif e.response.status_code == 401:
            return "🔐 Gurubaba needs a valid API key. Please check your connection to the higher powers."
        else:
            return f"🚨 Gurubaba faced an unexpected issue: {e.response.status_code}."

    except httpx.RequestError:
        return "📡 Gurubaba cannot connect to the cloud right now. Please check your connection."

    except Exception as e:
        return f"⚠️ Something went wrong while invoking Gurubaba: {e}"
