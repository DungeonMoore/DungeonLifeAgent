"""Punto de entrada alternativo para ejecutar Willow."""

from __future__ import annotations

import os

from dungeon_life_agent.cli import main as willow_main


def main() -> int:
    """Delegar en la CLI oficial para que ambos comandos sean equivalentes."""
    # Al invocar `python run_agent.py` no queremos imprimir el banner dos veces.
    os.environ.setdefault("WILLOW_HIDE_BANNER", "1")
    return willow_main()


if __name__ == "__main__":
    raise SystemExit(main())
