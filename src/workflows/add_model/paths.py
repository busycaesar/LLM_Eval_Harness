from pathlib import Path


def _find_root() -> Path:
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / "src").is_dir():
            return current
        current = current.parent
    raise RuntimeError("Could not find project root (no src/ directory found).")

ROOT = _find_root()
SRC = ROOT / "src"
LLM_DIR = SRC / "llm"
LLM_BASE = LLM_DIR / "base.py"
PROVIDERS_DIR = LLM_DIR / "providers"

def provider_file(provider: str) -> Path:
    return PROVIDERS_DIR / f"{provider.lower()}.py"