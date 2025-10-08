"""Utilidades de configuración para el Dungeon Life Agent."""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class RoleProfile:
    """Representa la configuración de un rol profesional."""

    name: str
    description: str
    tone: str
    priorities: tuple[str, ...]


@dataclass(frozen=True)
class ModeProfile:
    """Describe un modo operativo y sus permisos."""

    name: str
    description: str
    permissions: frozenset[str]


DEFAULT_CONFIG_PATH = pathlib.Path(__file__).resolve().parent / "config" / "default_config.json"


class ConfigurationError(RuntimeError):
    """Error lanzado cuando la configuración no es válida."""


class AgentConfiguration:
    """Wrapper ligero alrededor del diccionario de configuración."""

    def __init__(self, raw: Mapping[str, Any]):
        self._raw = dict(raw)
        self._roles = {
            name: RoleProfile(
                name=name,
                description=entry.get("description", ""),
                tone=entry.get("tone", "neutral"),
                priorities=tuple(entry.get("priorities", ())),
            )
            for name, entry in self._require(raw, "roles").items()
        }
        self._modes = {
            name: ModeProfile(
                name=name,
                description=entry.get("description", ""),
                permissions=frozenset(entry.get("permissions", ())),
            )
            for name, entry in self._require(raw, "modes").items()
        }

    @staticmethod
    def _require(raw: Mapping[str, Any], key: str) -> Mapping[str, Any]:
        try:
            value = raw[key]
        except KeyError as exc:
            raise ConfigurationError(f"Falta la clave obligatoria '{key}' en la configuración") from exc
        if not isinstance(value, Mapping):
            raise ConfigurationError(f"La clave '{key}' debe ser un mapeo, se recibió: {type(value)!r}")
        return value

    @property
    def raw(self) -> Mapping[str, Any]:
        return dict(self._raw)

    @property
    def roles(self) -> Mapping[str, RoleProfile]:
        return dict(self._roles)

    @property
    def modes(self) -> Mapping[str, ModeProfile]:
        return dict(self._modes)

    def get_role(self, name: Optional[str]) -> Optional[RoleProfile]:
        if name is None:
            return None
        return self._roles.get(name)

    def get_mode(self, name: str) -> ModeProfile:
        try:
            return self._modes[name]
        except KeyError as exc:
            raise ConfigurationError(f"Modo desconocido: {name}") from exc


def load_config(path: Optional[str | pathlib.Path] = None) -> AgentConfiguration:
    """Carga el archivo de configuración YAML.

    Si no se especifica ruta se utiliza la configuración por defecto incluida
    en el paquete.
    """

    config_path = pathlib.Path(path) if path else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
    if config_path.suffix.lower() in {".yaml", ".yml"}:
        raise ConfigurationError(
            "El MVP utiliza archivos JSON para la configuración. Convierte tu YAML a JSON o usa default_config.json."
        )
    with config_path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    return AgentConfiguration(data)


__all__ = ["load_config", "AgentConfiguration", "RoleProfile", "ModeProfile", "ConfigurationError"]
