from abc import ABC, abstractmethod

class Provider(ABC):
    @property
    @abstractmethod
    def model_name(self) -> str:
        """The model identifier this provider is configured to call (e.g. "claude-sonnet-5")."""

    @abstractmethod
    def infer(self, prompt: str) -> str:
        """Send the prompt to the LLM and return the raw text response."""