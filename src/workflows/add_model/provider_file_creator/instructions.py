INSTRUCTIONS = """\
# Provider File Writer

Write a Python file implementing an LLM Provider adapter for a specific provider.

## What you receive

- The provider name and model identifier.
- The exact target file path (where your file will be written).
- The base ABC source — this is your contract. Read every abstract member. Your class must implement all of them. Your `__init__` must match the abstract `__init__`'s argument names and order EXACTLY.
- The exact import line to use for the Provider ABC. Copy it verbatim into your file.
- SDK-specific inputs (a modern client-based example and a response-extraction expression).

## Hard requirements (validated after generation)

1. Define a class named `{Provider}Provider` (e.g. `OpenAIProvider`).
2. Class must inherit from the base ABC.
3. `__init__` arg names must match the abstract `__init__` EXACTLY — do not drop, add, or rename any.
4. Implement EVERY abstract member (methods and properties) of the base ABC.
5. Imports must resolve at runtime (no invented module names).

## Style

- Modern client-based SDKs only. Never deprecated module-level calls.
- Terse: no docstrings, no comments.
- Response objects: attribute access, never dict indexing.

## Output

Return only structured JSON with `content` = the full file source.
"""