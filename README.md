# LLM Eval

## Description

A Colab notebook (`main.ipynb`) that benchmarks Anthropic Claude models against the [MMLU](https://huggingface.co/datasets/cais/mmlu) multiple-choice question dataset. It samples questions, prompts the model, parses its letter answer, scores accuracy, and saves per-question results to CSV.

## Tech Stack

![Image Alt](https://skillicons.dev/icons?i=python)

## Features

- Configurable model, dataset, and sample size (`MODEL`, `DATASET`, `SAMPLE_SIZE` in the config cell)
- Parallel evaluation via `ThreadPoolExecutor` with retry/backoff on API calls
- Automatic answer extraction and scoring (accuracy, unparsed responses, API errors)
- Results exported to `eval_results/results_<model>.csv` with subject, question, gold answer, prediction, raw response, and correctness

## How to run the project?

1. Open `main.ipynb` in [Google Colab](https://colab.research.google.com/github/busycaesar/LLM_Eval/blob/Master/main.ipynb) (or run locally with Jupyter).
2. Set an `ANTHROPIC_API_KEY` secret (Colab userdata, or adapt the client init for a local `.env`).
3. Adjust `MODEL`, `DATASET`, and `SAMPLE_SIZE` in the configuration cell as needed.
4. Run all cells. Results are saved as a CSV in `eval_results/`.

## Author

[Dev J. Shah](https://github.com/busycaesar)
