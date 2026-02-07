from __future__ import annotations

import json
import time
from dataclasses import dataclass

import requests


@dataclass
class LLMConfig:
    provider: str
    model: str
    timeout_sec: int
    retries: int


class LLMClient:
    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def generate(self, prompt: str) -> str:
        if self.config.provider == "ollama":
            return self._call_ollama(prompt)
        if self.config.provider == "openai":
            return self._call_openai(prompt)
        raise ValueError(f"Unsupported provider: {self.config.provider}")

    def _call_ollama(self, prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        payload = {"model": self.config.model, "prompt": prompt, "stream": False}
        response = requests.post(url, json=payload, timeout=self.config.timeout_sec)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

    def _call_openai(self, prompt: str) -> str:
        raise ValueError("OpenAI provider not configured for this experiment.")


def generate_with_retry(client: LLMClient, prompt: str, retries: int) -> tuple[str, bool]:
    last_error = None
    for attempt in range(retries + 1):
        try:
            return client.generate(prompt), True
        except requests.RequestException as exc:
            last_error = exc
            time.sleep(1)
    if last_error:
        raise last_error
    return "", False
