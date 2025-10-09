from __future__ import annotations

from pathlib import Path

from dungeon_life_agent.advanced_embeddings import EmbeddingQuality
from dungeon_life_agent.knowledge import DocumentSection, SearchResult
from dungeon_life_agent.search_pipeline import (
    HybridSearchPipeline,
    PipelineTrace,
    SearchPipelineConfig,
)


class _DeterministicEmbedder:
    def embed(self, texts, strategy="auto"):
        vectors: list[list[float]] = []
        for index, text in enumerate(texts):
            length = len(text)
            vectors.append([
                float(length % 13) / 10.0,
                float((index + 1) % 7) / 10.0,
                float(length) / 100.0,
            ])
        return vectors

    def quality_report(self, vectors):
        return EmbeddingQuality(mean_magnitude=1.0, stdev_magnitude=0.0, pairwise_cosine=0.5)


def _make_section(name: str, title: str, content: str, *, role: str | None = None) -> DocumentSection:
    metadata = {"rol": role} if role else {}
    return DocumentSection(
        document_path=Path(f"{name}.md"),
        title=title,
        content=content,
        metadata=metadata,
        heading_level=1,
        tokens=tuple(content.split()),
    )


def test_pipeline_trace_captures_stages_and_prompt():
    section_a = _make_section("doc_a", "Introducción", "Contenido inicial relevante", role="consultor")
    section_b = _make_section("doc_b", "Detalles", "Explicación alternativa del tema")

    candidates = [
        SearchResult(section=section_a, score=0.9),
        SearchResult(section=section_b, score=0.6),
    ]

    pipeline = HybridSearchPipeline(
        embedder=_DeterministicEmbedder(),
        config=SearchPipelineConfig(
            alpha=0.6,
            lexical_top_k=5,
            fusion_top_n=2,
            mmr_lambda=0.7,
            mmr_limit=2,
            rrf_k=20,
            chunk_size_tokens=50,
            chunk_overlap_tokens=10,
            role_bias=0.05,
            final_context_size=2,
        ),
    )

    selections = pipeline.search("¿Qué es Willow?", candidates, limit=2, role="consultor")
    assert selections, "Debe haber selecciones finales"

    trace = pipeline.last_trace
    assert isinstance(trace, PipelineTrace)
    assert trace.query == "¿Qué es Willow?"
    assert len(trace.stages) >= 5
    assert any(stage.name == "MMR Diversificación" for stage in trace.stages)

    prompt = trace.to_prompt()
    assert "Consulta Analizada" in prompt
    assert "Selección Final" in prompt
    assert "Willow" in prompt
