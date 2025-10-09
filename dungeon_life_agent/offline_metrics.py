"""Métricas offline y grid-search para el pipeline híbrido de Willow."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log2
from statistics import fmean
from typing import Sequence

from .search_pipeline import SearchPipelineConfig


@dataclass(frozen=True)
class OfflineQuery:
    """Describe una consulta real con sus documentos relevantes."""

    query: str
    relevant_ids: tuple[str, ...]
    role: str | None = None
    alpha: float | None = None


@dataclass(frozen=True)
class QueryEvaluation:
    """Resultados de métricas offline para una consulta individual."""

    query: OfflineQuery
    recall_at_k: dict[int, float]
    mrr_at_10: float
    ndcg_at_10: float


@dataclass
class EvaluationReport:
    """Métricas agregadas sobre un conjunto de consultas."""

    per_query: list[QueryEvaluation]
    macro_recall_at_k: dict[int, float]
    macro_mrr_at_10: float
    macro_ndcg_at_10: float


@dataclass(frozen=True)
class GridSearchEntry:
    """Resultado de evaluar una combinación de hiperparámetros."""

    alpha: float
    fusion_top_n: int
    mmr_limit: int
    mmr_lambda: float
    role_bias: float
    report: EvaluationReport


@dataclass
class GridSearchReport:
    """Colección ordenada de resultados de grid-search."""

    entries: list[GridSearchEntry]

    def top(self, n: int = 5) -> list[GridSearchEntry]:
        """Devuelve las mejores combinaciones según nDCG@10."""

        return self.entries[: max(1, n)]


def evaluate_offline(
    index,
    queries: Sequence[OfflineQuery],
    *,
    limit: int = 20,
    ks: Sequence[int] = (5, 10),
) -> EvaluationReport:
    """Calcula Recall@K, MRR@10 y nDCG@10 sobre consultas reales."""

    results: list[QueryEvaluation] = []
    ks_sorted = sorted(set(k for k in ks if k > 0))

    for offline_query in queries:
        retrieved = index.search(
            offline_query.query,
            limit=limit,
            role=offline_query.role,
            alpha=offline_query.alpha,
        )
        identifiers = [result.section.identifier for result in retrieved]
        relevant = set(offline_query.relevant_ids)
        vector = [1 if identifier in relevant else 0 for identifier in identifiers]
        total_relevant = len(relevant)

        recall_scores = {
            k: _recall_at_k(vector, k, total_relevant) for k in ks_sorted
        }
        mrr_score = _mrr_at_k(vector, 10)
        ndcg_score = _ndcg_at_k(vector, 10)
        results.append(
            QueryEvaluation(
                query=offline_query,
                recall_at_k=recall_scores,
                mrr_at_10=mrr_score,
                ndcg_at_10=ndcg_score,
            )
        )

    macro_recall = {
        k: fmean(result.recall_at_k.get(k, 0.0) for result in results)
        for k in ks_sorted
    }
    macro_mrr = fmean(result.mrr_at_10 for result in results) if results else 0.0
    macro_ndcg = fmean(result.ndcg_at_10 for result in results) if results else 0.0

    return EvaluationReport(
        per_query=results,
        macro_recall_at_k=macro_recall,
        macro_mrr_at_10=macro_mrr,
        macro_ndcg_at_10=macro_ndcg,
    )


def grid_search_hyperparameters(
    index,
    queries: Sequence[OfflineQuery],
    *,
    alpha_values: Sequence[float] = (0.4, 0.5, 0.6, 0.7, 0.8),
    fusion_top_n_values: Sequence[int] = (30, 50, 80),
    mmr_limit_values: Sequence[int] = (10, 20, 30),
    mmr_lambda_values: Sequence[float] = (0.7, 0.8, 0.9),
    role_bias_values: Sequence[float] = (0.0, 0.03, 0.05, 0.1),
    limit: int = 20,
    ks: Sequence[int] = (5, 10),
) -> GridSearchReport:
    """Explora combinaciones recomendadas de hiperparámetros."""

    config = index._pipeline.config  # noqa: SLF001 - acceso controlado para tuning offline
    original = SearchPipelineConfig(**config.__dict__)

    entries: list[GridSearchEntry] = []
    combinations = product(
        alpha_values,
        fusion_top_n_values,
        mmr_limit_values,
        mmr_lambda_values,
        role_bias_values,
    )

    try:
        for alpha, fusion_top_n, mmr_limit, mmr_lambda, role_bias in combinations:
            config.alpha = alpha
            config.fusion_top_n = fusion_top_n
            config.mmr_limit = mmr_limit
            config.mmr_lambda = mmr_lambda
            config.role_bias = role_bias
            report = evaluate_offline(index, queries, limit=limit, ks=ks)
            entries.append(
                GridSearchEntry(
                    alpha=alpha,
                    fusion_top_n=fusion_top_n,
                    mmr_limit=mmr_limit,
                    mmr_lambda=mmr_lambda,
                    role_bias=role_bias,
                    report=report,
                )
            )
    finally:
        config.__dict__.update(original.__dict__)

    entries.sort(key=lambda entry: entry.report.macro_ndcg_at_10, reverse=True)
    return GridSearchReport(entries=entries)


def _recall_at_k(vector: Sequence[int], k: int, total_relevant: int) -> float:
    if total_relevant == 0:
        return 0.0
    hits = sum(vector[:k])
    return hits / total_relevant


def _mrr_at_k(vector: Sequence[int], k: int) -> float:
    for index, value in enumerate(vector[:k]):
        if value:
            return 1.0 / (index + 1)
    return 0.0


def _ndcg_at_k(vector: Sequence[int], k: int) -> float:
    gains = vector[:k]
    if not gains:
        return 0.0
    dcg = _dcg(gains)
    ideal = sorted(gains, reverse=True)
    ideal_dcg = _dcg(ideal)
    if ideal_dcg == 0.0:
        return 0.0
    return dcg / ideal_dcg


def _dcg(gains: Sequence[int]) -> float:
    value = 0.0
    for index, gain in enumerate(gains, start=1):
        if gain:
            denom = log2(index + 1) if index > 1 else 1.0
            value += (2**gain - 1) / denom
    return value


__all__ = [
    "OfflineQuery",
    "QueryEvaluation",
    "EvaluationReport",
    "GridSearchEntry",
    "GridSearchReport",
    "evaluate_offline",
    "grid_search_hyperparameters",
]
