from datasets import load_dataset
from dotenv import load_dotenv
import os
import re

load_dotenv()

DATASET = "cais/mmlu"
SAMPLE_SIZE = 10
LETTERS = ["A", "B", "C", "D"]

def get_dataset(sample_size = SAMPLE_SIZE):
    dataset = load_dataset(DATASET, "all", split="test", token=os.getenv("HF_TOKEN"))

    if SAMPLE_SIZE:
        dataset = dataset.shuffle(seed=0).select(range(min(sample_size, len(dataset))))

    rows = [dict(r) for r in dataset]

    return rows

def get_prompt_for_data(row):
    choices = "\n".join(f"{LETTERS[i]}. {c}" for i, c in enumerate(row["choices"]))
    return (
        "Answer the following multiple choice question.\n\n"
        f"Question: {row['question']}\n\n"
        f"{choices}\n\n"
        "Reply with only the letter of the correct answer."
    )

def extract_prediction(response):
    match = re.search(r"\b([ABCD])\b", response.strip().upper())
    return match.group(1) if match else None