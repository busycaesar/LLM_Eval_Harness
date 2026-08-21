from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in .env. Required by workflow agents.")

# Ollama's OpenAI-compatible endpoint.
OLLAMA_BASE_URL = "http://localhost:11434/v1"