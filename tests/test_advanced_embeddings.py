import math

from dungeon_life_agent.advanced_embeddings import (
    EmbeddingModelConfig,
    EmbeddingSystem,
    HybridEmbeddingCache,
)


class _StubEmbedder:
    def __init__(self, dimension: int, value: float) -> None:
        self.dimension = dimension
        self.value = value
        self.calls = 0

    def embed(self, texts):
        items = list(texts)
        self.calls += len(items)
        return [[self.value for _ in range(self.dimension)] for _ in items]


def test_average_strategy_combines_models_and_uses_cache():
    cache = HybridEmbeddingCache()
    embedder_a = _StubEmbedder(4, 1.0)
    embedder_b = _StubEmbedder(4, 0.5)

    configs = [
        EmbeddingModelConfig(name="model-a", dimension=4, precision="fp32"),
        EmbeddingModelConfig(name="model-b", dimension=4, precision="fp32"),
    ]

    system = EmbeddingSystem(
        configs,
        cache=cache,
        factories={
            "model-a": lambda cfg: embedder_a,
            "model-b": lambda cfg: embedder_b,
        },
        default_strategy="average",
    )

    vectors, metrics = system.embed(["hola"], return_metrics=True)
    assert len(vectors) == 1
    assert math.isclose(sum(component * component for component in vectors[0]), 1.0, rel_tol=1e-6)
    assert len(metrics) == 2
    assert embedder_a.calls == 1
    assert embedder_b.calls == 1
    assert metrics[0].cache_misses == 1
    assert metrics[1].cache_misses == 1

    second_vectors, second_metrics = system.embed(["hola"], return_metrics=True)
    assert len(second_vectors) == 1
    assert embedder_a.calls == 1, "Las consultas deben obtenerse del caché"
    assert embedder_b.calls == 1
    assert second_metrics[0].cache_hits == 1
    assert second_metrics[1].cache_hits == 1


def test_int8_quantization_stores_integer_payloads():
    cache = HybridEmbeddingCache()
    embedder = _StubEmbedder(3, 0.25)
    config = EmbeddingModelConfig(name="model-int8", dimension=3, precision="int8")
    system = EmbeddingSystem([config], cache=cache, factories={"model-int8": lambda cfg: embedder})

    vectors, metrics = system.embed(["quantiza"], return_metrics=True)
    assert len(vectors) == 1
    assert metrics[0].cache_misses == 1

    key = system._cache_key("quantiza", config, "int8")  # type: ignore[attr-defined]
    payload = cache.get(key)
    assert payload is not None
    assert payload["precision"] == "int8"
    assert all(isinstance(value, int) for value in payload["vector"])

    system.embed(["quantiza"], return_metrics=True)
    assert embedder.calls == 1


def test_quality_report_measures_pairwise_cosine():
    system = EmbeddingSystem([EmbeddingModelConfig(name="only")])
    vectors = [[1.0, 0.0], [0.0, 1.0]]
    report = system.quality_report(vectors)
    assert math.isclose(report.mean_magnitude, 1.0, rel_tol=1e-6)
    assert math.isclose(report.pairwise_cosine, 0.0, rel_tol=1e-6)
