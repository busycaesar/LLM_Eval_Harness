import sys
from .config import OPENAI_API_KEY, OLLAMA_BASE_URL
from .agent import run, infer, WORKFLOW_MODEL_SMALL, WORKFLOW_MODEL_LARGE
from .add_model import dispatch as add_model_dispatch, run as _add_model_run
from .workflow_router import route

WORKFLOWS = {
    "add-model": _add_model_run,
}

def chat_dispatch(text: str) -> None:
    """CLI dispatcher: route the prompt via the LLM router, then invoke the matching workflow."""
    intent = route(text)

    if intent["confidence"] < 0.7 or intent["workflow"] == "Unknown":
        closest = intent.get("closest_match")
        if closest:
            print(f"Not sure which workflow. Did you mean `{closest}`?")
        else:
            print("Not sure which workflow to run for that request.")
        sys.exit(1)

    fn = WORKFLOWS.get(intent["workflow"])

    if fn is None:
        print(f"No workflow registered under `{intent['workflow']}`.")
        sys.exit(1)

    fn(text)