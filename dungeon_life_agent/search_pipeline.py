"""Arquitectura definitiva del pipeline de inferencia de alta fidelidad."""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Protocol, Sequence, TYPE_CHECKING

from .embedding_gemma import EmbeddingGemma

try:  # Import opcional para compatibilidad con el nuevo sistema avanzado
    from .advanced_embeddings import EmbeddingQuality
except Exception:  # pragma: no cover - dependencia opcional
    EmbeddingQuality = None  # type: ignore


class _SupportsEmbed(Protocol):
    """Contrato mínimo requerido por el pipeline para generar embeddings."""

    def embed(self, texts: Iterable[str]):
        ...

if TYPE_CHECKING:  # pragma: no cover
    from .knowledge import DocumentSection, SearchResult


@dataclass(frozen=True)
class PipelineSelection:
    """Representa un fragmento listo para el LLM con trazabilidad completa."""

    section: "DocumentSection"
    chunk_text: str
    score: float
    lexical_score: float
    semantic_score: float
    bias_applied: float


@dataclass(frozen=True)
class StageHighlight:
    """Resumen compacto de un elemento producido durante una etapa del pipeline."""

    identifier: str
    title: str
    score: float
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StageReport:
    """Detalle de ejecución de una etapa específica del pipeline."""

    name: str
    description: str
    input_size: int
    output_size: int
    parameters: dict[str, Any] = field(default_factory=dict)
    highlights: list[StageHighlight] = field(default_factory=list)


@dataclass
class PipelineTrace:
    """Trazabilidad completa de una búsqueda, lista para análisis o prompts."""

    query: str
    alpha_used: float
    config_snapshot: "SearchPipelineConfig"
    stages: list[StageReport]
    selections: list[PipelineSelection]
    embedding_quality: "EmbeddingQuality | None"

    def to_prompt(self, *, max_items_per_stage: int = 3) -> str:
        """Construye una representación textual apta para un prompt de LLM."""

        lines: list[str] = []
        lines.append("### Consulta Analizada")
        lines.append(f"- Texto: {self.query}")
        lines.append(
            "- Parámetros clave: "
            f"α={self.alpha_used:.2f}, N={self.config_snapshot.fusion_top_n}, "
            f"M={self.config_snapshot.mmr_limit}, λ={self.config_snapshot.mmr_lambda:.2f}, "
            f"β={self.config_snapshot.role_bias:.2f}"
        )
        lines.append("- Estrategia de embeddings: " + self.config_snapshot.embedding_strategy)
        if self.embedding_quality is not None:
            lines.append(
                "- Calidad de embeddings: "
                f"‖v‖̄={self.embedding_quality.mean_magnitude:.3f}, "
                f"σ={self.embedding_quality.stdev_magnitude:.3f}, "
                f"cos̄={self.embedding_quality.pairwise_cosine:.3f}"
            )

        lines.append("\n### Etapas del Pipeline")
        for position, stage in enumerate(self.stages, start=1):
            lines.append(
                f"{position}. {stage.name} ({stage.input_size}→{stage.output_size})"
            )
            if stage.description:
                lines.append(f"   {stage.description}")
            if stage.parameters:
                ordered = sorted(stage.parameters.items())
                params = ", ".join(f"{key}={value}" for key, value in ordered)
                lines.append(f"   Parámetros: {params}")
            highlights = stage.highlights[: max_items_per_stage]
            for highlight in highlights:
                lines.append(
                    f"   - {highlight.title or highlight.identifier}"
                    f" (score={highlight.score:.3f})"
                )
                if highlight.extra:
                    extra_ordered = sorted(highlight.extra.items())
                    for key, value in extra_ordered:
                        lines.append(f"       · {key}: {value}")

        lines.append("\n### Selección Final")
        for selection in self.selections:
            title = selection.section.title or selection.section.document_path.name
            lines.append(
                f"- {title} (score={selection.score:.3f}, "
                f"lex={selection.lexical_score:.3f}, sem={selection.semantic_score:.3f}, "
                f"bias={selection.bias_applied:.3f})"
            )
        return "\n".join(lines)


@dataclass
class SearchPipelineConfig:
    """Configura cada etapa del pipeline de inferencia."""

    alpha: float = 0.6  # fusión híbrida BM25 + Gemma
    lexical_top_k: int = 200
    fusion_top_n: int = 50
    mmr_lambda: float = 0.8
    mmr_limit: int = 20
    rrf_k: int = 60
    chunk_size_tokens: int = 400
    chunk_overlap_tokens: int = 40
    role_bias: float = 0.05
    final_context_size: int = 5
    embedding_strategy: str = "auto"


class HybridSearchPipeline:
    """Implementa el flujo BM25 → RRF → MMR → Gemma descrito por el Arquitecto."""

    def __init__(
        self,
        embedder: _SupportsEmbed | None = None,
        config: SearchPipelineConfig | None = None,
    ) -> None:
        self.embedder: _SupportsEmbed = embedder or EmbeddingGemma()
        self.config = config or SearchPipelineConfig()
        self.embedding_quality: EmbeddingQuality | None = None
        self.last_trace: PipelineTrace | None = None

    # ------------------------------------------------------------------
    def search(
        self,
        query: str,
        candidates: Sequence["SearchResult"],
        *,
        limit: int,
        role: str | None = None,
        alpha_override: float | None = None,
    ) -> list[PipelineSelection]:
        self.last_trace = None
        stages: list[StageReport] = []
        if not candidates:
            return []

        alpha = self._clamp_alpha(alpha_override if alpha_override is not None else self.config.alpha)
        lexical_ranking = list(candidates)
        lexical_highlights = [
            StageHighlight(
                identifier=result.section.identifier,
                title=result.section.title or result.section.document_path.name,
                score=result.score,
                extra={
                    "documento": result.section.document_path.name,
                    "nivel": result.section.heading_level,
                },
            )
            for result in lexical_ranking[:5]
        ]
        stages.append(
            StageReport(
                name="Recuperación Léxica",
                description="Resultados iniciales BM25/TF-IDF",
                input_size=len(candidates),
                output_size=len(lexical_ranking),
                parameters={"top_k": self.config.lexical_top_k},
                highlights=lexical_highlights,
            )
        )
        fusion = self._apply_rrf(lexical_ranking)
        if not fusion:
            return []

        fusion_highlights = [
            StageHighlight(
                identifier=result.section.identifier,
                title=result.section.title or result.section.document_path.name,
                score=result.score,
                extra={"rrf": result.score},
            )
            for result in fusion[:5]
        ]
        stages.append(
            StageReport(
                name="Fusión Recíproca",
                description="RRF para equilibrar rankings parciales",
                input_size=len(lexical_ranking),
                output_size=len(fusion),
                parameters={"k": self.config.rrf_k},
                highlights=fusion_highlights,
            )
        )

        query_embedding = self._generate_embeddings([query])
        query_vector = query_embedding[0]

        sections_for_mmr = fusion[: self.config.fusion_top_n]
        section_texts = [self._section_to_text(candidate.section) for candidate in sections_for_mmr]
        section_vectors = self._generate_embeddings(section_texts)
        similarities = [_cosine_similarity(query_vector, vector) for vector in section_vectors]
        mmr_indices = self._apply_mmr(section_vectors, similarities)
        diversified_sections = [sections_for_mmr[index] for index in mmr_indices]

        mmr_highlights = [
            StageHighlight(
                identifier=sections_for_mmr[index].section.identifier,
                title=sections_for_mmr[index].section.title
                or sections_for_mmr[index].section.document_path.name,
                score=similarities[index],
                extra={
                    "rank": position + 1,
                    "mmr_score": round(similarities[index], 4),
                    "lexico": round(sections_for_mmr[index].score, 4),
                },
            )
            for position, index in enumerate(mmr_indices[:5])
        ]
        stages.append(
            StageReport(
                name="MMR Diversificación",
                description="Selecciona secciones diversas mediante Maximal Marginal Relevance",
                input_size=len(sections_for_mmr),
                output_size=len(diversified_sections),
                parameters={
                    "N": self.config.fusion_top_n,
                    "M": self.config.mmr_limit,
                    "λ": self.config.mmr_lambda,
                },
                highlights=mmr_highlights,
            )
        )

        chunk_candidates: list[_ChunkCandidate] = []
        for candidate in diversified_sections:
            chunks = self._chunk_section(candidate.section)
            for chunk in chunks:
                chunk_candidates.append(
                    _ChunkCandidate(
                        section=candidate.section,
                        chunk_text=chunk,
                        lexical_score=candidate.score,
                    )
                )

        if not chunk_candidates:
            return []

        chunk_highlights = [
            StageHighlight(
                identifier=candidate.section.identifier,
                title=candidate.section.title or candidate.section.document_path.name,
                score=float(len(candidate.chunk_text)),
                extra={"tokens": _count_tokens(candidate.chunk_text)},
            )
            for candidate in chunk_candidates[:5]
        ]
        stages.append(
            StageReport(
                name="Segmentación",
                description="División en fragmentos listos para embeddings",
                input_size=len(diversified_sections),
                output_size=len(chunk_candidates),
                parameters={
                    "chunk_tokens": self.config.chunk_size_tokens,
                    "overlap": self.config.chunk_overlap_tokens,
                },
                highlights=chunk_highlights,
            )
        )

        chunk_texts = [candidate.chunk_text for candidate in chunk_candidates]
        chunk_vectors = self._generate_embeddings(chunk_texts)
        if EmbeddingQuality is not None and hasattr(self.embedder, "quality_report"):
            try:
                self.embedding_quality = self.embedder.quality_report(chunk_vectors)  # type: ignore[arg-type]
            except Exception:  # pragma: no cover - defensivo
                self.embedding_quality = None
        else:
            self.embedding_quality = None
        semantic_scores = [_cosine_similarity(query_vector, vector) for vector in chunk_vectors]
        semantic_scores = [(value + 1.0) / 2.0 for value in semantic_scores]

        semantic_highlights = [
            StageHighlight(
                identifier=candidate.section.identifier,
                title=candidate.section.title or candidate.section.document_path.name,
                score=semantic,
                extra={"lexical": candidate.lexical_score},
            )
            for candidate, semantic in zip(chunk_candidates[:5], semantic_scores, strict=False)
        ]
        stages.append(
            StageReport(
                name="Scoring Semántico",
                description="Embeddings + fusión híbrida",
                input_size=len(chunk_candidates),
                output_size=len(chunk_candidates),
                parameters={"α": alpha, "β": self.config.role_bias},
                highlights=semantic_highlights,
            )
        )

        lexical_values = [candidate.lexical_score for candidate in chunk_candidates]
        max_lexical = max(lexical_values) if lexical_values else 0.0

        selections: list[PipelineSelection] = []
        for candidate, semantic in zip(chunk_candidates, semantic_scores, strict=False):
            lexical_norm = candidate.lexical_score / max_lexical if max_lexical > 0 else 0.0
            hybrid = alpha * lexical_norm + (1.0 - alpha) * semantic
            bias = self._metadata_bias(candidate.section.metadata, role)
            final_score = hybrid + self.config.role_bias * bias
            selections.append(
                PipelineSelection(
                    section=candidate.section,
                    chunk_text=candidate.chunk_text,
                    score=final_score,
                    lexical_score=lexical_norm,
                    semantic_score=semantic,
                    bias_applied=bias,
                )
            )

        selections.sort(key=lambda item: item.score, reverse=True)
        final_limit = min(limit, self.config.final_context_size)
        final_selections = selections[:final_limit]

        stages.append(
            StageReport(
                name="Selección Final",
                description="Contexto enviado al LLM",
                input_size=len(selections),
                output_size=len(final_selections),
                parameters={"final_context_size": self.config.final_context_size},
                highlights=[
                    StageHighlight(
                        identifier=selection.section.identifier,
                        title=selection.section.title
                        or selection.section.document_path.name,
                        score=selection.score,
                        extra={
                            "lex": round(selection.lexical_score, 4),
                            "sem": round(selection.semantic_score, 4),
                            "bias": round(selection.bias_applied, 4),
                        },
                    )
                    for selection in final_selections
                ],
            )
        )

        self.last_trace = PipelineTrace(
            query=query,
            alpha_used=alpha,
            config_snapshot=SearchPipelineConfig(**asdict(self.config)),
            stages=stages,
            selections=list(final_selections),
            embedding_quality=self.embedding_quality,
        )

        return final_selections

    # ------------------------------------------------------------------
    def _generate_embeddings(self, texts: Iterable[str]) -> list[list[float]]:
        try:
            return self.embedder.embed(texts, strategy=self.config.embedding_strategy)
        except TypeError:
            return self.embedder.embed(texts)

    # ------------------------------------------------------------------
    def _apply_rrf(self, lexical_ranking: Sequence["SearchResult"]) -> list["SearchResult"]:
        if not lexical_ranking:
            return []

        rrf_k = self.config.rrf_k
        id_to_candidate: dict[str, "SearchResult"] = {}
        scores: dict[str, float] = {}

        for rank, candidate in enumerate(lexical_ranking):
            identifier = candidate.section.identifier
            id_to_candidate.setdefault(identifier, candidate)
            scores[identifier] = scores.get(identifier, 0.0) + 1.0 / (rrf_k + rank + 1)

        ordered_ids = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        fused = [id_to_candidate[identifier] for identifier, _ in ordered_ids]
        for identifier, fused_score in ordered_ids:
            id_to_candidate[identifier].score = fused_score
        return fused

    def _apply_mmr(
        self,
        candidate_vectors: Sequence[Sequence[float]],
        similarities: Sequence[float],
    ) -> list[int]:
        if not candidate_vectors:
            return []

        mmr_lambda = self.config.mmr_lambda
        limit = min(self.config.mmr_limit, len(candidate_vectors))
        available = list(range(len(candidate_vectors)))
        selected: list[int] = []
        while available and len(selected) < limit:
            best_index = None
            best_score = -math.inf
            for index in available:
                if not selected:
                    diversity_penalty = 0.0
                else:
                    diversity_penalty = max(
                        _cosine_similarity(candidate_vectors[index], candidate_vectors[chosen])
                        for chosen in selected
                    )
                mmr_score = mmr_lambda * similarities[index] - (1.0 - mmr_lambda) * diversity_penalty
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_index = index
            if best_index is None:
                break
            selected.append(best_index)
            available.remove(best_index)
        return selected

    def _chunk_section(self, section: "DocumentSection") -> list[str]:
        sentences = _split_sentences(section.content)
        if not sentences:
            return [self._compose_chunk_text(section, section.content)]

        chunk_size = max(50, self.config.chunk_size_tokens)
        overlap = max(0, self.config.chunk_overlap_tokens)

        chunks: list[str] = []
        current: list[str] = []
        current_tokens = 0
        sentence_tokens: list[int] = []

        for sentence in sentences:
            tokens = _count_tokens(sentence)
            if current and current_tokens + tokens > chunk_size and current_tokens >= chunk_size // 2:
                chunk_body = " ".join(current).strip()
                chunks.append(self._compose_chunk_text(section, chunk_body))
                if overlap > 0:
                    overlap_tokens = 0
                    overlap_sentences: list[str] = []
                    overlap_counts: list[int] = []
                    for sent, tok in zip(reversed(current), reversed(sentence_tokens)):
                        overlap_tokens += tok
                        overlap_sentences.insert(0, sent)
                        overlap_counts.insert(0, tok)
                        if overlap_tokens >= overlap:
                            break
                    current = overlap_sentences[:]
                    sentence_tokens = overlap_counts[:]
                    current_tokens = sum(overlap_counts)
                else:
                    current = []
                    sentence_tokens = []
                    current_tokens = 0
            current.append(sentence)
            sentence_tokens.append(tokens)
            current_tokens += tokens

        if current:
            chunk_body = " ".join(current).strip()
            chunks.append(self._compose_chunk_text(section, chunk_body))

        return chunks

    def _compose_chunk_text(self, section: "DocumentSection", body: str) -> str:
        header_parts: list[str] = []
        stem = section.document_path.stem.replace("_", " ")
        if stem:
            header_parts.append(stem)
        if section.title:
            header_parts.append(section.title)
        header = " › ".join(header_parts) or section.document_path.name
        return f"{header}\n\n{body.strip()}".strip()

    def _metadata_bias(self, metadata: dict[str, str], role: str | None) -> float:
        if not metadata or not role:
            return 0.0
        normalized_role = role.strip().lower()
        for key, value in metadata.items():
            if "rol" in key.lower() or "role" in key.lower():
                if normalized_role == value.strip().lower():
                    return 1.0
        return 0.0

    @staticmethod
    def _section_to_text(section: "DocumentSection") -> str:
        header = section.title or ""
        return f"{header}\n{section.content}".strip()

    @staticmethod
    def _clamp_alpha(alpha: float) -> float:
        if alpha <= 0:
            return 0.0
        if alpha >= 1:
            return 1.0
        return alpha


@dataclass
class _ChunkCandidate:
    section: "DocumentSection"
    chunk_text: str
    lexical_score: float


_TOKEN_PATTERN = re.compile(r"[\wáéíóúñü]+", re.IGNORECASE)


def _split_sentences(text: str) -> list[str]:
    stripped = text.strip()
    if not stripped:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", stripped)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def _count_tokens(text: str) -> int:
    return len(_TOKEN_PATTERN.findall(text))


# ----------------------------------------------------------------------
def _cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or not right:
        return 0.0
    return sum(l * r for l, r in zip(left, right, strict=False))


__all__ = [
    "HybridSearchPipeline",
    "PipelineSelection",
    "PipelineTrace",
    "StageHighlight",
    "StageReport",
    "SearchPipelineConfig",
]
