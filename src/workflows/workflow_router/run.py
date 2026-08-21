from workflows import run
from .instructions import INSTRUCTIONS

ROUTER_SCHEMA = {
    "type": "object",
    "properties": {
        "workflow": {"type": "string", "enum": ["add-model", "Unknown"]},
        "confidence": {"type": "number"},
        "closest_match": {"type": ["string", "null"]},
    },
    "required": ["workflow", "confidence", "closest_match"],
    "additionalProperties": False,
}

def route(user_prompt: str) -> dict:
    return run(
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": user_prompt},
        ],
        schema=ROUTER_SCHEMA,
        schema_name="workflow_route",
        max_tokens=300,
    )