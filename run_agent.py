"""Interfaz interactiva rápida para el Dungeon Life Agent."""

from __future__ import annotations

from dungeon_life_agent.agent import DungeonLifeAgent


def main() -> None:
    agent = DungeonLifeAgent()
    print("🌿 Willow listo. Escribe 'salir' para terminar.")
    while True:
        try:
            message = input("consulta> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()  # nueva línea
            break
        if message.lower() in {"salir", "exit", "quit"}:
            break
        if not message:
            continue
        response = agent.query(message)
        print(response.format_text())
        print()


if __name__ == "__main__":
    main()
