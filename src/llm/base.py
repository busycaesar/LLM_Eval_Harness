from abc import ABC, abstractmethod

class Provider(ABC):
    @abstractmethod
    def __init__(self, api_key: str, model: str, max_tokens: int):
        """Provider constructor contract: takes api_key, model identifier, and max_tokens cap."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """The model identifier this provider is configured to call (e.g. "claude-sonnet-5")."""

    @abstractmethod
    def infer(self, prompt: str) -> str:
        """Send the prompt to the LLM and return the raw text response."""