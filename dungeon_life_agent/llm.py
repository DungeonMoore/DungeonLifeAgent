"""Lightweight clients for integrating local language models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


class LanguageModelClient(Protocol):
    """Minimal interface for language model clients."""

    def generate(self, prompt: str, **kwargs: Any) -> str:  # pragma: no cover - protocol
        ...


@dataclass
class OllamaClient:
    """HTTP client ready to work with local Ollama instances."""

    model: str
    host: str = "http://localhost:11434"

    def __post_init__(self) -> None:
        self._session = None

    def generate(self, prompt: str, **kwargs: Any) -> str:
        if self._session is None:
            import requests

            self._session = requests.Session()
        payload: dict[str, Any] = {
            "model": kwargs.get("model", self.model),
            "prompt": prompt,
            "stream": False,
        }
        options = kwargs.get("options")
        if isinstance(options, Mapping):
            payload["options"] = dict(options)
        response = self._session.post(
            f"{self.host.rstrip('/')}/api/generate",
            json=payload,
            timeout=kwargs.get("timeout", 120),
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")


class EchoLanguageModel:
    """Testing client that echoes prompts with a configurable suffix."""

    def generate(self, prompt: str, **kwargs: Any) -> str:
        suffix = kwargs.get("suffix", "[sin respuesta de modelo]")
        return f"{prompt}\n\n{suffix}"


@dataclass(frozen=True)
class OllamaServiceStatus:
    """Structured result for Ollama availability probes."""

    available: bool
    host: str
    model: str | None
    detail: str | None = None


def probe_ollama_service(
    *,
    host: str = "http://localhost:11434",
    configured_model: str | None = None,
    timeout: float = 2.0,
) -> OllamaServiceStatus:
    """Check whether an Ollama service is reachable and what model looks active.

    The probe first verifies the service responds and then attempts to infer
    a suitable model name from the running processes or the installed tags.
    """

    import requests

    base = host.rstrip("/")
    try:
        response = requests.get(f"{base}/api/version", timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - network failure
        return OllamaServiceStatus(False, host, configured_model, str(exc))

    model = configured_model

    try:
        running = requests.get(f"{base}/api/ps", timeout=timeout)
        running.raise_for_status()
        payload = running.json()
        active = next(
            (entry.get("name") for entry in payload.get("models", []) if entry.get("name")),
            None,
        )
        if active and not model:
            model = active
    except requests.RequestException:  # pragma: no cover - degraded fallback
        pass

    if model is None:
        try:
            tags = requests.get(f"{base}/api/tags", timeout=timeout)
            tags.raise_for_status()
            models = tags.json().get("models", [])
            model = next((entry.get("name") for entry in models if entry.get("name")), None)
        except requests.RequestException:  # pragma: no cover - degraded fallback
            pass

    return OllamaServiceStatus(True, host, model)


__all__ = [
    "LanguageModelClient",
    "OllamaClient",
    "EchoLanguageModel",
    "OllamaServiceStatus",
    "probe_ollama_service",
]
