"""Gestor de servicios para controlar el ciclo de vida de Ollama."""

from __future__ import annotations

import atexit
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from .llm import probe_ollama_service


class OllamaManager:
    """Gestor que controla el inicio, verificación y parada de Ollama."""

    def __init__(
        self,
        ollama_path: Optional[str] = None,
        host: str = "http://localhost:11434",
        model: str = "gemma3:4b",
        auto_start: bool = True,
        verbose: bool = False,
    ) -> None:
        self.ollama_path = ollama_path or self._find_ollama_path()
        self.host = host
        self.model = model
        self.auto_start = auto_start
        self.verbose = verbose
        self._ollama_process: Optional[subprocess.Popen[bytes]] = None
        self._started_by_us = False

        # Registrar limpieza al salir
        atexit.register(self.stop)

    def _find_ollama_path(self) -> Optional[str]:
        """Busca la instalación de Ollama en rutas comunes."""
        common_paths = [
            "ollama",  # Si está en PATH
            "/usr/local/bin/ollama",
            "/usr/bin/ollama",
            str(Path.home() / ".local" / "bin" / "ollama"),
            "C:\\Program Files\\Ollama\\ollama.exe",  # Windows
            str(Path.home() / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"),
        ]

        for path in common_paths:
            if self._is_ollama_executable(path):
                return path

        return None

    def _is_ollama_executable(self, path: str) -> bool:
        """Verifica si la ruta apunta a un ejecutable válido de Ollama."""
        try:
            # Para Windows, usar 'ollama --version'
            # Para Unix-like, usar 'ollama --version'
            result = subprocess.run(
                [path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0 and "ollama" in result.stdout.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False

    def is_available(self) -> bool:
        """Verifica si Ollama está disponible y respondiendo."""
        try:
            status = probe_ollama_service(host=self.host, configured_model=self.model)
            return status.available
        except Exception:
            return False

    def ensure_running(self) -> bool:
        """Asegura que Ollama esté ejecutándose, iniciándolo si es necesario."""
        if self.is_available():
            if self.verbose:
                print(f"[OK] Ollama ya esta disponible en {self.host}")
            return True

        if not self.auto_start:
            if self.verbose:
                print("[ERROR] Ollama no esta disponible y auto_start esta deshabilitado")
            return False

        return self.start()

    def start(self) -> bool:
        """Inicia el servicio de Ollama."""
        if self.ollama_path is None:
            print("[ERROR] No se encontro Ollama instalado en el sistema")
            print("[INFO] Instala Ollama desde https://ollama.ai/download")
            return False

        if self._ollama_process is not None:
            if self.verbose:
                print("[WARNING] Ollama ya esta siendo gestionado por este proceso")
            return True

        try:
            if self.verbose:
                print(f"[INFO] Iniciando Ollama desde: {self.ollama_path}")
                print("[INFO] Ejecutando: ollama serve")

            stdout_target = None if self.verbose else subprocess.DEVNULL
            stderr_target = None if self.verbose else subprocess.DEVNULL

            # Iniciar Ollama como proceso en segundo plano
            self._ollama_process = subprocess.Popen(
                [self.ollama_path, "serve"],
                stdout=stdout_target,
                stderr=stderr_target,
            )

            self._started_by_us = True

            # Esperar a que esté disponible
            if self.verbose:
                print("[INFO] Esperando a que Ollama este listo...")

            for attempt in range(30):  # Máximo 30 segundos
                time.sleep(1)
                if self.is_available():
                    if self.verbose:
                        print(f"[OK] Ollama iniciado correctamente en {self.host}")
                        print(f"[INFO] Modelo configurado: {self.model}")
                    return True

                if self._ollama_process and self._ollama_process.poll() is not None:
                    if self.verbose:
                        return_code = self._ollama_process.returncode
                        print(
                            "[ERROR] Ollama finalizo inesperadamente"
                            + (f" (codigo {return_code})" if return_code is not None else "")
                        )
                    self.stop()
                    return False

            print("[ERROR] Timeout esperando a que Ollama este disponible")
            self.stop()
            return False

        except Exception as e:
            print(f"[ERROR] Error iniciando Ollama: {e}")
            self._ollama_process = None
            return False

    def stop(self) -> None:
        """Detiene el proceso de Ollama si fue iniciado por nosotros."""
        if self._ollama_process and self._started_by_us:
            if self.verbose:
                print("[INFO] Deteniendo proceso de Ollama...")

            try:
                if self._ollama_process.poll() is None:
                    self._ollama_process.terminate()
                    # Esperar hasta 5 segundos a que termine
                    self._ollama_process.wait(timeout=5)
                    if self.verbose:
                        print("[OK] Ollama detenido correctamente")
                elif self.verbose:
                    print("[INFO] Ollama ya se encontraba detenido")
            except subprocess.TimeoutExpired:
                if self.verbose:
                    print("[WARNING] Forzando terminacion de Ollama...")
                self._ollama_process.kill()
            except Exception as e:
                print(f"[WARNING] Error deteniendo Ollama: {e}")

        self._ollama_process = None
        self._started_by_us = False

    def get_status(self) -> dict:
        """Obtiene el estado actual de Ollama."""
        available = self.is_available()

        return {
            "available": available,
            "host": self.host,
            "model": self.model,
            "ollama_path": self.ollama_path,
            "managed_by_us": self._started_by_us,
            "process_alive": self._ollama_process is not None and self._ollama_process.poll() is None,
        }


def create_ollama_manager(
    model: str = "gemma3:4b",
    auto_start: bool = True,
    verbose: bool = True,
) -> OllamaManager:
    """Función de conveniencia para crear un gestor de Ollama con configuración típica."""
    return OllamaManager(
        model=model,
        auto_start=auto_start,
        verbose=verbose,
    )
