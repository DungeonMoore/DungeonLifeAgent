"""Sistema avanzado de embeddings multi-modelo con caché híbrida y métricas.

Este módulo implementa varias de las capacidades descritas en la
planificación de optimización del proyecto:

* **Soporte multi-modelo**: permite combinar distintos modelos de
  embeddings (por ejemplo Gemma y modelos especializados) utilizando
  estrategias configurables.
* **Cuantización ligera**: soporta almacenamiento en precisiones FP32,
  FP16 e INT8 para optimizar memoria sin depender de librerías externas.
* **Caché híbrida**: combina un caché en memoria (LRU) con un backend
  opcional en Redis para escenarios distribuidos.
* **Métricas de calidad**: genera métricas simples sobre la magnitud y
  coherencia de los embeddings para facilitar la monitorización.

La implementación evita dependencias pesadas y se integra con la clase
``EmbeddingGemma`` existente, reutilizando su modo determinista de
fallback cuando no hay modelos remotos disponibles. Las interfaces se
han diseñado para mantener compatibilidad hacia atrás con el pipeline de
 búsqueda existente.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Callable, Iterable, Protocol, Sequence

from .embedding_gemma import EmbeddingGemma

LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuración y contratos


class SupportsEmbedding(Protocol):
    """Contrato mínimo para backends de embeddings."""

    dimension: int

    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        """Genera embeddings normalizados para los textos dados."""


@dataclass(frozen=True)
class EmbeddingModelConfig:
    """Configura un modelo de embeddings dentro del sistema."""

    name: str
    weight: float = 1.0
    dimension: int = 384
    precision: str = "fp32"  # fp32 | fp16 | int8
    role: str | None = None


@dataclass(frozen=True)
class EmbeddingRunMetrics:
    """Métricas básicas obtenidas tras una generación de embeddings."""

    model: str
    precision: str
    latency_ms: float
    dimension: int
    cache_hits: int
    cache_misses: int


@dataclass(frozen=True)
class EmbeddingQuality:
    """Indicadores rápidos para evaluar la coherencia de un lote."""

    mean_magnitude: float
    stdev_magnitude: float
    pairwise_cosine: float


Factory = Callable[[EmbeddingModelConfig], SupportsEmbedding]


# ---------------------------------------------------------------------------
# Caché híbrida (memoria + Redis opcional)


class HybridEmbeddingCache:
    """Caché LRU con backend opcional en Redis."""

    def __init__(
        self,
        *,
        max_size: int = 2048,
        namespace: str = "embeddings",
        redis_url: str | None = None,
    ) -> None:
        self.max_size = max(1, max_size)
        self.namespace = namespace
        self._storage: OrderedDict[str, dict] = OrderedDict()
        self._lock = threading.Lock()
        self._redis = self._initialize_redis(redis_url)

    @staticmethod
    def _initialize_redis(redis_url: str | None):  # pragma: no cover - import dinámico
        if not redis_url:
            return None
        try:
            import redis  # type: ignore

            client = redis.Redis.from_url(redis_url)
            client.ping()
            return client
        except Exception as exc:  # pragma: no cover - dependencias opcionales
            LOGGER.warning("No se pudo inicializar Redis para el caché de embeddings: %s", exc)
            return None

    def _make_key(self, identifier: str) -> str:
        return f"{self.namespace}:{identifier}"

    def get(self, identifier: str) -> dict | None:
        key = self._make_key(identifier)
        with self._lock:
            if key in self._storage:
                self._storage.move_to_end(key)
                return dict(self._storage[key])
        if self._redis is None:
            return None
        raw = self._redis.get(key)
        if raw is None:
            return None
        try:
            data = json.loads(raw.decode("utf-8"))
            with self._lock:
                self._storage[key] = data
                self._storage.move_to_end(key)
                while len(self._storage) > self.max_size:
                    self._storage.popitem(last=False)
            return dict(data)
        except Exception:
            return None

    def set(self, identifier: str, payload: dict) -> None:
        key = self._make_key(identifier)
        with self._lock:
            self._storage[key] = dict(payload)
            self._storage.move_to_end(key)
            while len(self._storage) > self.max_size:
                self._storage.popitem(last=False)
        if self._redis is not None:
            try:  # pragma: no branch - se intenta escribir y se ignoran errores
                self._redis.set(key, json.dumps(payload))
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Sistema de embeddings multi-modelo


class EmbeddingSystem:
    """Administra múltiples modelos de embeddings con caché y métricas."""

    def __init__(
        self,
        configs: Sequence[EmbeddingModelConfig] | None = None,
        *,
        cache: HybridEmbeddingCache | None = None,
        factories: dict[str, Factory] | None = None,
        default_strategy: str = "auto",
    ) -> None:
        if not configs:
            configs = (
                EmbeddingModelConfig(name="gemma2:2b", dimension=384, precision="fp32"),
                EmbeddingModelConfig(name="gemma2:2b", dimension=384, precision="fp16"),
            )
        self.configs = list(configs)
        self.cache = cache or HybridEmbeddingCache()
        self.factories = factories or {}
        self.default_strategy = default_strategy
        self._embedders: dict[str, SupportsEmbedding] = {}

    # ------------------------------------------------------------------
    def embed(
        self,
        texts: Iterable[str],
        *,
        strategy: str | None = None,
        precision: str | None = None,
        return_metrics: bool = False,
    ) -> list[list[float]] | tuple[list[list[float]], list[EmbeddingRunMetrics]]:
        normalized_texts = [text.strip() if text else "" for text in texts]
        if not normalized_texts:
            return ([], []) if return_metrics else []

        strategy = strategy or self.default_strategy
        selected = self._select_configs(strategy)

        aggregate: list[list[float] | None] = [None] * len(normalized_texts)
        metrics: list[EmbeddingRunMetrics] = []

        for index, config in enumerate(selected):
            embedder = self._get_embedder(config)
            run_precision = precision or config.precision
            start = time.perf_counter()
            vectors, hits, misses = self._embed_with_cache(
                normalized_texts, embedder, config, run_precision
            )
            elapsed = (time.perf_counter() - start) * 1000.0
            metrics.append(
                EmbeddingRunMetrics(
                    model=config.name,
                    precision=run_precision,
                    latency_ms=elapsed,
                    dimension=len(vectors[0]) if vectors else config.dimension,
                    cache_hits=hits,
                    cache_misses=misses,
                )
            )
            aggregate = self._merge_vectors(aggregate, vectors, strategy, index)

        final_vectors = [self._normalize_vector(vector) for vector in aggregate if vector is not None]
        if return_metrics:
            return final_vectors, metrics
        return final_vectors

    # ------------------------------------------------------------------
    def quality_report(self, vectors: Sequence[Sequence[float]]) -> EmbeddingQuality:
        """Calcula métricas agregadas de calidad para un lote de embeddings."""

        if not vectors:
            return EmbeddingQuality(mean_magnitude=0.0, stdev_magnitude=0.0, pairwise_cosine=0.0)

        magnitudes = [math.sqrt(sum(component * component for component in vector)) for vector in vectors]
        mean_mag = mean(magnitudes)
        stdev_mag = pstdev(magnitudes)
        pairwise = self._average_pairwise_cosine(vectors)
        return EmbeddingQuality(mean_magnitude=mean_mag, stdev_magnitude=stdev_mag, pairwise_cosine=pairwise)

    # ------------------------------------------------------------------
    def _select_configs(self, strategy: str) -> list[EmbeddingModelConfig]:
        if strategy == "auto":
            return [self.configs[0]]
        if strategy == "stack":
            return list(self.configs)
        if strategy == "average":
            return list(self.configs)
        return [self.configs[0]]

    def _get_embedder(self, config: EmbeddingModelConfig) -> SupportsEmbedding:
        if config.name not in self._embedders:
            factory = self.factories.get(config.name)
            if factory is not None:
                self._embedders[config.name] = factory(config)
            else:
                self._embedders[config.name] = EmbeddingGemma(model=config.name, dimension=config.dimension)
        return self._embedders[config.name]

    def _embed_with_cache(
        self,
        texts: Sequence[str],
        embedder: SupportsEmbedding,
        config: EmbeddingModelConfig,
        precision: str,
    ) -> tuple[list[list[float]], int, int]:
        hits = 0
        misses = 0
        vectors: list[list[float]] = []
        to_query: list[tuple[int, str]] = []

        for index, text in enumerate(texts):
            key = self._cache_key(text, config, precision)
            cached = self.cache.get(key)
            if cached is not None:
                vector = self._dequantize(cached["vector"], cached.get("precision", precision))
                vectors.append(vector)
                hits += 1
            else:
                vectors.append([])
                to_query.append((index, text))
                misses += 1

        if to_query:
            fresh_vectors = embedder.embed([text for _, text in to_query])
            for (position, text), vector in zip(to_query, fresh_vectors, strict=False):
                quantized = self._quantize(vector, precision)
                key = self._cache_key(text, config, precision)
                self.cache.set(key, {"precision": precision, "vector": quantized})
                vectors[position] = list(vector)

        return vectors, hits, misses

    def _merge_vectors(
        self,
        aggregate: list[list[float] | None],
        vectors: Sequence[Sequence[float]],
        strategy: str,
        iteration: int,
    ) -> list[list[float] | None]:
        if strategy == "stack":
            for index, vector in enumerate(vectors):
                existing = aggregate[index] or []
                aggregate[index] = list(existing) + list(vector)
            return aggregate

        if strategy == "average" and iteration > 0:
            for index, vector in enumerate(vectors):
                existing = aggregate[index]
                if existing is None:
                    aggregate[index] = list(vector)
                else:
                    aggregate[index] = [
                        (prev * iteration + current) / (iteration + 1)
                        for prev, current in zip(existing, vector, strict=False)
                    ]
            return aggregate

        for index, vector in enumerate(vectors):
            if aggregate[index] is None:
                aggregate[index] = list(vector)
        return aggregate

    def _normalize_vector(self, vector: Sequence[float]) -> list[float]:
        norm = math.sqrt(sum(component * component for component in vector))
        if norm == 0:
            return [0.0 for _ in vector]
        return [component / norm for component in vector]

    def _cache_key(self, text: str, config: EmbeddingModelConfig, precision: str) -> str:
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
        return f"{config.name}:{config.dimension}:{precision}:{digest}"

    def _quantize(self, vector: Sequence[float], precision: str) -> list[float] | list[int]:
        if precision.lower() == "fp16":
            return [float(f"{component:.4f}") for component in vector]
        if precision.lower() == "int8":
            scale = 127.0
            return [int(max(-127, min(127, round(component * scale)))) for component in vector]
        return [float(component) for component in vector]

    def _dequantize(self, data: Sequence[float | int], precision: str) -> list[float]:
        if precision.lower() == "fp16":
            return [float(component) for component in data]
        if precision.lower() == "int8":
            scale = 127.0
            return [float(component) / scale for component in data]
        return [float(component) for component in data]

    def _average_pairwise_cosine(self, vectors: Sequence[Sequence[float]]) -> float:
        if len(vectors) < 2:
            return 1.0
        total = 0.0
        count = 0
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                total += self._cosine(vectors[i], vectors[j])
                count += 1
        return total / count if count else 0.0

    def _cosine(self, left: Sequence[float], right: Sequence[float]) -> float:
        numerator = sum(a * b for a, b in zip(left, right, strict=False))
        norm_left = math.sqrt(sum(a * a for a in left))
        norm_right = math.sqrt(sum(b * b for b in right))
        if norm_left == 0 or norm_right == 0:
            return 0.0
        return numerator / (norm_left * norm_right)


__all__ = [
    "EmbeddingModelConfig",
    "EmbeddingRunMetrics",
    "EmbeddingQuality",
    "HybridEmbeddingCache",
    "EmbeddingSystem",
]

