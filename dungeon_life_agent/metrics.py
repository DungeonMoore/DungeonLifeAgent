"""Instrumentación ligera para medir rendimiento y cobertura del agente."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Dict


@dataclass
class SearchEvent:
    mode: str
    latency: float
    results: int


class MetricsRegistry:
    """Registra eventos de búsqueda y genera reportes agregados."""

    def __init__(self) -> None:
        self._search_events: list[SearchEvent] = []

    # ------------------------------------------------------------------
    # Registro de eventos
    def record_search(self, mode: str, latency: float, results: int) -> None:
        self._search_events.append(SearchEvent(mode=mode, latency=latency, results=results))

    # ------------------------------------------------------------------
    # Consultas
    def snapshot(self) -> dict[str, Dict[str, float]]:
        """Devuelve métricas agregadas listas para serializar."""

        if not self._search_events:
            return {"search": {"count": 0}}

        total_latency = sum(event.latency for event in self._search_events)
        total_results = sum(event.results for event in self._search_events)
        per_mode: dict[str, list[SearchEvent]] = {}
        for event in self._search_events:
            per_mode.setdefault(event.mode, []).append(event)

        summary = {
            "search": {
                "count": len(self._search_events),
                "average_latency": total_latency / len(self._search_events),
                "max_latency": max(event.latency for event in self._search_events),
                "average_results": total_results / len(self._search_events),
            }
        }

        for mode, events in per_mode.items():
            summary[f"mode:{mode}"] = {
                "count": len(events),
                "average_latency": mean(event.latency for event in events),
                "max_latency": max(event.latency for event in events),
                "average_results": mean(event.results for event in events),
            }
        return summary

    def format_report(self) -> str:
        """Crea un reporte textual amigable."""

        data = self.snapshot()
        count = data.get("search", {}).get("count", 0)
        if not count:
            return "Sin métricas registradas aún. Ejecuta consultas para generarlas."

        lines = ["📊 Métricas de búsqueda acumuladas"]
        search = data["search"]
        lines.append(
            f"Total consultas: {int(search['count'])} | Latencia promedio: {search['average_latency']:.3f}s | "
            f"Máxima latencia: {search['max_latency']:.3f}s | Resultados promedio: {search['average_results']:.1f}"
        )

        for key, values in data.items():
            if not key.startswith("mode:"):
                continue
            mode_name = key.split(":", 1)[1]
            lines.append(
                f"  - {mode_name}: {int(values['count'])} consultas, "
                f"latencia promedio {values['average_latency']:.3f}s, resultados {values['average_results']:.1f}"
            )
        return "\n".join(lines)

    def reset(self) -> None:
        self._search_events.clear()


__all__ = ["MetricsRegistry", "SearchEvent"]
