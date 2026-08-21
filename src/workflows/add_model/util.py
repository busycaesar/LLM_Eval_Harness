from .paths import provider_file

def provider_file_exists(provider: str) -> bool:
    """Return True if `src/llm/{provider}.py` already exists."""
    return provider_file(provider).exists()
