import math

from dungeon_life_agent.embedding_gemma import EmbeddingGemma


def test_embedding_gemma_returns_normalized_vectors():
    embedder = EmbeddingGemma(dimension=32)
    vector = embedder.embed(["hola mundo"])[0]
    norm = math.sqrt(sum(component * component for component in vector))
    assert vector, "Se esperaba un vector no vacío"
    assert math.isclose(norm, 1.0, rel_tol=1e-6)

    repeated = embedder.embed(["hola mundo"])[0]
    assert vector == repeated, "La caché debe devolver el mismo embedding"


def test_embedding_gemma_handles_textos_vacios():
    embedder = EmbeddingGemma(dimension=16)
    vector = embedder.embed([""])[0]
    norm = math.sqrt(sum(component * component for component in vector))
    assert math.isclose(norm, 1.0, rel_tol=1e-6)
