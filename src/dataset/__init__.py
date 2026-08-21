import os
from dotenv import load_dotenv
from .base import Dataset
from .mmlu import MMLUDataset

load_dotenv()
_HF_TOKEN = os.getenv("HF_TOKEN")

def get_dataset(dataset_name: str, sample_size: int) -> Dataset:
    if dataset_name == "MMLU":
        return MMLUDataset(sample_size, _HF_TOKEN)
    raise RuntimeError(f"No dataset implemented yet for '{dataset_name}'.")
