import os
from dotenv import load_dotenv
import redis

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
GROQ_API_BASE=os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1/chat/completions")

#OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
#OPENROUTER_API_BASE = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1/chat/completions")


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# === Model Config (future-proof for multiple LLM providers) ===
# Default model for Guru Baba
#DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

# Session settings
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", 86400))  # 1 day
