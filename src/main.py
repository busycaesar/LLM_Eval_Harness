import argparse
import sys
from runner import run
from workflows import add_model_dispatch, chat_dispatch

def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="llm_eval CLI")
    subs = parser.add_subparsers(dest="command", required=True)

    run_p = subs.add_parser("run", help="Run an evaluation")
    run_p.add_argument("--provider", required=True, help="LLM provider (e.g. OpenAI)")
    run_p.add_argument("--model", required=True, help="Model identifier for the provider")
    run_p.add_argument("--dataset", default="MMLU", help="Dataset name (default: MMLU)")
    run_p.add_argument("--sample-size", type=int, default=10, help="Number of rows to sample")

    chat_p = subs.add_parser("chat", help="Natural-language request routed to a workflow")
    chat_p.add_argument("text", help="Natural-language request, e.g. 'please add gpt-4o-mini'")

    addm_p = subs.add_parser("add-model", help="Add a new LLM provider/model (deterministic)")
    addm_p.add_argument("model", help="Model identifier, e.g. 'gpt-4o-mini' or 'claude-sonnet-5'")

    return parser

def main() -> None:
    args = _make_parser().parse_args()

    try:
        if args.command == "run":
            run(args.provider, args.model, args.dataset, args.sample_size)
        elif args.command == "chat":
            chat_dispatch(args.text)
        elif args.command == "add-model":
            add_model_dispatch(args.model)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()