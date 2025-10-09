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


def run_interactive(
    agent: DungeonLifeAgent, *, greeting: Optional[str] = None
) -> None:
    """Ejecuta el bucle interactivo compartido entre `willow` y `run_agent.py`."""

    if greeting:
        print(greeting)

    while True:
        try:
            message = input("consulta> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()  # nueva línea
            break

        lowered = message.lower()

        if lowered in {"salir", "exit", "quit"}:
            break

        if lowered in {"ayuda", "help"}:
            print(HELP_TEXT)
            print()
            continue

        if lowered.startswith("sugerencias"):
            parts = message.split()
            if len(parts) < 2:
                print("Debes indicar al menos un prefijo para obtener sugerencias.")
                print()
                continue
            limit = 5
            if parts[-1].isdigit():
                limit = int(parts[-1])
                parts = parts[:-1]
            prefix = " ".join(parts[1:])
            suggestions = agent.suggest_queries(prefix, limit=limit)
            if suggestions:
                for suggestion in suggestions:
                    print(f"• {suggestion}")
            else:
                print("Sin sugerencias para ese prefijo.")
            print()
            continue

        if lowered.startswith("refrescar"):
            _, *rest = message.split(maxsplit=1)
            paths = [rest[0]] if rest else None
            agent.refresh_knowledge(paths=paths)
            print("Índice actualizado.")
            print()
            continue

        if lowered in {"metricas", "metrics"}:
            print(agent.get_metrics_report())
            print()
            continue

        if lowered.startswith("metricas export"):
            parts = message.split(maxsplit=2)
            if len(parts) < 3:
                print("Debes indicar la ruta destino: metricas export <ruta.csv>")
            else:
                path = agent.metrics.export_csv(parts[2])
                print(f"Métricas exportadas a {path}")
            print()
            continue

        if lowered.startswith("memoria registrar"):
            payload = message[len("memoria registrar") :].strip()
            fields = [field.strip() for field in payload.split(";") if field.strip()]
            if len(fields) < 4:
                print(
                    "Formato esperado: memoria registrar "
                    "canal;autor;resumen;contenido[;tags][;decisiones]"
                )
                print()
                continue
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
            print(f"Memoria registrada ({record.identifier[:8]}…) en canal {record.channel}.")
            print()
            continue

        if lowered.startswith("memoria buscar"):
            parts = message.split()
            if len(parts) < 3:
                print("Uso: memoria buscar <consulta> [limite]")
                print()
                continue
            limit = 5
            if parts[-1].isdigit():
                limit = int(parts[-1])
                parts = parts[:-1]
            query = " ".join(parts[2:])
            results = agent.search_memory(query, limit=limit)
            if not results:
                print("Sin coincidencias en memoria colectiva.")
            else:
                for record in results:
                    tags = ", ".join(record.tags) if record.tags else "sin tags"
                    print(
                        f"[{record.timestamp}] {record.channel} · {record.author} → "
                        f"{record.summary} ({tags})"
                    )
            print()
            continue

        if lowered == "memoria canales":
            channels = agent.list_memory_channels()
            if channels:
                for channel in channels:
                    print(f"• {channel}")
            else:
                print("Sin canales registrados aún.")
            print()
            continue

        if lowered == "pipeline listar":
            for name in agent.list_asset_pipelines():
                print(f"• {name}")
            print()
            continue

        if lowered.startswith("pipeline ver"):
            parts = message.split(maxsplit=2)
            if len(parts) < 3:
                print("Uso: pipeline ver <nombre>")
            else:
                try:
                    print(agent.describe_asset_pipeline(parts[2]))
                except ValueError as error:
                    print(error)
            print()
            continue

        if lowered.startswith("dataset analizar"):
            raw_args = message[len("dataset analizar") :].strip().split()
            metadata: dict[str, str] = {}
            for item in raw_args:
                if "=" not in item:
                    continue
                key, value = item.split("=", 1)
                metadata[key.strip()] = value.strip().strip('"')
            plan = agent.plan_dataset_analysis(metadata)
            print(plan.render())
            print()
            continue

        if lowered == "plantilla listar":
            for name in agent.list_templates():
                print(f"• {name}")
            print()
            continue

        if lowered.startswith("plantilla aplicar"):
            parts = message.split()
            if len(parts) < 3:
                print("Uso: plantilla aplicar <nombre> campo=valor ...")
                print()
                continue
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
                print(f"Error al aplicar plantilla: {error}")
            else:
                print(rendered)
            print()
            continue

        if lowered.startswith("productividad"):
            parts = message.split()
            if len(parts) != 4:
                print("Uso: productividad <rol> <tareas_completadas> <minutos>")
                print()
                continue
            role = parts[1]
            try:
                tasks = int(parts[2])
                minutes = float(parts[3])
            except ValueError:
                print("Tareas debe ser entero y minutos un número.")
            else:
                agent.register_productivity(
                    role=role, tasks_completed=tasks, session_minutes=minutes
                )
                print("Registro de productividad agregado.")
            print()
            continue

        if lowered.startswith("lm generar"):
            prompt = message[len("lm generar") :].strip()
            if not prompt:
                print("Debes proporcionar un prompt para el modelo de lenguaje.")
                print()
                continue
            try:
                output = agent.generate_with_model(prompt)
            except RuntimeError as error:
                print(error)
            else:
                print(output)
            print()
            continue

        if not message:
            continue

        response = agent.query(message)
        show_debug = bool(os.environ.get("WILLOW_DEBUG_TRACE"))
        print(response.format_text(show_debug=show_debug))
        print()

