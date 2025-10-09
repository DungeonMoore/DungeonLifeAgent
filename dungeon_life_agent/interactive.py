"""Utilidades compartidas para el modo interactivo del agente."""

from __future__ import annotations

import os
from typing import Optional

from .agent import DungeonLifeAgent

HELP_TEXT = """Comandos disponibles:\n" \
    "  • sugerencias <prefijo> [limite] → muestra autocompletado\n" \
    "  • refrescar [ruta.md] → reconstruye el índice (modo colaborador)\n" \
    "  • metricas → imprime métricas acumuladas de la sesión\n" \
    "  • metricas export <ruta.csv> → exporta snapshot a CSV\n" \
    "  • memoria registrar canal;autor;resumen;contenido[;tags][;decisiones]\n" \
    "  • memoria buscar <consulta> [limite]\n" \
    "  • memoria canales → lista canales registrados\n" \
    "  • pipeline listar → muestra pipelines disponibles\n" \
    "  • pipeline ver <nombre> → describe pipeline\n" \
    "  • dataset analizar clave=valor ... → genera plan de análisis\n" \
    "  • plantilla listar → plantillas disponibles\n" \
    "  • plantilla aplicar <nombre> campo=valor ...\n" \
    "  • productividad <rol> <tareas> <minutos> → registra productividad\n" \
    "  • lm generar <prompt> → utiliza el modelo configurado\n" \
    "  • salir → termina la interacción\n" \
    "Cualquier otro texto se interpreta como consulta en modo consultor."""


def process_interactive_message(
    agent: DungeonLifeAgent, message: str, *, show_debug: bool = False
) -> tuple[bool, str]:
    """Procesa un mensaje y devuelve si continuar y la respuesta generada."""

    stripped = message.strip()
    if not stripped:
        return True, ""

    lowered = stripped.lower()

    if lowered in {"salir", "exit", "quit"}:
        return False, ""

    if lowered in {"ayuda", "help"}:
        return True, HELP_TEXT

    if lowered.startswith("sugerencias"):
        parts = stripped.split()
        if len(parts) < 2:
            return True, "Debes indicar al menos un prefijo para obtener sugerencias."
        limit = 5
        if parts[-1].isdigit():
            limit = int(parts[-1])
            parts = parts[:-1]
        prefix = " ".join(parts[1:])
        suggestions = agent.suggest_queries(prefix, limit=limit)
        if suggestions:
            return True, "\n".join(f"• {suggestion}" for suggestion in suggestions)
        return True, "Sin sugerencias para ese prefijo."

    if lowered.startswith("refrescar"):
        _, *rest = stripped.split(maxsplit=1)
        paths = [rest[0]] if rest else None
        agent.refresh_knowledge(paths=paths)
        return True, "Índice actualizado."

    if lowered in {"metricas", "metrics"}:
        return True, agent.get_metrics_report()

    if lowered.startswith("metricas export"):
        parts = stripped.split(maxsplit=2)
        if len(parts) < 3:
            return True, "Debes indicar la ruta destino: metricas export <ruta.csv>"
        path = agent.metrics.export_csv(parts[2])
        return True, f"Métricas exportadas a {path}"

    if lowered.startswith("memoria registrar"):
        payload = stripped[len("memoria registrar") :].strip()
        fields = [field.strip() for field in payload.split(";") if field.strip()]
        if len(fields) < 4:
            return (
                True,
                "Formato esperado: memoria registrar "
                "canal;autor;resumen;contenido[;tags][;decisiones]",
            )
        channel, author, summary, content, *extra = fields
        tags = extra[0].split(",") if extra else []
        decisions = extra[1].split("|") if len(extra) > 1 else []
        record = agent.capture_memory_event(
            channel=channel,
            author=author,
            summary=summary,
            content=content,
            tags=[tag.strip() for tag in tags if tag.strip()],
            decisions=[decision.strip() for decision in decisions if decision.strip()],
        )
        return True, f"Memoria registrada ({record.identifier[:8]}…) en canal {record.channel}."

    if lowered.startswith("memoria buscar"):
        parts = stripped.split()
        if len(parts) < 3:
            return True, "Uso: memoria buscar <consulta> [limite]"
        limit = 5
        if parts[-1].isdigit():
            limit = int(parts[-1])
            parts = parts[:-1]
        query = " ".join(parts[2:])
        results = agent.search_memory(query, limit=limit)
        if not results:
            return True, "Sin coincidencias en memoria colectiva."
        lines = []
        for record in results:
            tags = ", ".join(record.tags) if record.tags else "sin tags"
            lines.append(
                f"[{record.timestamp}] {record.channel} · {record.author} → "
                f"{record.summary} ({tags})"
            )
        return True, "\n".join(lines)

    if lowered == "memoria canales":
        channels = agent.list_memory_channels()
        if channels:
            return True, "\n".join(f"• {channel}" for channel in channels)
        return True, "Sin canales registrados aún."

    if lowered == "pipeline listar":
        pipelines = agent.list_asset_pipelines()
        if pipelines:
            return True, "\n".join(f"• {name}" for name in pipelines)
        return True, "Sin pipelines registrados."

    if lowered.startswith("pipeline ver"):
        parts = stripped.split(maxsplit=2)
        if len(parts) < 3:
            return True, "Uso: pipeline ver <nombre>"
        try:
            return True, agent.describe_asset_pipeline(parts[2])
        except ValueError as error:
            return True, str(error)

    if lowered.startswith("dataset analizar"):
        raw_args = stripped[len("dataset analizar") :].strip().split()
        metadata: dict[str, str] = {}
        for item in raw_args:
            if "=" not in item:
                continue
            key, value = item.split("=", 1)
            metadata[key.strip()] = value.strip().strip('"')
        plan = agent.plan_dataset_analysis(metadata)
        return True, plan.render()

    if lowered == "plantilla listar":
        templates = agent.list_templates()
        if templates:
            return True, "\n".join(f"• {name}" for name in templates)
        return True, "Sin plantillas registradas."

    if lowered.startswith("plantilla aplicar"):
        parts = stripped.split()
        if len(parts) < 3:
            return True, "Uso: plantilla aplicar <nombre> campo=valor ..."
        name = parts[2]
        context: dict[str, str] = {}
        for item in parts[3:]:
            if "=" not in item:
                continue
            key, value = item.split("=", 1)
            context[key.strip()] = value.strip().strip('"')
        try:
            rendered = agent.apply_template(name, context)
        except ValueError as error:
            return True, f"Error al aplicar plantilla: {error}"
        return True, rendered

    if lowered.startswith("productividad"):
        parts = stripped.split()
        if len(parts) != 4:
            return True, "Uso: productividad <rol> <tareas_completadas> <minutos>"
        role = parts[1]
        try:
            tasks = int(parts[2])
            minutes = float(parts[3])
        except ValueError:
            return True, "Tareas debe ser entero y minutos un número."
        agent.register_productivity(
            role=role, tasks_completed=tasks, session_minutes=minutes
        )
        return True, "Registro de productividad agregado."

    if lowered.startswith("lm generar"):
        prompt = stripped[len("lm generar") :].strip()
        if not prompt:
            return True, "Debes proporcionar un prompt para el modelo de lenguaje."
        try:
            output = agent.generate_with_model(prompt)
        except RuntimeError as error:
            return True, str(error)
        return True, output

    response = agent.query(stripped)
    return True, response.format_text(show_debug=show_debug)


def run_interactive(
    agent: DungeonLifeAgent, *, greeting: Optional[str] = None
) -> None:
    """Ejecuta el bucle interactivo compartido entre `willow` y `run_agent.py`."""

    if greeting:
        print(greeting)

    show_debug = bool(os.environ.get("WILLOW_DEBUG_TRACE"))

    while True:
        try:
            message = input("consulta> ")
        except (EOFError, KeyboardInterrupt):
            print()  # nueva línea
            break

        should_continue, output = process_interactive_message(
            agent, message, show_debug=show_debug
        )

        if output:
            print(output)
            print()

        if not should_continue:
            break

