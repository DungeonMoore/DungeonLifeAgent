"""Integraciones seguras y de solo lectura para el MVP del agente."""

from __future__ import annotations

import pathlib
import subprocess
from typing import Iterable, List


class ToolIntegration:
    """Herramientas básicas permitidas en el MVP."""

    def list_directory(self, path: str | pathlib.Path) -> list[str]:
        target = pathlib.Path(path).expanduser().resolve()
        if not target.exists():
            raise FileNotFoundError(f"No existe el directorio: {target}")
        return sorted(item.name for item in target.iterdir())

    def read_file(self, path: str | pathlib.Path, max_bytes: int = 32_768) -> str:
        file_path = pathlib.Path(path).expanduser().resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"No existe el archivo: {file_path}")
        if file_path.is_dir():
            raise IsADirectoryError(f"La ruta solicitada es un directorio: {file_path}")
        data = file_path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="replace")

    def git_status(self, repo_path: str | pathlib.Path) -> str:
        repo = pathlib.Path(repo_path).expanduser().resolve()
        result = subprocess.run(
            ["git", "-C", str(repo), "status", "--short"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "No se pudo obtener el estado de git")
        return result.stdout.strip()


__all__ = ["ToolIntegration"]
