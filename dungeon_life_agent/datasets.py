"""Agente auxiliar para analizar datasets y proponer flujos de validación."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class DatasetPlan:
    """Representa un plan de análisis recomendado."""

    overview: str
    quality_checks: tuple[str, ...]
    exploratory_steps: tuple[str, ...]
    automation: tuple[str, ...]

    def render(self) -> str:
        lines = [self.overview]
        if self.quality_checks:
            lines.append("\n✔️ Controles de calidad sugeridos:")
            lines.extend(f"  - {item}" for item in self.quality_checks)
        if self.exploratory_steps:
            lines.append("\n🔍 Exploración inicial:")
            lines.extend(f"  - {item}" for item in self.exploratory_steps)
        if self.automation:
            lines.append("\n🤖 Automatización propuesta:")
            lines.extend(f"  - {item}" for item in self.automation)
        return "\n".join(lines)


class DatasetAnalysisAgent:
    """Genera recomendaciones alineadas a la arquitectura de datos del proyecto."""

    def analyze(self, metadata: Mapping[str, str]) -> DatasetPlan:
        fmt = metadata.get("formato", metadata.get("format", "desconocido")).lower()
        domain = metadata.get("dominio", metadata.get("domain", "general")).lower()
        volume = metadata.get("tamanio", metadata.get("tam", metadata.get("rows", "0")))
        rows = _parse_int(volume)

        overview = self._build_overview(fmt=fmt, domain=domain, rows=rows)
        quality = self._quality_checks(fmt=fmt, rows=rows)
        exploratory = self._exploratory(domain=domain, rows=rows)
        automation = self._automation(fmt=fmt, domain=domain)
        return DatasetPlan(overview=overview, quality_checks=quality, exploratory_steps=exploratory, automation=automation)

    def _build_overview(self, *, fmt: str, domain: str, rows: int) -> str:
        base = f"Dataset detectado ({fmt or 'sin formato'})." if fmt else "Dataset sin formato declarado."
        if rows:
            base += f" Volumen estimado: {rows:,} registros."
        if domain != "general":
            base += f" Dominio: {domain}."
        base += " Se alineará con el Atlas de datos y contratos descritos en la arquitectura técnica."
        return base

    def _quality_checks(self, *, fmt: str, rows: int) -> tuple[str, ...]:
        checks: list[str] = []
        if fmt in {"csv", "tsv"}:
            checks.append("Validar delimitadores, encoding UTF-8 y consistencia de columnas versus esquema Atlas.")
        if fmt in {"parquet", "orc"}:
            checks.append("Verificar compresión columnar, particiones y versionado de esquema en Glue Catalog local.")
        if rows > 1_000_000:
            checks.append("Activar muestreo incremental y particionado para evitar cuellos en memoria.")
        checks.append("Ejecutar validaciones de integridad (nulos, duplicados, llaves foráneas) con Great Expectations local.")
        return tuple(checks)

    def _exploratory(self, *, domain: str, rows: int) -> tuple[str, ...]:
        steps: list[str] = []
        if domain in {"economia", "economía", "finanzas"}:
            steps.append("Calcular métricas de dispersión, correlaciones y detectar outliers con robust scaler.")
        elif domain in {"narrativa", "texto", "dialogos"}:
            steps.append("Generar nubes de palabras, análisis de sentimiento y frecuencia por personaje.")
        else:
            steps.append("Crear perfil exploratorio automático (pandas-profiling o ydata-profiling).")
        if rows:
            steps.append(f"Estimar tamaño de particiones para entrenamiento/validación considerando {rows:,} filas.")
        return tuple(steps)

    def _automation(self, *, fmt: str, domain: str) -> tuple[str, ...]:
        steps: list[str] = ["Registrar pipeline en orquestador (Prefect local) siguiendo convenciones del Atlas."]
        if fmt in {"csv", "tsv"}:
            steps.append("Programar limpieza incremental con watchdog para detectar nuevos drops en repositorio de datos.")
        if domain in {"vision", "imagenes", "imágenes"}:
            steps.append("Integrar validación de metadata EXIF y generación de thumbnails automáticos.")
        steps.append("Publicar artefactos en Dataset Registry del proyecto con versión semántica.")
        return tuple(steps)


def _parse_int(value: str) -> int:
    try:
        return int(str(value).replace(",", "").replace("_", "").strip())
    except (TypeError, ValueError):
        return 0


__all__ = ["DatasetAnalysisAgent", "DatasetPlan"]

