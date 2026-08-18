from datasets import load_dataset
import re

from .base import Dataset

class MMLUDataset(Dataset):
    _NAME = "cais/mmlu"
    _LETTERS = ["A", "B", "C", "D"]

    def __init__(self, sample_size: int | None = None, hf_token: str | None = None):
        self._sample_size = sample_size
        self._hf_token = hf_token

    @property
    def name(self) -> str:
        return self._NAME

    def load(self):
        dataset = load_dataset(self._NAME, "all", split="test", token=self._hf_token)
        if self._sample_size:
            dataset = dataset.shuffle(seed=0).select(range(min(self._sample_size, len(dataset))))
        return [dict(r) for r in dataset]

    def prompt_for(self, row):
        choices = "\n".join(f"{self._LETTERS[i]}. {c}" for i, c in enumerate(row["choices"]))
        return (
            "Answer the following multiple choice question.\n\n"
            f"Question: {row['question']}\n\n"
            f"{choices}\n\n"
            "Reply with only the letter of the correct answer."
        )

    def correct_answer(self, row):
        return self._LETTERS[row["answer"]]

    def extract_prediction(self, response):
        match = re.search(r"\b([ABCD])\b", response.strip().upper())
        return match.group(1) if match else None

    def metadata(self, row):
        return {"subject": row["subject"], "question": row["question"]}
