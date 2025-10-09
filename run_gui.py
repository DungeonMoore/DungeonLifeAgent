"""Lanza la interfaz gráfica de Willow o ejecuta consultas en modo headless."""

from __future__ import annotations

import argparse
import sys

from dungeon_life_agent.gui import launch_app, run_headless_query, supports_windowing


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Interfaz gráfica y pruebas rápidas de Willow")
    parser.add_argument("--ask", metavar="PREGUNTA", help="Realiza una consulta rápida sin abrir la ventana")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Incluye trazas del pipeline de búsqueda en la respuesta headless",
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Evita lanzar la ventana incluso si hay entorno gráfico disponible",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.ask:
        output = run_headless_query(args.ask, show_debug=args.debug)
        if output:
            print(output)
        else:
            print("No se generó respuesta para la consulta proporcionada.", file=sys.stderr)
        if args.no_gui or not supports_windowing():
            return 0

    if args.no_gui:
        return 0

    if not supports_windowing():
        print(
            "Entorno gráfico no disponible. Exporta DISPLAY/WAYLAND_DISPLAY o usa --no-gui.",
            file=sys.stderr,
        )
        return 2

    launch_app()
    return 0


if __name__ == "__main__":  # pragma: no cover - punto de entrada manual
    sys.exit(main())
