from .prompt_parser import parse_prompt
from .provider_file_creator import create_provider_file
from .provider_sdk_docs_fetcher import fetch_provider_sdk_docs
from .status_messages import emit
from workflows.utils import install_if_missing
from .util import provider_file_exists

def run(user_prompt: str) -> None:
    """Natural-language entry: parse the prompt, resolve provider/model, then run the pipeline."""
    parsed = parse_prompt(user_prompt)

    if parsed["confidence"] < 0.7:
        emit("AMBIGUOUS", parsed)
        return

    provider = parsed["provider"]
    model = parsed["model"]

    if provider_file_exists(provider):
        emit("PROVIDER_EXISTS", {"provider": provider, "model": model})
        return

    docs = fetch_provider_sdk_docs(provider)

    install_if_missing(docs["sdk_package"])

    create_provider_file(provider, model, docs)

    emit("GENERATED", {"provider": provider, "model": model})

def dispatch(model: str) -> None:
    """CLI dispatcher for `add-model MODEL`. Hands the model name to the LLM parser via `run`."""
    run(f"add {model}")