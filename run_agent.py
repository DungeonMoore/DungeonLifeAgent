"""Punto de entrada alternativo para ejecutar Willow con inicio automático de Ollama."""

from __future__ import annotations

import os

from dungeon_life_agent.cli import main as willow_main
from dungeon_life_agent.ollama_manager import create_ollama_manager


def main() -> int:
    """Delegar en la CLI oficial para que ambos comandos sean equivalentes."""
    # Al invocar `python run_agent.py` no queremos imprimir el banner dos veces.
    os.environ.setdefault("WILLOW_HIDE_BANNER", "1")

    # Iniciar Ollama automáticamente si no está disponible
    ollama_manager = create_ollama_manager(verbose=True)
    ollama_available = ollama_manager.ensure_running()

    if not ollama_available:
        print("[WARNING] Continuando sin Ollama. Algunas funcionalidades podrian no estar disponibles.")
        print("[INFO] Puedes iniciar Ollama manualmente con: ollama serve")

    return willow_main()


if __name__ == "__main__":
    raise SystemExit(main())
