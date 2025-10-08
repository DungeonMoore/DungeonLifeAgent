"""Navegador de pipelines creativos y técnicos definidos para el ecosistema DLE."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class PipelineStep:
    name: str
    description: str
    owner: str
    deliverables: tuple[str, ...]


@dataclass(frozen=True)
class Pipeline:
    name: str
    context: str
    stages: tuple[PipelineStep, ...]
    handoff_tools: tuple[str, ...]

    def describe(self) -> str:
        lines = [f"📦 Pipeline {self.name}"]
        lines.append(self.context)
        for index, stage in enumerate(self.stages, start=1):
            deliverables = ", ".join(stage.deliverables)
            lines.append(
                f"  {index}. {stage.name} · {stage.owner} — {stage.description} (Entregables: {deliverables})"
            )
        if self.handoff_tools:
            tools = ", ".join(self.handoff_tools)
            lines.append(f"Handoff y herramientas clave: {tools}")
        return "\n".join(lines)


class AssetPipelineNavigator:
    """Centraliza los pipelines requeridos por la Fase 3 del roadmap."""

    def __init__(self) -> None:
        self._pipelines: Mapping[str, Pipeline] = _build_default_pipelines()

    def available(self) -> Iterable[str]:
        return sorted(self._pipelines)

    def get(self, name: str) -> Pipeline:
        try:
            return self._pipelines[name]
        except KeyError as exc:
            available = ", ".join(self.available())
            raise ValueError(f"Pipeline desconocido '{name}'. Disponibles: {available}") from exc


def _build_default_pipelines() -> Mapping[str, Pipeline]:
    blender = Pipeline(
        name="Blender",
        context="Creación de assets 3D con traspaso limpio a motores en tiempo real.",
        stages=(
            PipelineStep(
                name="Bloqueo y layout",
                description="Definición de proporciones, silueta y escalado métrico en escena maestra.",
                owner="Artista 3D",
                deliverables=("scene.blend", "mallas_base"),
            ),
            PipelineStep(
                name="Detalle y texturizado",
                description="Esculpido de high poly, bake de mapas y texturas PBR exportadas.",
                owner="Artista 3D",
                deliverables=("texturas_PBR", "mapas_normales", "mapas_occlusion"),
            ),
            PipelineStep(
                name="Optimización y export",
                description="Reducción de polígonos, LODs y export a FBX/GLTF con naming Atlas.",
                owner="Técnico de assets",
                deliverables=("LOD_bundle", "asset_catalog.json"),
            ),
        ),
        handoff_tools=("Blender", "Substance 3D Painter", "Asset Validator"),
    )

    unreal = Pipeline(
        name="Unreal",
        context="Ingesta y montaje dentro de Unreal Engine con blueprinting estándar.",
        stages=(
            PipelineStep(
                name="Import y nomenclatura",
                description="Uso de DataSmith/importer, verificación de escalas y rutas de materiales.",
                owner="Technical Artist",
                deliverables=("/Game/Environments/...", "data_table_assets"),
            ),
            PipelineStep(
                name="Blueprint + LODs",
                description="Creación de blueprint base, sockets y LOD sync con tabla Atlas.",
                owner="Technical Artist",
                deliverables=("BP_Asset", "atlas_lods.json"),
            ),
            PipelineStep(
                name="Validación de performance",
                description="Test de perfilador, métricas de draw calls y verificación de iluminación.",
                owner="QA Técnica",
                deliverables=("perf_report.csv", "screenshots_validacion"),
            ),
        ),
        handoff_tools=("Unreal Engine", "Profiling Dashboard", "Atlas Sync"),
    )

    react_ts = Pipeline(
        name="React/TypeScript",
        context="Componentes UI del Atlas y paneles de control conectados a backend.",
        stages=(
            PipelineStep(
                name="Diseño funcional",
                description="Revisión con UX y definición de estados + datos requeridos.",
                owner="Diseñador UX",
                deliverables=("wireframes", "contrato_props.json"),
            ),
            PipelineStep(
                name="Implementación de componentes",
                description="Creación de componentes con Storybook + pruebas unitarias.",
                owner="Frontend Engineer",
                deliverables=("Component.tsx", "stories.tsx", "tests.tsx"),
            ),
            PipelineStep(
                name="Integración y despliegue",
                description="Conexión a backend, validación de accesibilidad y publicación.",
                owner="Frontend Engineer",
                deliverables=("integration_report.md", "bundle_metrics.json"),
            ),
        ),
        handoff_tools=("Storybook", "Playwright", "CI Atlas"),
    )

    python_backend = Pipeline(
        name="Python Backend",
        context="Servicios de datos y APIs que alimentan el ecosistema DLE.",
        stages=(
            PipelineStep(
                name="Modelado de dominio",
                description="Definición de entidades, esquemas y contratos de API con taxonomía.",
                owner="Backend Engineer",
                deliverables=("openapi.yaml", "schema_migration.sql"),
            ),
            PipelineStep(
                name="Implementación y pruebas",
                description="Servicios REST/gRPC, cobertura mínima 80% y validación de performance.",
                owner="Backend Engineer",
                deliverables=("service.py", "coverage_report.xml"),
            ),
            PipelineStep(
                name="Observabilidad y handoff",
                description="Dashboards, alertas SLO y documentación de despliegue.",
                owner="DevOps",
                deliverables=("grafana_dashboard.json", "runbook.md"),
            ),
        ),
        handoff_tools=("FastAPI", "Poetry", "Observability Stack"),
    )

    return {
        "blender": blender,
        "unreal": unreal,
        "react_ts": react_ts,
        "python_backend": python_backend,
    }


__all__ = ["AssetPipelineNavigator", "Pipeline", "PipelineStep"]

