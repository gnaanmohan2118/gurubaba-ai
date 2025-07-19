import os
from dotenv import load_dotenv

load_dotenv()

PERPLEXITY_API_KEY= os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_BASE = os.getenv("PERPLEXITY_API_BASE", "https://api.perplexity.ai/v1/chat/completions")
