import argparse
from runner import run

parser = argparse.ArgumentParser(description="Run an LLM evaluation on a dataset.")
parser.add_argument("--provider", default="Anthropic", help="LLM provider (e.g. Anthropic)")
parser.add_argument("--model", default="claude-sonnet-5", help="Model identifier for the provider")
parser.add_argument("--dataset", default="MMLU", help="Dataset name (e.g. MMLU)")
parser.add_argument("--sample-size", type=int, default=10, help="Number of rows to sample from the dataset")
args = parser.parse_args()

run(args.provider, args.model, args.dataset, args.sample_size)