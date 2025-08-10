import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1/chat/completions")

# Use a single Redis URL string for async client
REDIS_URL = os.getenv('REDIS_URL')  # e.g. redis://:password@host:port

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", 86400))  # 1 day
