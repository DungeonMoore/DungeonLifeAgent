"""Gestión de memoria colectiva y registro histórico del conocimiento tácito."""

from __future__ import annotations

import json
import pathlib
import re
import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Iterable, Sequence

_TOKEN_RE = re.compile(r"[\wáéíóúñü]+", re.IGNORECASE)


@dataclass(frozen=True)
class MemoryRecord:
    """Entrada almacenada dentro de la memoria colectiva."""

    identifier: str
    timestamp: str
    channel: str
    author: str
    summary: str
    content: str
    tags: tuple[str, ...]
    decisions: tuple[str, ...]

    def matches_channel(self, name: str) -> bool:
        return self.channel.lower() == name.lower()


class CollectiveMemory:
    """Persiste eventos colaborativos y permite consultarlos semánticamente."""

    def __init__(self, storage_path: str | pathlib.Path | None = None):
        base_path = pathlib.Path(storage_path) if storage_path else pathlib.Path("Documentacion/memoria_colectiva.json")
        self.path = base_path.expanduser().resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._records: list[MemoryRecord] = []
        self._tokens: dict[str, tuple[str, ...]] = {}
        self._load()

    # ------------------------------------------------------------------
    # Persistencia
    def _load(self) -> None:
        if not self.path.exists():
            self._records = []
            self._tokens = {}
            return
        with self.path.open("r", encoding="utf-8") as stream:
            raw = json.load(stream)
        self._records = [
            MemoryRecord(
                identifier=entry["identifier"],
                timestamp=entry["timestamp"],
                channel=entry.get("channel", "desconocido"),
                author=entry.get("author", "desconocido"),
                summary=entry.get("summary", ""),
                content=entry.get("content", ""),
                tags=tuple(entry.get("tags", ())),
                decisions=tuple(entry.get("decisions", ())),
            )
            for entry in raw
        ]
        self._rebuild_tokens()

    def _persist(self) -> None:
        payload = [asdict(record) for record in self._records]
        with self.path.open("w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)

    def _rebuild_tokens(self) -> None:
        self._tokens = {
            record.identifier: _tokenize(" ".join((record.summary, record.content, " ".join(record.tags), " ".join(record.decisions))))
            for record in self._records
        }

    # ------------------------------------------------------------------
    # Operaciones públicas
    def capture(
        self,
        *,
        channel: str,
        author: str,
        content: str,
        summary: str | None = None,
        tags: Sequence[str] | None = None,
        decisions: Sequence[str] | None = None,
    ) -> MemoryRecord:
        """Registra un nuevo evento en la memoria colectiva."""

        entry = MemoryRecord(
            identifier=str(uuid.uuid4()),
            timestamp=datetime.now(tz=UTC).isoformat(timespec="seconds"),
            channel=channel,
            author=author,
            summary=summary or content[:140],
            content=content,
            tags=tuple(sorted({tag.strip() for tag in tags or () if tag.strip()})),
            decisions=tuple(decisions or ()),
        )
        self._records.append(entry)
        self._tokens[entry.identifier] = _tokenize(
            " ".join((entry.summary, entry.content, " ".join(entry.tags), " ".join(entry.decisions)))
        )
        self._persist()
        return entry

    def search(self, query: str, limit: int = 5, *, channels: Iterable[str] | None = None) -> list[MemoryRecord]:
        tokens = _tokenize(query)
        if not tokens:
            return []
        channel_filter = {name.lower() for name in channels} if channels else None

        ranked: list[tuple[float, MemoryRecord]] = []
        for record in self._records:
            if channel_filter and record.channel.lower() not in channel_filter:
                continue
            record_tokens = self._tokens.get(record.identifier, ())
            score = 0.0
            if not record_tokens:
                continue
            record_freqs = _term_frequencies(record_tokens)
            for token in tokens:
                score += record_freqs.get(token, 0)
            if score:
                ranked.append((score, record))

        ranked.sort(key=lambda item: (item[0], item[1].timestamp), reverse=True)
        return [record for _, record in ranked[:limit]]

    def list_recent(self, limit: int = 10) -> list[MemoryRecord]:
        return sorted(self._records, key=lambda record: record.timestamp, reverse=True)[:limit]

    def channels(self) -> list[str]:
        return sorted({record.channel for record in self._records})


def _tokenize(text: str) -> tuple[str, ...]:
    return tuple(token.lower() for token in _TOKEN_RE.findall(text))


def _term_frequencies(tokens: Sequence[str]) -> dict[str, int]:
    freqs: dict[str, int] = {}
    for token in tokens:
        freqs[token] = freqs.get(token, 0) + 1
    return freqs


__all__ = ["CollectiveMemory", "MemoryRecord"]

