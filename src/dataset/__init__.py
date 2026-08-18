from config import HF_TOKEN
from .base import Dataset
from .mmlu import MMLUDataset

def get_dataset(dataset_name: str, sample_size: int) -> Dataset:
    if dataset_name == "MMLU":
        return MMLUDataset(sample_size, HF_TOKEN)
    raise RuntimeError(f"No dataset implemented yet for '{dataset_name}'.")
