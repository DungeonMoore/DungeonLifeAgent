"""Pruebas del modo headless de la interfaz gráfica."""

from __future__ import annotations

import subprocess
import sys

from dungeon_life_agent.gui import run_headless_query


def test_headless_query_returns_craft_definition():
    output = run_headless_query("sabes que es CRAFT?")
    assert "Creative Framework for Augmented Fantasy Teams" in output


def test_cli_allows_headless_query(tmp_path):
    result = subprocess.run(
        [sys.executable, "run_gui.py", "--ask", "sabes que es CRAFT?", "--no-gui"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Creative Framework for Augmented Fantasy Teams" in result.stdout
    assert result.stderr == ""
