from workflows import run
from .instructions import INSTRUCTIONS

EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "model": {"type": "string"},
        "provider": {"type": "string"},
        "confidence": {"type": "number"},
        "closest_match": {"type": ["string", "null"]},
    },
    "required": ["model", "provider", "confidence", "closest_match"],
    "additionalProperties": False,
}

def parse_prompt(user_prompt: str) -> dict:
    return run(
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": user_prompt},
        ],
        schema=EXTRACT_SCHEMA,
        schema_name="extraction",
        max_tokens=500,
    )
