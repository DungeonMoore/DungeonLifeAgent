"""Clientes ligeros para integrar modelos de lenguaje locales."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


class LanguageModelClient(Protocol):
    """Interfaz mínima para clientes de modelos de lenguaje."""

    def generate(self, prompt: str, **kwargs: Any) -> str:  # pragma: no cover - protocolo
        ...


@dataclass
class OllamaClient:
    """Cliente HTTP listo para usarse con instancias locales de Ollama."""

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
    """Cliente de prueba que devuelve prompts enriquecidos (útil en tests)."""

    def generate(self, prompt: str, **kwargs: Any) -> str:
        suffix = kwargs.get("suffix", "[sin respuesta de modelo]")
        return f"{prompt}\n\n{suffix}"


__all__ = ["LanguageModelClient", "OllamaClient", "EchoLanguageModel"]

