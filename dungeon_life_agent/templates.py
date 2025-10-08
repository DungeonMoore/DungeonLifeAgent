"""Plantillas de colaboración controladas para el modo colaborador."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class CollaborationTemplate:
    name: str
    description: str
    placeholders: tuple[str, ...]
    body: str

    def render(self, context: Mapping[str, str]) -> str:
        missing = [field for field in self.placeholders if field not in context]
        if missing:
            required = ", ".join(missing)
            raise ValueError(f"Faltan campos requeridos para la plantilla: {required}")
        return self.body.format(**context)


class CollaborationTemplates:
    """Catálogo de plantillas disponibles para el modo colaborador."""

    def __init__(self, templates: Iterable[CollaborationTemplate] | None = None):
        self._templates = {template.name: template for template in (templates or _default_templates())}

    def names(self) -> list[str]:
        return sorted(self._templates)

    def get(self, name: str) -> CollaborationTemplate:
        try:
            return self._templates[name]
        except KeyError as exc:
            available = ", ".join(self.names())
            raise ValueError(f"Plantilla desconocida '{name}'. Disponibles: {available}") from exc

    def render(self, name: str, context: Mapping[str, str]) -> str:
        template = self.get(name)
        return template.render(context)


def _default_templates() -> tuple[CollaborationTemplate, ...]:
    return (
        CollaborationTemplate(
            name="bitacora_sesion",
            description="Resumen operativo para registrar decisiones clave por rol.",
            placeholders=("rol", "objetivo", "decisiones", "seguimiento"),
            body=(
                "# Bitácora de sesión ({rol})\n\n"
                "## Objetivo\n{objetivo}\n\n"
                "## Decisiones relevantes\n{decisiones}\n\n"
                "## Seguimiento\n{seguimiento}\n"
            ),
        ),
        CollaborationTemplate(
            name="plan_entrega",
            description="Checklist de entregables y responsables para iteración quincenal.",
            placeholders=("iteracion", "entregables", "riesgos", "responsables"),
            body=(
                "# Plan de entrega {iteracion}\n\n"
                "### Entregables prioritarios\n{entregables}\n\n"
                "### Riesgos\n{riesgos}\n\n"
                "### Responsables\n{responsables}\n"
            ),
        ),
        CollaborationTemplate(
            name="handoff_asset",
            description="Formato estructurado para traspaso de asset entre pipelines.",
            placeholders=("asset", "pipeline", "checklist", "notas"),
            body=(
                "# Handoff de asset\n"
                "- Asset: {asset}\n"
                "- Pipeline: {pipeline}\n\n"
                "## Checklist validada\n{checklist}\n\n"
                "## Notas adicionales\n{notas}\n"
            ),
        ),
    )


__all__ = ["CollaborationTemplate", "CollaborationTemplates"]

