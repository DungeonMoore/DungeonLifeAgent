from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from dungeon_life_agent.knowledge import DocumentSection, SearchResult
from dungeon_life_agent.offline_metrics import (
    OfflineQuery,
    evaluate_offline,
    grid_search_hyperparameters,
)
from dungeon_life_agent.search_pipeline import SearchPipelineConfig


class _StubIndex:
    def __init__(self) -> None:
        self._pipeline = SimpleNamespace(config=SearchPipelineConfig())
        self._data = {
            "consulta a": [
                SearchResult(section=_make_section("a", "Intro", "Contenido"), score=0.2),
                SearchResult(section=_make_section("b", "Guía", "Detalle relevante"), score=0.1),
            ],
            "consulta b": [
                SearchResult(section=_make_section("c", "Resumen", "Contexto extra"), score=0.5),
                SearchResult(section=_make_section("d", "Anexo", "Más info"), score=0.3),
            ],
        }

    def search(self, query: str, limit: int, *, role=None, alpha=None):
        results = list(self._data[query])
        if self._pipeline.config.role_bias > 0.05:
            results = list(reversed(results))
        return results[:limit]


def _make_section(name: str, title: str, content: str) -> DocumentSection:
    return DocumentSection(
        document_path=Path(f"{name}.md"),
        title=title,
        content=content,
        metadata={},
        heading_level=1,
        tokens=tuple(content.split()),
    )


def test_offline_evaluation_and_grid_search():
    index = _StubIndex()
    queries = [
        OfflineQuery(query="consulta a", relevant_ids=("b.md::Guía",)),
        OfflineQuery(query="consulta b", relevant_ids=("d.md::Anexo",)),
    ]

    report = evaluate_offline(index, queries, limit=2, ks=(1, 2))
    assert report.macro_recall_at_k[1] < 1.0
    assert report.macro_recall_at_k[2] == 1.0
    assert 0.0 <= report.macro_mrr_at_10 <= 1.0
    assert 0.0 <= report.macro_ndcg_at_10 <= 1.0

    search_report = grid_search_hyperparameters(
        index,
        queries,
        alpha_values=(0.6,),
        fusion_top_n_values=(30,),
        mmr_limit_values=(10,),
        mmr_lambda_values=(0.8,),
        role_bias_values=(0.0, 0.1),
        limit=2,
        ks=(1,),
    )

    assert search_report.entries[0].role_bias == 0.1
    assert search_report.entries[0].report.macro_recall_at_k[1] == 1.0
