"""Gestión de modos operativos para el Dungeon Life Agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .config import AgentConfiguration, ModeProfile


@dataclass(frozen=True)
class Mode:
    name: str
    description: str
    permissions: frozenset[str]

    def allows(self, operation: str) -> bool:
        return operation in self.permissions


class ModeManager:
    """Valida operaciones disponibles según el modo activo."""

    def __init__(self, modes: Mapping[str, ModeProfile]):
        self._modes = {
            name: Mode(name=profile.name, description=profile.description, permissions=profile.permissions)
            for name, profile in modes.items()
        }

    @classmethod
    def from_config(cls, config: AgentConfiguration) -> "ModeManager":
        return cls(config.modes)

    def available_modes(self) -> Iterable[Mode]:
        return self._modes.values()

    def get(self, name: str) -> Mode:
        try:
            return self._modes[name]
        except KeyError as exc:
            available = ", ".join(self._modes)
            raise ValueError(f"Modo desconocido '{name}'. Modos disponibles: {available}") from exc

    def ensure(self, mode_name: str, operation: str) -> None:
        mode = self.get(mode_name)
        if not mode.allows(operation):
            raise PermissionError(
                f"La operación '{operation}' no está permitida en el modo '{mode_name}'."
            )


__all__ = ["Mode", "ModeManager"]
