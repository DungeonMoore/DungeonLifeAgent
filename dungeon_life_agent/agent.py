"""Implementación MVP del Dungeon Life Agent."""

from __future__ import annotations

import pathlib
import time
from dataclasses import dataclass
from typing import Iterable, Optional

import textwrap

from .config import AgentConfiguration, RoleProfile, load_config
from .knowledge import DocumentationIndex, SearchResult
from .mode_manager import ModeManager
from .metrics import MetricsRegistry
from .tools import ToolIntegration
from .memory import CollectiveMemory, MemoryRecord
from .pipelines import AssetPipelineNavigator
from .datasets import DatasetAnalysisAgent, DatasetPlan
from .templates import CollaborationTemplates
from .llm import LanguageModelClient
from .search_pipeline import PipelineTrace


@dataclass
class AgentResponse:
    """Estructura homogénea para las respuestas del agente."""

    mode: str
    role: Optional[str]
    summary: str
    highlights: list[str]
    references: list[str]
    debug_trace: Optional[str] = None

    def format_text(self, *, show_debug: bool = False) -> str:
        box_width = 96
        inner_width = box_width - 4

        def _wrap(text: str) -> list[str]:
            if not text.strip():
                return [""]
            prefix = len(text) - len(text.lstrip())
            body = text[prefix:]
            wrapper = textwrap.TextWrapper(
                width=inner_width,
                initial_indent=" " * prefix,
                subsequent_indent=" " * prefix,
            )
            return wrapper.wrap(body)

        def _wrap_bullet(text: str, bullet: str) -> list[str]:
            if not text.strip():
                return [bullet.strip()]
            return textwrap.wrap(
                text,
                width=inner_width,
                initial_indent=bullet,
                subsequent_indent=" " * len(bullet),
            )

        def _box_line(content: str) -> str:
            return f"║ {content.ljust(inner_width)} ║"

        def _section_title(title: str) -> str:
            label = f" {title} "
            filler = "─" * max(0, inner_width - len(label))
            return f"╟{label}{filler}╢"

        lines: list[str] = []
        header = f"Willow · {self.mode.capitalize()}"
        lines.append("╔" + "═" * (box_width - 2) + "╗")
        lines.append(_box_line(header))
        if self.role:
            lines.append(_box_line(f"Rol activo: {self.role}"))
        lines.append("╠" + "═" * (box_width - 2) + "╣")

        lines.append(_section_title("Resumen"))
        for row in _wrap(self.summary):
            lines.append(_box_line(row))

        if self.highlights:
            lines.append(_section_title("Puntos clave"))
            for item in self.highlights:
                for row in _wrap_bullet(item, "• "):
                    lines.append(_box_line(row))

        if self.references:
            lines.append(_section_title("Referencias"))
            for ref in self.references:
                for row in _wrap_bullet(ref, "- "):
                    lines.append(_box_line(row))

        if show_debug and self.debug_trace:
            lines.append(_section_title("Diagnóstico del pipeline"))
            for raw in self.debug_trace.splitlines() or [""]:
                for row in _wrap(raw):
                    lines.append(_box_line(row))

        lines.append("╚" + "═" * (box_width - 2) + "╝")
        return "\n".join(lines)


class DungeonLifeAgent:
    """Capa de orquestación que combina configuración, modos y conocimiento."""

    def __init__(
        self,
        documentation_path: str = "Documentacion",
        config_path: str | None = None,
        *,
        knowledge_index: DocumentationIndex | None = None,
        tool_integration: ToolIntegration | None = None,
        configuration: AgentConfiguration | None = None,
        mode_manager: ModeManager | None = None,
        metrics: MetricsRegistry | None = None,
        collective_memory: CollectiveMemory | None = None,
        pipeline_navigator: AssetPipelineNavigator | None = None,
        dataset_agent: DatasetAnalysisAgent | None = None,
        templates: CollaborationTemplates | None = None,
        language_model: LanguageModelClient | None = None,
    ) -> None:
        self.config = configuration or load_config(config_path)
        self.knowledge = knowledge_index or DocumentationIndex(documentation_path)
        self.mode_manager = mode_manager or ModeManager.from_config(self.config)
        self.tools = tool_integration or ToolIntegration()
        self.metrics = metrics or MetricsRegistry()
        self.memory = collective_memory or CollectiveMemory()
        self.pipelines = pipeline_navigator or AssetPipelineNavigator()
        self.dataset_agent = dataset_agent or DatasetAnalysisAgent()
        self.templates = templates or CollaborationTemplates()
        self.language_model = language_model

    # ------------------------------------------------------------------
    # Operaciones de alto nivel
    def query(self, message: str, *, mode: str = "consultor", role: Optional[str] = None, limit: int = 3) -> AgentResponse:
        self.mode_manager.ensure(mode, "query")
        role_profile = self.config.get_role(role)
        start = time.perf_counter()
        results = self.knowledge.search(message, limit=limit)
        self.metrics.record_search(mode, time.perf_counter() - start, len(results))
        trace = self.knowledge.last_search_trace()
        return self._build_response(
            mode=mode,
            role=role_profile,
            query=message,
            results=results,
            trace=trace,
        )

    def list_documents(self, *, mode: str = "consultor") -> list[str]:
        self.mode_manager.ensure(mode, "list_documents")
        return [str(path) for path in self.knowledge.list_documents()]

    def classify(self, message: str, *, mode: str = "taxonomico") -> AgentResponse:
        self.mode_manager.ensure(mode, "classify")
        start = time.perf_counter()
        results = self.knowledge.search(message, limit=5)
        self.metrics.record_search(mode, time.perf_counter() - start, len(results))
        trace = self.knowledge.last_search_trace()
        return self._build_taxonomy_response(mode=mode, results=results, trace=trace)

    def suggest_actions(self, message: str, *, mode: str = "colaborador", role: Optional[str] = None) -> AgentResponse:
        self.mode_manager.ensure(mode, "suggest_actions")
        role_profile = self.config.get_role(role)
        start = time.perf_counter()
        results = self.knowledge.search(message, limit=3)
        self.metrics.record_search(mode, time.perf_counter() - start, len(results))
        trace = self.knowledge.last_search_trace()
        return self._build_collaboration_response(
            mode=mode,
            role=role_profile,
            query=message,
            results=results,
            trace=trace,
        )

    def use_tool(self, name: str, *, mode: str = "colaborador", **kwargs) -> str:
        self.mode_manager.ensure(mode, "use_tools")
        if name == "list_directory":
            return "\n".join(self.tools.list_directory(kwargs["path"]))
        if name == "read_file":
            return self.tools.read_file(kwargs["path"], max_bytes=kwargs.get("max_bytes", 32_768))
        if name == "git_status":
            return self.tools.git_status(kwargs["path"])
        raise ValueError(f"Herramienta desconocida: {name}")

    def suggest_queries(self, prefix: str, *, mode: str = "consultor", limit: int = 5) -> list[str]:
        self.mode_manager.ensure(mode, "suggest_queries")
        return self.knowledge.suggest(prefix, limit=limit)

    def refresh_knowledge(self, *, mode: str = "colaborador", paths: Optional[Iterable[str | pathlib.Path]] = None) -> None:
        self.mode_manager.ensure(mode, "refresh_index")
        self.knowledge.refresh(paths)

    def get_metrics_report(self) -> str:
        return self.metrics.format_report()

    def metrics_snapshot(self) -> dict[str, float]:
        snapshot = self.metrics.snapshot()
        flat: dict[str, float] = {}
        for key, values in snapshot.items():
            for metric, value in values.items():
                flat[f"{key}.{metric}"] = float(value)
        return flat

    def capture_memory_event(
        self,
        *,
        channel: str,
        author: str,
        content: str,
        summary: str | None = None,
        tags: Iterable[str] | None = None,
        decisions: Iterable[str] | None = None,
        mode: str = "colaborador",
    ) -> MemoryRecord:
        self.mode_manager.ensure(mode, "capture_memory")
        record = self.memory.capture(
            channel=channel,
            author=author,
            content=content,
            summary=summary,
            tags=tuple(tags or ()),
            decisions=tuple(decisions or ()),
        )
        for decision in record.decisions:
            self.metrics.record_decision(identifier=record.identifier, mode=mode, description=decision)
        return record

    def search_memory(
        self,
        query: str,
        *,
        mode: str = "consultor",
        limit: int = 5,
        channels: Iterable[str] | None = None,
    ) -> list[MemoryRecord]:
        self.mode_manager.ensure(mode, "search_memory")
        return self.memory.search(query, limit=limit, channels=channels)

    def list_memory_channels(self, *, mode: str = "consultor") -> list[str]:
        self.mode_manager.ensure(mode, "search_memory")
        return self.memory.channels()

    def list_asset_pipelines(self, *, mode: str = "colaborador") -> list[str]:
        self.mode_manager.ensure(mode, "pipeline_navigator")
        return list(self.pipelines.available())

    def describe_asset_pipeline(self, name: str, *, mode: str = "colaborador") -> str:
        self.mode_manager.ensure(mode, "pipeline_navigator")
        pipeline = self.pipelines.get(name)
        return pipeline.describe()

    def plan_dataset_analysis(self, metadata: dict[str, str], *, mode: str = "colaborador") -> DatasetPlan:
        self.mode_manager.ensure(mode, "dataset_analysis")
        return self.dataset_agent.analyze(metadata)

    def list_templates(self, *, mode: str = "colaborador") -> list[str]:
        self.mode_manager.ensure(mode, "apply_templates")
        return self.templates.names()

    def apply_template(self, name: str, context: dict[str, str], *, mode: str = "colaborador") -> str:
        self.mode_manager.ensure(mode, "apply_templates")
        return self.templates.render(name, context)

    def register_productivity(self, *, role: str, tasks_completed: int, session_minutes: float, mode: str = "colaborador") -> None:
        self.mode_manager.ensure(mode, "record_productivity")
        self.metrics.record_productivity(role=role, tasks_completed=tasks_completed, minutes=session_minutes)

    def generate_with_model(self, prompt: str, *, mode: str = "colaborador", **kwargs) -> str:
        self.mode_manager.ensure(mode, "invoke_llm")
        if self.language_model is None:
            raise RuntimeError("No hay cliente de modelo configurado. Inicializa DungeonLifeAgent con language_model.")
        return self.language_model.generate(prompt, **kwargs)

    # ------------------------------------------------------------------
    # Construcción de respuestas
    def _build_response(
        self,
        *,
        mode: str,
        role: Optional[RoleProfile],
        query: str,
        results: list[SearchResult],
        trace: PipelineTrace | None = None,
    ) -> AgentResponse:
        if not results:
            summary = "No encontré información relacionada en la documentación actual."
            return AgentResponse(
                mode=mode,
                role=role.name if role else None,
                summary=summary,
                highlights=[],
                references=[],
                debug_trace=_format_debug_trace(trace) if trace else None,
            )

        best = results[0]
        tone = _select_tone(role)
        summary = _format_summary(best, tone=tone, query=query)
        highlights = [_format_highlight(result) for result in results]
        references = [
            f"{res.section.document_path.name} → {res.section.title or 'Introducción'}"
            for res in results
        ]
        return AgentResponse(
            mode=mode,
            role=role.name if role else None,
            summary=summary,
            highlights=highlights,
            references=references,
            debug_trace=_format_debug_trace(trace) if trace else None,
        )

    def _build_taxonomy_response(
        self,
        *,
        mode: str,
        results: list[SearchResult],
        trace: PipelineTrace | None,
    ) -> AgentResponse:
        if not results:
            summary = "No hay coincidencias para clasificar con la consulta proporcionada."
            return AgentResponse(
                mode=mode,
                role=None,
                summary=summary,
                highlights=[],
                references=[],
                debug_trace=_format_debug_trace(trace) if trace else None,
            )

        summary = "Mapa de secciones relevantes ordenadas por afinidad con la consulta."
        highlights = []
        references = []
        for item in results:
            path = item.section.document_path.name
            title = item.section.title or "Introducción"
            snippet = item.section.build_snippet(160)
            highlights.append(f"{path} › {title}: {snippet}")
            references.append(f"{path}#{title.replace(' ', '-')}")
        return AgentResponse(
            mode=mode,
            role=None,
            summary=summary,
            highlights=highlights,
            references=references,
            debug_trace=_format_debug_trace(trace) if trace else None,
        )

    def _build_collaboration_response(
        self,
        *,
        mode: str,
        role: Optional[RoleProfile],
        query: str,
        results: list[SearchResult],
    ) -> AgentResponse:
        base = self._build_response(
            mode=mode,
            role=role,
            query=query,
            results=results,
            trace=trace,
        )
        focus = ", ".join(role.priorities) if role else "entregables"  # type: ignore[attr-defined]
        action = f"Próximo paso sugerido: sintetiza hallazgos enfocados en {focus}."
        base.highlights.append(action)
        template_hint = self.templates.names()[0] if self.templates.names() else None
        if template_hint:
            base.highlights.append(f"Plantilla sugerida: usa '{template_hint}' para documentar avances.")
        return base


def _select_tone(role: Optional[RoleProfile]) -> str:
    if role is None:
        return "neutral"
    return role.tone


def _format_summary(result: SearchResult, *, tone: str, query: str) -> str:
    snippet = result.section.build_snippet(220)
    if tone == "inspirador":
        return f"Conectando tu consulta sobre '{query}', encontré una referencia clave: {snippet}"
    if tone == "tecnico":
        return f"Consulta '{query}' → Referencia prioritaria: {snippet}"
    if tone == "analitico":
        return f"Análisis para '{query}': {snippet}"
    if tone == "directo":
        return f"Respuesta directa a '{query}': {snippet}"
    return f"Resultado para '{query}': {snippet}"


def _format_highlight(result: SearchResult) -> str:
    title = result.section.title or "Introducción"
    location = result.section.document_path.name
    snippet = result.section.build_snippet(140)
    return f"{title} · {location} (score {result.score:.3f}) — {snippet}"


def _format_debug_trace(trace: PipelineTrace | None) -> str | None:
    if trace is None:
        return None

    def _format_value(value: object) -> str:
        if isinstance(value, float):
            return f"{value:.3f}"
        return str(value)

    lines: list[str] = []
    lines.append(f"Consulta: {trace.query}")
    config = trace.config_snapshot
    lines.append(
        "Parámetros principales → "
        f"α={trace.alpha_used:.2f}, N={config.fusion_top_n}, M={config.mmr_limit}, "
        f"λ={config.mmr_lambda:.2f}, β={config.role_bias:.2f}"
    )
    lines.append(f"Estrategia de embeddings: {config.embedding_strategy}")
    if trace.embedding_quality is not None:
        quality = trace.embedding_quality
        lines.append(
            "Calidad embeddings → "
            f"‖v‖̄={quality.mean_magnitude:.3f}, σ={quality.stdev_magnitude:.3f}, cos̄={quality.pairwise_cosine:.3f}"
        )

    lines.append("Etapas ejecutadas:")
    for index, stage in enumerate(trace.stages, start=1):
        lines.append(f"  {index}. {stage.name} ({stage.input_size}→{stage.output_size})")
        if stage.description:
            lines.append(f"     · {stage.description}")
        if stage.parameters:
            params = ", ".join(f"{key}={_format_value(value)}" for key, value in sorted(stage.parameters.items()))
            lines.append(f"     · Parámetros: {params}")
        for highlight in stage.highlights[:3]:
            extra = ""
            if highlight.extra:
                formatted = ", ".join(
                    f"{key}={_format_value(value)}" for key, value in sorted(highlight.extra.items())
                )
                extra = f" [{formatted}]"
            title = highlight.title or highlight.identifier
            lines.append(f"     • {title} (score={highlight.score:.3f}){extra}")

    lines.append("Selección final enviada al LLM:")
    for selection in trace.selections:
        title = selection.section.title or selection.section.document_path.name
        lines.append(
            "  • "
            f"{title} (score={selection.score:.3f}, lex={selection.lexical_score:.3f}, "
            f"sem={selection.semantic_score:.3f}, bias={selection.bias_applied:.3f})"
        )
    return "\n".join(lines)


__all__ = ["DungeonLifeAgent", "AgentResponse"]
