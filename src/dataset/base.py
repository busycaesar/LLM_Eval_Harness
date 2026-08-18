from abc import ABC, abstractmethod
from typing import Any

class Dataset(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Identifier used for output labels (e.g. the dataset name)."""

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
    def metadata(self, data: dict[str, Any]) -> dict[str, Any]:
        """Return context fields to include alongside eval results (e.g. subject, question)."""
