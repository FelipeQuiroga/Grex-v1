from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path as _Path

import requests


@dataclass
class LLMConfig:
    provider: str
    model: str
    timeout_sec: int
    retries: int


# region agent log
def _agent_log(
    run_id: str,
    hypothesis_id: str,
    location: str,
    message: str,
    data: dict | None = None,
) -> None:
    """Pequeno logger para debug da sessão atual."""
    try:
        # Coloca o ficheiro de log na raiz do projeto mvp-validation
        log_path = _Path(__file__).resolve().parents[4] / "debug-a8a80a.log"
        payload = {
            "sessionId": "a8a80a",
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")
    except Exception:
        # Nunca deixamos o logging partir o fluxo principal
        pass


# endregion agent log


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
        url = "http://127.0.0.1:11434/api/generate"
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
            # region agent log
            _agent_log(
                run_id="run-e2",
                hypothesis_id="H2",
                location="e2.llm_client:generate_with_retry",
                message="generate attempt",
                data={"attempt": attempt, "max_retries": retries},
            )
            # endregion agent log
            return client.generate(prompt), True
        except requests.RequestException as exc:
            last_error = exc
            # region agent log
            _agent_log(
                run_id="run-e2",
                hypothesis_id="H2",
                location="e2.llm_client:generate_with_retry",
                message="generate attempt failed",
                data={"attempt": attempt, "error": str(exc)},
            )
            # endregion agent log
            time.sleep(1)
    if last_error:
        raise last_error
    return "", False
