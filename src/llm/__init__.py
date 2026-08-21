import importlib
import os

from .base import Provider


def get_llm(provider_name: str, model: str, max_tokens: int) -> Provider:
    """
    Dynamically load `src/llm/providers/{provider}.py` and instantiate `{Provider}Provider`. Providers are user-installed via the add-model workflow — not shipped with the tool.
    """
    module_name = f"llm.providers.{provider_name.lower()}"
    class_name = f"{provider_name}Provider"

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise RuntimeError(
            f"No provider `{provider_name}` installed. Add it via:\n"
            f"  python src/main.py chat 'add {model}'"
        ) from None

    cls = getattr(module, class_name, None)
    
    if cls is None:
        raise RuntimeError(
            f"Provider module `{module_name}` was found but does not define `{class_name}`."
        )

    env_var = f"{provider_name.upper()}_API_KEY"
    api_key = os.getenv(env_var)

    if not api_key:
        raise RuntimeError(f"{env_var} is not set. Add it to .env before running.")

    return cls(api_key, model, max_tokens)