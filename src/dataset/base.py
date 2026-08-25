from abc import ABC, abstractmethod
from typing import Any

class Dataset(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Identifier used for output labels (e.g. the dataset name)."""

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        """Max tokens per LLM response for this dataset (e.g. 16 for MCQ, higher for open-ended)."""

    @abstractmethod
    def load(self) -> list[dict[str, Any]]:
        """Return the dataset to evaluate."""

    @abstractmethod
    def prompt_for(self, data: dict[str, Any]) -> str:
        """Build the prompt to send to the LLM for this data."""

    @abstractmethod
    def correct_answer(self, data: dict[str, Any]) -> str:
        """Return the ground-truth answer for this data."""

    @abstractmethod
    def extract_prediction(self, response: str) -> str | None:
        """Parse the LLM's raw response into a comparable answer, or None if unparseable."""

    @abstractmethod
    def is_correct(self, prediction: str | None, correct_answer: str) -> bool:
        """
        Decide whether `prediction` counts as correct against `correct_answer`.
        """

    @abstractmethod
    def metadata(self, data: dict[str, Any]) -> dict[str, Any]:
        """Return context fields to include alongside eval results (e.g. subject, question)."""
