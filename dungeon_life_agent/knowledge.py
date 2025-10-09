"""Capa de conocimiento ligera para el Dungeon Life Agent."""

from __future__ import annotations

import math
import pathlib
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Sequence


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


@dataclass
class _IndexedDocument:
    path: pathlib.Path
    mtime: float
    sections: list[DocumentSection]


class DocumentationIndex:
    """Indexa la carpeta de documentación usando una métrica TF-IDF ligera."""

    def __init__(self, root: str | pathlib.Path):
        self.root = pathlib.Path(root).expanduser().resolve()
        if not self.root.exists():
            raise FileNotFoundError(f"No se encontró la carpeta de documentación: {self.root}")
        self.sections: list[DocumentSection] = []
        self._idf: dict[str, float] = {}
        self._documents: dict[pathlib.Path, _IndexedDocument] = {}
        self._suggestion_catalog: list[tuple[str, str]] = []
        self.refresh()

    # ------------------------------------------------------------------
    # API pública
    def search(self, query: str, limit: int = 3) -> list[SearchResult]:
        """Búsqueda mejorada con algoritmo matemático avanzado"""
        tokens = _tokenize_mejorado(query)
        scores = []
        if not tokens:
            return []
        query_freqs = _term_frequencies(tokens)
        for section in self.sections:
            score = self._calcular_relevancia_mejorada(tokens, section.tokens, query_freqs)
            if score > 0:
                scores.append(SearchResult(section=section, score=score))
        scores.sort(key=lambda result: result.score, reverse=True)
        return scores[:limit]

    def list_documents(self) -> list[pathlib.Path]:
        return sorted((doc.path for doc in self._documents.values()), key=lambda path: path.name)

    def refresh(self, paths: Iterable[str | pathlib.Path] | None = None) -> None:
        """Reconstruye el índice detectando cambios incrementales."""

        forced_paths = {_resolve_to_root(self.root, path) for path in paths} if paths else None
        discovered: set[pathlib.Path] = set()

        for path in sorted(self.root.rglob("*.md")):
            discovered.add(path)
            needs_update = False
            record = self._documents.get(path)
            mtime = path.stat().st_mtime
            if record is None:
                needs_update = True
            elif forced_paths and path in forced_paths:
                needs_update = True
            elif record.mtime < mtime:
                needs_update = True

            if needs_update:
                self._documents[path] = _IndexedDocument(
                    path=path,
                    mtime=mtime,
                    sections=list(_parse_sections(path)),
                )

        if paths is None:
            stale = [path for path in self._documents if path not in discovered]
        else:
            stale = [path for path in self._documents if path not in discovered and path in forced_paths]
        for path in stale:
            self._documents.pop(path, None)

        self._rebuild_cache()

    def suggest(self, prefix: str, limit: int = 5) -> list[str]:
        """Devuelve sugerencias de autocompletado basadas en títulos y etiquetas."""

        normalized_prefix = prefix.strip().lower()
        if not normalized_prefix:
            return []

        suggestions: list[str] = []
        for key, label in self._suggestion_catalog:
            if key.startswith(normalized_prefix) or any(part.startswith(normalized_prefix) for part in key.split()):
                if label not in suggestions:
                    suggestions.append(label)
            if len(suggestions) >= limit:
                break
        return suggestions

    def _calcular_relevancia_mejorada(self, query_tokens, section_tokens, query_freqs):
        """Nueva ecuación matemática corregida para búsqueda precisa"""

        # Componente 1: Matches Exactos (40% del peso total)
        # Boost masivo para términos que aparecen exactamente
        exact_matches = sum(1 for token in query_tokens if token in section_tokens)
        exact_score = exact_matches * 10.0

        # Componente 2: TF-IDF Corregido (40% del peso total)
        # CORRECCIÓN CRÍTICA: Solo una multiplicación por IDF, no dos
        tfidf_score = 0.0
        for token in query_tokens:
            if token in section_tokens and token in self._idf:
                freq_query = query_freqs.get(token, 0.0)
                freq_section = section_tokens.count(token) / len(section_tokens)
                # TF-IDF corregido: freq_query * idf * freq_section (sin idf²)
                tfidf_score += (freq_query * self._idf[token]) * freq_section

        # Componente 3: Cobertura de Consulta (20% del peso total)
        # Mide qué porcentaje de términos de la consulta están cubiertos
        query_terms_found = len(set(query_tokens) & set(section_tokens))
        coverage_bonus = (query_terms_found / len(query_tokens)) * 5.0 if query_tokens else 0

        # Componente 4: Penalización por longitud (factor multiplicativo)
        # Evita que secciones muy largas obtengan score alto por coincidencias casuales
        length_penalty = min(1.0, 1000 / len(section_tokens)) if section_tokens else 0

        # Cálculo del score final ponderado
        score_final = (exact_score * 0.4 + tfidf_score * 0.4 + coverage_bonus * 0.2) * length_penalty

        return score_final

    # ------------------------------------------------------------------
    # Construcción del índice
    def _rebuild_cache(self) -> None:
        self.sections = [
            section
            for document in sorted(self._documents.values(), key=lambda record: record.path.name)
            for section in document.sections
        ]
        self._build_index()
        self._build_suggestions()

    def _build_index(self) -> None:
        total_sections = len(self.sections)
        if total_sections == 0:
            self._idf = {}
            return
        doc_freqs: dict[str, int] = {}
        for section in self.sections:
            for token in set(section.tokens):
                doc_freqs[token] = doc_freqs.get(token, 0) + 1
        self._idf = {
            token: math.log((1 + total_sections) / (1 + freq)) + 1
            for token, freq in doc_freqs.items()
        }

    def _build_suggestions(self) -> None:
        if not self.sections:
            self._suggestion_catalog = []
            return

        scores: Counter[str] = Counter()
        labels: dict[str, str] = {}

        for record in self._documents.values():
            base_label = record.path.stem.replace("_", " ")
            base_key = base_label.lower()
            labels.setdefault(base_key, base_label)
            scores[base_key] += 1

            doc_metadata = record.sections[0].metadata if record.sections else {}
            for key in ("tags", "keywords"):
                raw = doc_metadata.get(key)
                if raw:
                    for tag in _tokenize(raw):
                        if len(tag) < 3:
                            continue
                        labels.setdefault(tag, tag)
                        scores[tag] += 1.5

            for section in record.sections:
                if section.title:
                    label = f"{record.path.stem} › {section.title}"
                    key = label.lower()
                    labels.setdefault(key, label)
                    scores[key] += 3
                    for token in _tokenize(section.title):
                        if len(token) < 3:
                            continue
                        labels.setdefault(token, token)
                        scores[token] += 1.5

        ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        self._suggestion_catalog = [(key, labels[key]) for key, _ in ordered]


def _parse_sections(path: pathlib.Path) -> Iterable[DocumentSection]:
    metadata, body = _split_front_matter(path.read_text(encoding="utf-8"))
    for title, level, content in _split_sections(body):
        tokens = tuple(_tokenize(content))
        if not tokens:
            continue
        yield DocumentSection(
            document_path=path,
            title=title,
            content=content,
            metadata=dict(metadata),
            heading_level=level,
            tokens=tokens,
        )


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


def _tokenize_mejorado(text: str) -> list[str]:
    """Tokenización inteligente para español con mejoras avanzadas"""
    import re
    import unicodedata

    # Normalización Unicode para manejar caracteres especiales españoles
    text = unicodedata.normalize('NFD', text.lower())
    text = re.sub(r'[^\w\sáéíóúñü]', ' ', text)

    # Tokenización mejorada usando regex de palabras
    tokens = re.findall(r'\b\w+\b', text)

    # Stop words en español para filtrar ruido
    stopwords = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'es', 'son',
        'era', 'eran', 'fueron', 'sea', 'sean', 'que', 'como', 'para', 'con',
        'por', 'del', 'desde', 'hasta', 'ante', 'sobre', 'tras', 'durante',
        'mediante', 'este', 'esta', 'estos', 'estas', 'este', 'esta',
        'esto', 'estos', 'estas', 'aquel', 'aquella', 'aquellos', 'aquellas',
        'uno', 'una', 'unos', 'unas', 'todo', 'toda', 'todos', 'todas',
        'muy', 'más', 'menos', 'mucho', 'poco', 'también', 'tampoco',
        'siempre', 'nunca', 'aquí', 'allí', 'allá', 'acá', 'hoy', 'ayer',
        'mañana', 'anoche', 'ahora', 'entonces', 'después', 'antes',
        'primero', 'primera', 'último', 'última', 'primero', 'primera',
        'segundo', 'segunda', 'tercero', 'tercera', 'cuarto', 'cuarta',
        'quinto', 'quinta', 'sexto', 'séptimo', 'octavo', 'noveno', 'décimo'
    }

    # Filtrar tokens: longitud mínima 3 caracteres, no stop words
    tokens_filtrados = [
        token for token in tokens
        if len(token) >= 3 and token not in stopwords
    ]

    return tokens_filtrados


def _term_frequencies(tokens: Sequence[str]) -> dict[str, float]:
    frequencies: dict[str, float] = {}
    if not tokens:
        return frequencies
    factor = 1.0 / len(tokens)
    for token in tokens:
        frequencies[token] = frequencies.get(token, 0.0) + factor
    return frequencies


def _resolve_to_root(root: pathlib.Path, path: str | pathlib.Path) -> pathlib.Path:
    candidate = pathlib.Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = (root / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return candidate


__all__ = ["DocumentationIndex", "SearchResult", "DocumentSection"]
