from config import ANTHROPIC_API_KEY, MAX_TOKENS
from .base import Provider
from .anthropic import AnthropicProvider

def get_llm(provider_name: str, model: str) -> Provider:
    if provider_name == "Anthropic":
        if not ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY is not set. Set it in .env before running llm_eval.")
        return AnthropicProvider(ANTHROPIC_API_KEY, model, MAX_TOKENS)
    raise RuntimeError(f"No provider implemented yet for '{provider_name}'.")
