"""Arquitectura definitiva del pipeline de inferencia de alta fidelidad."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING

from .embedding_gemma import EmbeddingGemma

if TYPE_CHECKING:  # pragma: no cover
    from .knowledge import DocumentSection, SearchResult


@dataclass
class PipelineSelection:
    """Representa un fragmento listo para el LLM con trazabilidad completa."""

    section: "DocumentSection"
    chunk_text: str
    score: float
    lexical_score: float
    semantic_score: float
    bias_applied: float


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


class HybridSearchPipeline:
    """Implementa el flujo BM25 → RRF → MMR → Gemma descrito por el Arquitecto."""

    def __init__(self, embedder: EmbeddingGemma | None = None, config: SearchPipelineConfig | None = None) -> None:
        self.embedder = embedder or EmbeddingGemma()
        self.config = config or SearchPipelineConfig()

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
        if not candidates:
            return []

        alpha = self._clamp_alpha(alpha_override if alpha_override is not None else self.config.alpha)
        lexical_ranking = list(candidates)
        fusion = self._apply_rrf(lexical_ranking)
        if not fusion:
            return []

        query_vector = self.embedder.embed([query])[0]

        sections_for_mmr = fusion[: self.config.fusion_top_n]
        section_vectors = self.embedder.embed([
            self._section_to_text(candidate.section) for candidate in sections_for_mmr
        ])
        similarities = [_cosine_similarity(query_vector, vector) for vector in section_vectors]
        mmr_indices = self._apply_mmr(section_vectors, similarities)
        diversified_sections = [sections_for_mmr[index] for index in mmr_indices]

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

        chunk_texts = [candidate.chunk_text for candidate in chunk_candidates]
        chunk_vectors = self.embedder.embed(chunk_texts)
        semantic_scores = [_cosine_similarity(query_vector, vector) for vector in chunk_vectors]
        semantic_scores = [(value + 1.0) / 2.0 for value in semantic_scores]

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
        return selections[:final_limit]

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


__all__ = ["HybridSearchPipeline", "PipelineSelection", "SearchPipelineConfig"]
