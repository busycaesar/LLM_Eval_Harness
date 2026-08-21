import ast
import subprocess
import sys
from workflows import run, WORKFLOW_MODEL_LARGE
from workflows.utils import (
    abstract_methods,
    class_extends,
    class_methods,
    compile_check,
    find_class,
    init_args,
)
from .. import LLM_BASE, PROVIDERS_DIR, ROOT, provider_file
from .instructions import INSTRUCTIONS

FILE_WRITER_SCHEMA = {
    "type": "object",
    "properties": {
        "content": {"type": "string"},
    },
    "required": ["content"],
    "additionalProperties": False,
}

def _base_provider_class() -> ast.ClassDef | None:
    return find_class(ast.parse(LLM_BASE.read_text()), "Provider")

def _static_validate(content: str, provider: str) -> str | None:
    """AST + compile checks against the base ABC. No runtime execution."""
    class_name = f"{provider}Provider"

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return f"SyntaxError: {e}"

    cls = find_class(tree, class_name)
    if cls is None:
        return f"Expected class `{class_name}` not found."

    if not class_extends(cls, "Provider"):
        return f"Class `{class_name}` must inherit from Provider."

    base_cls = _base_provider_class()
    if base_cls is None:
        return "Base Provider class not found — cannot validate against contract."

    gen_args = init_args(cls)
    base_args = init_args(base_cls)
    if base_args and gen_args != base_args:
        return (
            f"Constructor args must match the base ABC's abstract __init__ exactly.\n"
            f"Base __init__: {base_args}\n"
            f"Generated __init__: {gen_args}"
        )

    missing = abstract_methods(base_cls) - class_methods(cls)

    if missing:
        return f"Missing implementations for abstract members: {sorted(missing)}"

    err = compile_check(content)
    if err:
        return f"Compile error: {err}"

    return None


def _import_validate(provider: str) -> str | None:
    """
    After writing the file, run a subprocess import to catch bad relative imports
    (e.g. `from .base_abc import Provider`) that compile fine but fail at runtime.
    """
    class_name = f"{provider}Provider"
    code = (
        f"import sys; sys.path.insert(0, {str(SRC := ROOT / 'src')!r}); "
        f"from llm.providers.{provider.lower()} import {class_name}"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if result.returncode != 0:
        return f"Import error: {result.stderr.strip()}"
    return None

def create_provider_file(provider: str, model: str, docs: dict) -> dict:
    target = provider_file(provider)

    if target.exists():
        return {"file_path": str(target.relative_to(ROOT)), "skipped": "already exists"}

    base_src = LLM_BASE.read_text()
    
    PROVIDERS_DIR.mkdir(parents=True, exist_ok=True)

    def _call_llm(feedback: str | None = None) -> dict:
        target_rel = str(target.relative_to(ROOT))
        base_import = f"from ..{LLM_BASE.stem} import Provider"
        user_msg = (
            f"Provider: {provider}\n"
            f"Model: {model}\n\n"
            f"Target file path: `{target_rel}`\n"
            f"Provider ABC import line (use EXACTLY this): `{base_import}`\n\n"
            f"Base ABC source:\n```python\n{base_src}\n```\n\n"
            f"SDK inputs:\n"
            f"- example_code:\n```python\n{docs['example_code']}\n```\n"
            f"- response_extraction: `{docs['response_extraction']}`\n"
        )
        if feedback:
            user_msg += f"\n\n**Previous attempt failed validation:**\n{feedback}\nFix and try again."
        return run(
            messages=[
                {"role": "system", "content": INSTRUCTIONS},
                {"role": "user", "content": user_msg},
            ],
            schema=FILE_WRITER_SCHEMA,
            schema_name="provider_file",
            model=WORKFLOW_MODEL_LARGE,
            max_tokens=2048,
        )

    feedback = None
    for _attempt in range(2):
        result = _call_llm(feedback=feedback)
        content = result["content"]

        static_err = _static_validate(content, provider)
        if static_err:
            feedback = static_err
            continue

        target.write_text(content)
        import_err = _import_validate(provider)
        if import_err:
            target.unlink()
            feedback = import_err
            continue

        return {"file_path": str(target.relative_to(ROOT)), "content": content}

    raise RuntimeError(
        f"Generated provider file for `{provider}` failed validation after retry.\n"
        f"Last error: {feedback}\n"
        f"Write `src/llm/providers/{provider.lower()}.py` manually before evaluating."
    )
