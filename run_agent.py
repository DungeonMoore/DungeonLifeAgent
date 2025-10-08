"""Interfaz interactiva rápida para el Dungeon Life Agent."""

from __future__ import annotations

from dungeon_life_agent.agent import DungeonLifeAgent

<<<<<<< ours
<<<<<<< ours
=======
HELP_TEXT = """Comandos disponibles:\n  • sugerencias <prefijo> [limite] → muestra autocompletado\n  • refrescar [ruta.md] → reconstruye el índice (modo colaborador)\n  • metricas → imprime métricas acumuladas de la sesión\n  • salir → termina la interacción\nCualquier otro texto se interpreta como consulta en modo consultor."""

>>>>>>> theirs
=======
HELP_TEXT = """Comandos disponibles:\n  • sugerencias <prefijo> [limite] → muestra autocompletado\n  • refrescar [ruta.md] → reconstruye el índice (modo colaborador)\n  • metricas → imprime métricas acumuladas de la sesión\n  • salir → termina la interacción\nCualquier otro texto se interpreta como consulta en modo consultor."""

>>>>>>> theirs

def main() -> None:
    agent = DungeonLifeAgent()
    print("🌿 Willow listo. Escribe 'salir' para terminar.")
    while True:
        try:
            message = input("consulta> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()  # nueva línea
            break
<<<<<<< ours
<<<<<<< ours
        if message.lower() in {"salir", "exit", "quit"}:
            break
=======
=======
>>>>>>> theirs
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
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
        if not message:
            continue
        response = agent.query(message)
        print(response.format_text())
        print()


if __name__ == "__main__":
    main()
