"""Pruebas ligeras para validar la integración opcional con Ollama."""

from __future__ import annotations

import os
import sys
import pytest


def _ensure_project_path() -> None:
    """Añade el directorio del proyecto al path si aún no está presente."""

    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def _ollama_available() -> bool:
    """Comprueba si hay una instancia de Ollama escuchando en localhost."""

    import requests

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=1)
    except Exception:
        return False
    return response.ok


def test_ollama_connection_roundtrip() -> None:
    """Ejecuta una llamada real contra Ollama si está disponible."""

    if not _ollama_available():
        pytest.skip("Ollama no está disponible en localhost:11434")

    _ensure_project_path()
    from dungeon_life_agent.llm import OllamaClient

    client = OllamaClient(model="gemma3:4b")
    prompt = "Dame un resumen de una frase sobre Willow"
    response = client.generate(prompt, timeout=5)

    assert isinstance(response, str)
    assert response.strip(), "La respuesta de Ollama no debería estar vacía"


def test_agent_uses_ollama_when_available() -> None:
    """Verifica que el agente pueda delegar en Ollama si el servidor existe."""

    if not _ollama_available():
        pytest.skip("Ollama no está disponible en localhost:11434")

    _ensure_project_path()
    from dungeon_life_agent import DungeonLifeAgent
    from dungeon_life_agent.llm import OllamaClient

    agent = DungeonLifeAgent(language_model=OllamaClient(model="gemma3:4b"))
    output = agent.generate_with_model("Explica la memoria colectiva en una frase")

    assert isinstance(output, str)
    assert output.strip(), "El agente debe propagar la respuesta del LLM"


if __name__ == "__main__":  # pragma: no cover - uso manual
    _ensure_project_path()

    if not _ollama_available():
        print("Ollama no está disponible en localhost:11434. Inicialo con 'ollama serve'.")
        sys.exit(1)

    print("Ollama disponible. Ejecuta `pytest test_ollama_integration.py` para las pruebas completas.")