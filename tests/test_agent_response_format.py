from pathlib import Path

from dungeon_life_agent.agent import AgentResponse, DungeonLifeAgent
from dungeon_life_agent.knowledge import DocumentSection, SearchResult
from dungeon_life_agent.search_pipeline import (
    PipelineSelection,
    PipelineTrace,
    SearchPipelineConfig,
    StageHighlight,
    StageReport,
)


class _StaticKnowledge:
    def __init__(self, results, trace):
        self._results = results
        self._trace = trace

    def search(self, query, limit=3, role=None, alpha=None):  # noqa: D401 - firma compatible
        return self._results[:limit]

    def last_search_trace(self):
        return self._trace


def _sample_section() -> DocumentSection:
    return DocumentSection(
        document_path=Path("doc.md"),
        title="Introducción",
        content="Contenido relevante para la consulta",
        metadata={},
        heading_level=1,
        tokens=("contenido", "relevante"),
    )


def _sample_trace(section: DocumentSection) -> PipelineTrace:
    selection = PipelineSelection(
        section=section,
        chunk_text="Texto",
        score=0.9,
        lexical_score=0.8,
        semantic_score=0.85,
        bias_applied=0.0,
    )
    stage = StageReport(
        name="Lexical",
        description="Coincidencia BM25",
        input_size=10,
        output_size=5,
        parameters={"top_k": 10},
        highlights=[StageHighlight(identifier="doc", title="Introducción", score=0.75)],
    )
    return PipelineTrace(
        query="¿Qué es DMTE?",
        alpha_used=0.6,
        config_snapshot=SearchPipelineConfig(),
        stages=[stage],
        selections=[selection],
        embedding_quality=None,
    )


def test_format_text_includes_debug_section_when_requested():
    response = AgentResponse(
        mode="consultor",
        role="Arquitecto",
        summary="Respuesta sintetizada",
        highlights=["Idea principal"],
        references=["doc.md → Introducción"],
        debug_trace="Linea A\nLinea B",
    )

    plain = response.format_text()
    assert "Linea A" not in plain

    debug_text = response.format_text(show_debug=True)
    assert "Diagnóstico del pipeline" in debug_text
    assert "Linea A" in debug_text
    assert "Linea B" in debug_text


def test_query_attaches_pipeline_trace_to_response():
    section = _sample_section()
    results = [SearchResult(section=section, score=0.9)]
    trace = _sample_trace(section)
    agent = DungeonLifeAgent(knowledge_index=_StaticKnowledge(results, trace))

    response = agent.query("¿Qué es DMTE?")
    assert response.debug_trace is not None
    formatted = response.format_text(show_debug=True)
    assert "Selección final enviada al LLM" in formatted
    assert "Introducción" in formatted
