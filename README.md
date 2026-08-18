# LLM Eval Harness

## Description

A modular, provider- and dataset-agnostic harness for benchmarking LLMs. Plug in an LLM provider and a dataset, and the harness runs the eval in parallel, scores predictions, and reports accuracy alongside per-item results. Ships with an Anthropic provider and an MMLU dataset implementation.

## Tech Stack

![Image Alt](https://skillicons.dev/icons?i=python)

## Architecture

The harness is organized into three independent packages that do not import each other — `main.py` is the only place they are wired together:

- `llm/` — `Provider` ABC (`base.py`) and provider implementations (`anthropic.py`). Each provider exposes `model_name` and `infer(prompt) -> str`.
- `dataset/` — `Dataset` ABC (`base.py`) and dataset implementations (`mmlu.py`). Each dataset exposes `load`, `prompt_for`, `correct_answer`, `extract_prediction`, and `metadata`.
- `eval/` — Evaluation ops (`ops.py`) with retry/backoff on inference calls, and result analysis (`analyze.py`) for building the results table and printing summary metrics.
- `main.py` — Orchestrator. Instantiates a provider and dataset, runs the eval concurrently with `ThreadPoolExecutor`, writes the CSV, and prints the analysis.

Adding a new provider or dataset means dropping in a new subclass under `llm/` or `dataset/` and swapping it in `main.py` — no changes to `eval/` required.

## Features

- Pluggable providers and datasets behind small ABCs — swap either without touching the evaluation loop
- Parallel evaluation via `ThreadPoolExecutor` with exponential-backoff retries on inference failures
- Automatic prediction extraction, accuracy scoring, and error/unparsed-response accounting
- Per-item results exported to `eval_results/results_<model>.csv` (metadata, raw response, prediction, gold answer, correctness)
- Summary printout of model, dataset, item count, accuracy, unparsed responses, and API errors

## How to run the project?

1. Create and activate a virtual environment, then install dependencies (`anthropic`, `datasets`, `pandas`, `tqdm`, `python-dotenv`).
2. Create a `.env` file with:
   - `ANTHROPIC_API_KEY` — required for the Anthropic provider
   - `HF_TOKEN` — required to download the MMLU dataset from Hugging Face
3. In `main.py`, configure the provider (`AnthropicProvider(model=...)`) and the dataset (`MMLUDataset(sample_size=...)`) as needed.
4. Run `python main.py`. Results are written to `eval_results/results_<model>.csv` and a summary is printed to stdout.

## Author

[Dev J. Shah](https://github.com/busycaesar)
