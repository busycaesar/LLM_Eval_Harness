from workflows import run, WORKFLOW_MODEL_SMALL
from .instructions import INSTRUCTIONS
from .tools import WEB_FETCH_TOOL, WEB_SEARCH_TOOL, web_fetch, web_search

DOCS_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "sdk_package": {"type": "string"},
        "example_code": {"type": "string"},
        "response_extraction": {"type": "string"},
    },
    "required": ["sdk_package", "example_code", "response_extraction"],
    "additionalProperties": False,
}

def fetch_provider_sdk_docs(provider: str) -> dict:
    return run(
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": f"Provider: {provider}"},
        ],
        schema=DOCS_OUTPUT_SCHEMA,
        tools=[WEB_SEARCH_TOOL, WEB_FETCH_TOOL],
        tool_fns={"web_search": web_search, "web_fetch": web_fetch},
        schema_name="docs_summary",
        model=WORKFLOW_MODEL_SMALL,
        max_tokens=4096,
    )
