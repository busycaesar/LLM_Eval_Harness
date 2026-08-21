import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OLLAMA_BASE_URL

WORKFLOW_MODEL_SMALL = "gpt-4o-mini"
WORKFLOW_MODEL_LARGE = "gpt-4o"

# WORKFLOW_MODEL_SMALL = "gemma4"
# WORKFLOW_MODEL_LARGE = "gemma4"

client = OpenAI(api_key=OPENAI_API_KEY)
# client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

def infer(messages, tools, schema, model=WORKFLOW_MODEL_SMALL, max_tokens=4096, schema_name="output"):
    """Call the LLM with tools available and a required output schema. Returns the raw message."""
    completion = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
        tools=tools,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "schema": schema, 
                "strict": True
            },
        },
    )

    return completion.choices[0].message

def run(messages, schema, tools=None, tool_fns=None, model=WORKFLOW_MODEL_SMALL, max_tokens=4096, schema_name="output", max_iterations=6):
    """
    Iterate: call infer, execute any tool calls, append results, call infer again.
    Returns the parsed JSON dict from the final message (once the model stops calling tools).
    Caps at `max_iterations` to prevent runaway tool-calling loops.
    """
    tools = tools or []
    tool_fns = tool_fns or {}
    conversation = list(messages)

    for _ in range(max_iterations):
        message = infer(conversation, tools, schema, model=model, max_tokens=max_tokens, schema_name=schema_name)

        if not message.tool_calls:
            return json.loads(message.content)

        conversation.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in message.tool_calls
            ],
        })

        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = tool_fns[tool_call.function.name](**args)

            content = result if isinstance(result, str) else json.dumps(result)

            conversation.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": content,
            })

    raise RuntimeError(
        f"Agent exceeded max_iterations ({max_iterations}) without producing a final response. "
        f"Model: {model}. Likely stuck in a tool-calling loop."
    )
