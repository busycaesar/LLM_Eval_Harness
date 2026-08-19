# Contributing

Thanks for contributing to LLM Eval Harness. This guide covers the architectural rules of the codebase and how to extend it. For basic project setup and running instructions, see the [README](README.md).

## Architecture principles

These rules keep the harness modular and predictable. **Please read them before writing code.**

### 1. Packages do not import each other

`src/llm/`, `src/dataset/`, and `src/eval/` are independent. They must not import from each other. Wiring happens only in the composition roots:

- `src/main.py` — parses CLI args
- `src/runner.py` — imports from all three packages and wires them together
- `src/config.py` — reads secrets from the environment

If a function in one package needs behavior from another (e.g. an LLM client, a prompt builder), it takes it as an argument. Do not reach across.

### 2. One run per invocation

Every `python src/main.py` invocation evaluates **one** (provider, model, dataset) combination. Comparison across models happens by running `main.py` multiple times (a shell loop or driver script), not by looping providers in a single process.

### 3. CLI selects, `.env` stores secrets

- `--provider`, `--model`, `--dataset`, `--sample-size` are CLI arguments on `main.py`.
- API keys and external tokens (`ANTHROPIC_API_KEY`, `HF_TOKEN`) live in `.env` and are read by `src/config.py`.
- Tuning knobs shared across providers (e.g. `MAX_TOKENS`) live in `src/config.py`.
- Do not put provider names, model names, or dataset names in `.env`.

### 4. Concrete classes accept dependencies via constructor

Providers and datasets do not read environment variables themselves. Their constructors take the secrets they need as arguments; `src/config.py` is the only module that touches `os.getenv`.

## Adding a new LLM provider

1. **Create the class** in `src/llm/{provider_name}.py`, extending the `Provider` ABC:

   ```python
   # src/llm/openai.py
   from openai import OpenAI
   from .base import Provider

   class OpenAIProvider(Provider):
       def __init__(self, api_key: str, model: str, max_tokens: int):
           self._model = model
           self._max_tokens = max_tokens
           self._client = OpenAI(api_key=api_key)

       @property
       def model_name(self) -> str:
           return self._model

       def infer(self, prompt: str) -> str:
           # implementation
           ...
   ```

2. **Add the secret** to `src/config.py` if the provider needs one:

   ```python
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   ```

3. **Register in the factory** in `src/llm/__init__.py`:

   ```python
   from config import ANTHROPIC_API_KEY, OPENAI_API_KEY, MAX_TOKENS
   from .base import Provider
   from .anthropic import AnthropicProvider
   from .openai import OpenAIProvider

   def get_llm(provider_name: str, model: str) -> Provider:
       if provider_name == "Anthropic":
           if not ANTHROPIC_API_KEY:
               raise RuntimeError("ANTHROPIC_API_KEY is not set.")
           return AnthropicProvider(ANTHROPIC_API_KEY, model, MAX_TOKENS)
       if provider_name == "OpenAI":
           if not OPENAI_API_KEY:
               raise RuntimeError("OPENAI_API_KEY is not set.")
           return OpenAIProvider(OPENAI_API_KEY, model, MAX_TOKENS)
       raise RuntimeError(f"No provider implemented yet for '{provider_name}'.")
   ```

4. **Run it**: `python src/main.py --provider OpenAI --model gpt-4o`

## Adding a new dataset

1. **Create the class** in `src/dataset/{dataset_name}.py`, extending the `Dataset` ABC:

   ```python
   # src/dataset/gsm8k.py
   from datasets import load_dataset
   import re
   from .base import Dataset

   class GSM8KDataset(Dataset):
       _NAME = "gsm8k"

       def __init__(self, sample_size: int | None = None, hf_token: str | None = None):
           self._sample_size = sample_size
           self._hf_token = hf_token

       @property
       def name(self) -> str:
           return self._NAME

       def load(self): ...
       def prompt_for(self, row): ...
       def correct_answer(self, row): ...
       def extract_prediction(self, response): ...
       def metadata(self, row):
           return {"question": row["question"]}
   ```

   Every abstract method on `Dataset` must be implemented. `metadata(row)` should return only the context columns you want in the CSV output (not the entire row).

2. **Register in the factory** in `src/dataset/__init__.py`:

   ```python
   def get_dataset(dataset_name: str, sample_size: int) -> Dataset:
       if dataset_name == "MMLU":
           return MMLUDataset(sample_size, HF_TOKEN)
       if dataset_name == "GSM8K":
           return GSM8KDataset(sample_size, HF_TOKEN)
       raise RuntimeError(f"No dataset implemented yet for '{dataset_name}'.")
   ```

3. **Run it**: `python src/main.py --dataset GSM8K --sample-size 20`

## Commit conventions

Commits follow Conventional Commits:

```
<type>(<scope>): <description>
```

Types used in this repo: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `style`.

Scope is lowercase and matches the affected package or area (`llm`, `dataset`, `eval`, `runner`, `main`, `config`, `gitignore`, `readme`). Omit scope for truly cross-cutting changes.

Description is lowercase, present tense, no trailing period, ≤ 72 characters on the first line.

Examples:

- `feat(llm): add OpenAI provider`
- `refactor(eval): extract retry logic into helper`
- `chore(dataset): rename dataset factory arg`

Prefer small, focused commits over one large one — each commit should represent a single logical change reviewable on its own.

## Where things go — quick reference

| Kind of thing                                        | Where it lives                    |
| ---------------------------------------------------- | --------------------------------- |
| Provider implementation                              | `src/llm/{name}.py`               |
| Dataset implementation                               | `src/dataset/{name}.py`           |
| Provider/dataset registration                        | Factory in package `__init__.py`  |
| Evaluation logic (retries, run_evaluation, analysis) | `src/eval/`                       |
| Wiring (provider + dataset + eval)                   | `src/runner.py`                   |
| CLI parsing                                          | `src/main.py`                     |
| Secrets (env-loaded)                                 | `src/config.py`, read from `.env` |
| Shared tuning knobs (e.g. `MAX_TOKENS`)              | `src/config.py`                   |
| Docs and checklists                                  | `docs/`                           |
