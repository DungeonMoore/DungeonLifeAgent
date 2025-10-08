"""Instrumentación ligera para medir rendimiento y cobertura del agente."""

from __future__ import annotations

import csv
import pathlib
from dataclasses import dataclass
from statistics import mean
from typing import Dict


@dataclass
class SearchEvent:
    mode: str
    latency: float
    results: int


@dataclass
class ProductivityEvent:
    role: str
    tasks_completed: int
    minutes: float


@dataclass
class DecisionEvent:
    identifier: str
    mode: str
    impact: str
    description: str


class MetricsRegistry:
    """Registra eventos de búsqueda y genera reportes agregados."""

    def __init__(self) -> None:
        self._search_events: list[SearchEvent] = []
        self._productivity_events: list[ProductivityEvent] = []
        self._decision_events: list[DecisionEvent] = []

    # ------------------------------------------------------------------
    # Registro de eventos
    def record_search(self, mode: str, latency: float, results: int) -> None:
        self._search_events.append(SearchEvent(mode=mode, latency=latency, results=results))

    def record_productivity(self, *, role: str, tasks_completed: int, minutes: float) -> None:
        self._productivity_events.append(
            ProductivityEvent(role=role, tasks_completed=max(0, tasks_completed), minutes=max(0.0, minutes))
        )

    def record_decision(self, *, identifier: str, mode: str, description: str) -> None:
        impact = description.split(":", 1)[0].strip().lower() if ":" in description else "general"
        self._decision_events.append(DecisionEvent(identifier=identifier, mode=mode, impact=impact, description=description))

    # ------------------------------------------------------------------
    # Consultas
    def snapshot(self) -> dict[str, Dict[str, float]]:
        """Devuelve métricas agregadas listas para serializar."""

        summary: dict[str, Dict[str, float]] = {"search": {"count": 0}}

        if self._search_events:
            total_latency = sum(event.latency for event in self._search_events)
            total_results = sum(event.results for event in self._search_events)
            per_mode: dict[str, list[SearchEvent]] = {}
            for event in self._search_events:
                per_mode.setdefault(event.mode, []).append(event)

            summary["search"] = {
                "count": len(self._search_events),
                "average_latency": total_latency / len(self._search_events),
                "max_latency": max(event.latency for event in self._search_events),
                "average_results": total_results / len(self._search_events),
            }

            for mode, events in per_mode.items():
                summary[f"mode:{mode}"] = {
                    "count": len(events),
                    "average_latency": mean(event.latency for event in events),
                    "max_latency": max(event.latency for event in events),
                    "average_results": mean(event.results for event in events),
                }

        if self._productivity_events:
            total_tasks = sum(event.tasks_completed for event in self._productivity_events)
            total_minutes = sum(event.minutes for event in self._productivity_events)
            by_role: dict[str, list[ProductivityEvent]] = {}
            for event in self._productivity_events:
                by_role.setdefault(event.role, []).append(event)
            summary["productivity"] = {
                "count": len(self._productivity_events),
                "tasks_total": float(total_tasks),
                "minutes_total": total_minutes,
                "tasks_per_hour": (total_tasks / (total_minutes / 60)) if total_minutes else 0.0,
            }
            for role, events in by_role.items():
                summary[f"role:{role}"] = {
                    "count": len(events),
                    "tasks_total": float(sum(item.tasks_completed for item in events)),
                    "minutes_total": sum(item.minutes for item in events),
                }

        if self._decision_events:
            summary["decisions"] = {"count": float(len(self._decision_events))}
            impact_counter: dict[str, int] = {}
            for event in self._decision_events:
                impact_counter[event.impact] = impact_counter.get(event.impact, 0) + 1
            for impact, count in impact_counter.items():
                summary[f"decision_impact:{impact}"] = {"count": float(count)}
        return summary

    def format_report(self) -> str:
        """Crea un reporte textual amigable."""

        data = self.snapshot()
        count = data.get("search", {}).get("count", 0)
        lines = ["📊 Tablero operativo del agente"]

        if count:
            search = data["search"]
            lines.append(
                f"Consultas: {int(search['count'])} | Latencia promedio: {search.get('average_latency', 0):.3f}s | "
                f"Máxima: {search.get('max_latency', 0):.3f}s | Resultados promedio: {search.get('average_results', 0):.1f}"
            )
            for key, values in data.items():
                if not key.startswith("mode:"):
                    continue
                mode_name = key.split(":", 1)[1]
                lines.append(
                    f"  - {mode_name}: {int(values['count'])} consultas, latencia {values.get('average_latency', 0):.3f}s"
                )
        else:
            lines.append("Sin consultas registradas aún.")

        productivity = data.get("productivity")
        if productivity:
            lines.append(
                f"Productividad: {int(productivity['count'])} sesiones | Tareas totales: {productivity['tasks_total']:.0f} | "
                f"Horas invertidas: {productivity['minutes_total']/60:.2f} | Tareas/hora: {productivity['tasks_per_hour']:.2f}"
            )

        decision_data = data.get("decisions")
        if decision_data:
            lines.append(f"Decisiones registradas: {int(decision_data['count'])}")
            for key, values in data.items():
                if key.startswith("decision_impact:"):
                    impact = key.split(":", 1)[1]
                    lines.append(f"  - {impact}: {int(values['count'])}")
        return "\n".join(lines)

    def reset(self) -> None:
        self._search_events.clear()
        self._productivity_events.clear()
        self._decision_events.clear()

    def export_csv(self, destination: str | pathlib.Path) -> pathlib.Path:
        path = pathlib.Path(destination).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        data = self.snapshot()
        rows: list[dict[str, object]] = []
        for category, metrics in data.items():
            for metric, value in metrics.items():
                rows.append({"metric": f"{category}.{metric}", "value": value})
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["metric", "value"])
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return path


__all__ = [
    "MetricsRegistry",
    "SearchEvent",
    "ProductivityEvent",
    "DecisionEvent",
]
