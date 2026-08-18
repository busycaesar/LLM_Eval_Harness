from anthropic import Anthropic

from .base import Provider

class AnthropicProvider(Provider):
    def __init__(self, api_key: str, model: str, max_tokens: int):
        self._model = model
        self._max_tokens = max_tokens
        self._client = Anthropic(api_key=api_key)

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
