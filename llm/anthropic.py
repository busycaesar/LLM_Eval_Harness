from dotenv import load_dotenv
from anthropic import Anthropic
import os
from .base import Provider

load_dotenv()

class AnthropicProvider(Provider):
    def __init__(self, model: str, max_tokens: int = 16):
        self._model = model
        self._max_tokens = max_tokens
        self._client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    @property
    def model_name(self) -> str:
        return self._model

    def infer(self, prompt: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in response.content if b.type == "text")
