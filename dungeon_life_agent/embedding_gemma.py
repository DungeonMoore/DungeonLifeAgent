"""Adaptador ligero para generar embeddings con modelos Gemma u otro backend compatible.

La implementación prioriza un modo de fallback determinista para entornos
sin acceso a Ollama o a modelos pesados, pero expone la interfaz necesaria
para enchufar Gemma cuando esté disponible. Todas las salidas se
normalizan (L2) para que la similitud de coseno sea equivalente al producto
punto, tal y como requiere la capa semántica del buscador."""

from __future__ import annotations

import functools
import hashlib
import math
import threading
from collections import OrderedDict
from dataclasses import dataclass
from typing import Iterable, Protocol, Sequence


class _SupportsEmbed(Protocol):
    """Protocolo mínimo compatible con el cliente oficial de Ollama."""

    def embed(self, *, model: str, input: Sequence[str]) -> dict:
        ...


@dataclass(frozen=True)
class EmbeddingRequest:
    """Representa una solicitud de embedding, utilizada para caché LRU."""

    text_hash: str
    dimension: int


class _LRUCache:
    """Caché LRU simple y thread-safe."""

    def __init__(self, max_size: int = 1024) -> None:
        self.max_size = max_size
        self._storage: OrderedDict[EmbeddingRequest, list[float]] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: EmbeddingRequest) -> list[float] | None:
        with self._lock:
            if key not in self._storage:
                return None
            self._storage.move_to_end(key)
            return list(self._storage[key])

    def put(self, key: EmbeddingRequest, value: Sequence[float]) -> None:
        with self._lock:
            self._storage[key] = list(value)
            self._storage.move_to_end(key)
            while len(self._storage) > self.max_size:
                self._storage.popitem(last=False)


class EmbeddingGemma:
    """Adaptador configurable para obtener embeddings normalizados.

    El adaptador intenta usar automáticamente un cliente compatible con
    Ollama si está disponible. En caso contrario, se recurre a un modo de
    fallback determinista basado en hashing, suficiente para pruebas y para
    garantizar que la canalización de búsqueda siga funcionando."""

    def __init__(
        self,
        model: str = "gemma2:2b",
        *,
        client: _SupportsEmbed | None = None,
        cache_size: int = 2048,
        dimension: int = 384,
    ) -> None:
        self.model = model
        self.dimension = dimension
        self._client = client or self._autodetect_client()
        self._cache = _LRUCache(max_size=cache_size)

    # ------------------------------------------------------------------
    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        """Genera embeddings normalizados para los textos proporcionados."""

        normalized_texts = [text.strip() if text else "" for text in texts]
        if not normalized_texts:
            return []

        results: list[list[float]] = []
        missing: list[tuple[int, str]] = []

        for index, text in enumerate(normalized_texts):
            key = EmbeddingRequest(_hash_text(text), self.dimension)
            cached = self._cache.get(key)
            if cached is not None:
                results.append(cached)
            else:
                results.append([])  # placeholder
                missing.append((index, text))

        if missing:
            if self._client is not None:
                try:
                    remote_vectors = self._request_remote_embeddings([text for _, text in missing])
                except Exception:
                    remote_vectors = None
            else:
                remote_vectors = None

            if remote_vectors is None:
                remote_vectors = [self._fallback_embedding(text) for _, text in missing]

            for (index, text), vector in zip(missing, remote_vectors, strict=False):
                normalized = _l2_normalize(vector)
                key = EmbeddingRequest(_hash_text(text), self.dimension)
                self._cache.put(key, normalized)
                results[index] = normalized

        return [vector if vector else self._fallback_embedding("") for vector in results]

    # ------------------------------------------------------------------
    def _request_remote_embeddings(self, texts: Sequence[str]) -> list[list[float]] | None:
        if self._client is None:
            return None
        response = self._client.embed(model=self.model, input=list(texts))
        vectors = response.get("embeddings") or response.get("data")
        if not vectors:
            return None
        processed: list[list[float]] = []
        for vector in vectors:
            if isinstance(vector, dict) and "embedding" in vector:
                vector = vector["embedding"]
            processed.append(list(vector))
        return processed

    def _fallback_embedding(self, text: str) -> list[float]:
        tokens = _tokenize_for_fallback(text)
        if not tokens:
            return _unit_vector(self.dimension)

        vector = [0.0] * self.dimension
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            for index in range(self.dimension):
                byte = digest[index % len(digest)]
                vector[index] += (byte / 255.0) * 2.0 - 1.0

        return _l2_normalize(vector)

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def _autodetect_client() -> _SupportsEmbed | None:
        try:
            import ollama  # type: ignore
        except Exception:
            return None
        return ollama


# ----------------------------------------------------------------------
def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _l2_normalize(vector: Sequence[float]) -> list[float]:
    norm = math.sqrt(sum(component * component for component in vector))
    if norm == 0:
        return [0.0] * len(vector)
    return [component / norm for component in vector]


def _unit_vector(dimension: int) -> list[float]:
    if dimension <= 0:
        return []
    return [1.0] + [0.0] * (dimension - 1)


def _tokenize_for_fallback(text: str) -> list[str]:
    tokens = []
    current = []
    for char in text.lower():
        if char.isalnum():
            current.append(char)
        else:
            if current:
                tokens.append("".join(current))
                current = []
    if current:
        tokens.append("".join(current))
    return tokens


__all__ = ["EmbeddingGemma"]
