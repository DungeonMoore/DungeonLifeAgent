"""Capa de conocimiento ligera para el MVP del Dungeon Life Agent."""

from __future__ import annotations

import math
import pathlib
import re
from dataclasses import dataclass
from typing import Iterable, List, Sequence


_TOKEN_RE = re.compile(r"[\wáéíóúñü]+", re.IGNORECASE)


@dataclass
class DocumentSection:
    """Representa una sección individual dentro de un documento markdown."""

    document_path: pathlib.Path
    title: str
    content: str
    metadata: dict[str, str]
    heading_level: int
    tokens: tuple[str, ...]

    @property
    def identifier(self) -> str:
        return f"{self.document_path.name}::{self.title or 'raiz'}"

    def build_snippet(self, max_chars: int = 280) -> str:
        clean = " ".join(self.content.split())
        return clean[: max_chars - 3] + "..." if len(clean) > max_chars else clean


@dataclass
class SearchResult:
    section: DocumentSection
    score: float


class DocumentationIndex:
    """Indexa la carpeta de documentación usando una métrica TF-IDF ligera."""

    def __init__(self, root: str | pathlib.Path):
        self.root = pathlib.Path(root)
        if not self.root.exists():
            raise FileNotFoundError(f"No se encontró la carpeta de documentación: {self.root}")
        self.sections: list[DocumentSection] = []
        self._idf: dict[str, float] = {}
        self._load_sections()
        self._build_index()

    # ------------------------------------------------------------------
    # API pública
    def search(self, query: str, limit: int = 3) -> list[SearchResult]:
        tokens = _tokenize(query)
        scores = []
        if not tokens:
            return []
        query_freqs = _term_frequencies(tokens)
        for section in self.sections:
            score = 0.0
            section_freqs = _term_frequencies(section.tokens)
            for token, q_freq in query_freqs.items():
                if token not in section_freqs:
                    continue
                idf = self._idf.get(token, 0.0)
                score += (q_freq * idf) * (section_freqs[token] * idf)
            if score > 0:
                scores.append(SearchResult(section=section, score=score))
        scores.sort(key=lambda result: result.score, reverse=True)
        return scores[:limit]

    def list_documents(self) -> list[pathlib.Path]:
        seen = []
        for section in self.sections:
            if section.document_path not in seen:
                seen.append(section.document_path)
        return seen

    # ------------------------------------------------------------------
    # Construcción del índice
    def _load_sections(self) -> None:
        for path in sorted(self.root.glob("*.md")):
            metadata, body = _split_front_matter(path.read_text(encoding="utf-8"))
            for title, level, content in _split_sections(body):
                tokens = tuple(_tokenize(content))
                if not tokens:
                    continue
                self.sections.append(
                    DocumentSection(
                        document_path=path,
                        title=title,
                        content=content,
                        metadata=dict(metadata),
                        heading_level=level,
                        tokens=tokens,
                    )
                )

    def _build_index(self) -> None:
        total_sections = len(self.sections)
        doc_freqs: dict[str, int] = {}
        for section in self.sections:
            for token in set(section.tokens):
                doc_freqs[token] = doc_freqs.get(token, 0) + 1
        self._idf = {
            token: math.log((1 + total_sections) / (1 + freq)) + 1
            for token, freq in doc_freqs.items()
        }


def _split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            _, header, rest = parts[:3]
            metadata = {}
            for line in header.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip('"')
            return metadata, rest
    return {}, text


def _split_sections(body: str) -> Iterable[tuple[str, int, str]]:
    current_title = ""
    current_level = 1
    current_lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("#"):
            if current_lines:
                yield current_title, current_level, "\n".join(current_lines).strip()
                current_lines = []
            hashes = len(line) - len(line.lstrip("#"))
            title = line.strip().lstrip("# ")
            current_title = title
            current_level = hashes
        else:
            current_lines.append(line)
    if current_lines:
        yield current_title, current_level, "\n".join(current_lines).strip()


def _tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in _TOKEN_RE.finditer(text)]


def _term_frequencies(tokens: Sequence[str]) -> dict[str, float]:
    frequencies: dict[str, float] = {}
    if not tokens:
        return frequencies
    factor = 1.0 / len(tokens)
    for token in tokens:
        frequencies[token] = frequencies.get(token, 0.0) + factor
    return frequencies


__all__ = ["DocumentationIndex", "SearchResult", "DocumentSection"]
