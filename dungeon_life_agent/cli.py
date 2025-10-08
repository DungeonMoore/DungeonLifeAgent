"""CLI mínima para interactuar con Willow."""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from .agent import DungeonLifeAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dungeon Life Agent - Willow")
    parser.add_argument("message", nargs="?", help="Consulta o instrucción a procesar")
    parser.add_argument("--mode", choices=["consultor", "taxonomico", "colaborador"], default="consultor")
    parser.add_argument("--role", help="Rol profesional que guía la respuesta")
    parser.add_argument("--classify", action="store_true", help="Ejecuta el modo taxonómico explicitamente")
    parser.add_argument("--suggest", action="store_true", help="Genera sugerencias colaborativas")
    parser.add_argument("--list-docs", action="store_true", help="Lista documentos disponibles")
    parser.add_argument("--config", help="Ruta alternativa de configuración YAML")
    parser.add_argument("--docs", help="Ruta a la carpeta de documentación", default="Documentacion")
    parser.add_argument("--tool", choices=["list_directory", "read_file", "git_status"], help="Herramienta a ejecutar")
    parser.add_argument("--path", help="Ruta utilizada por la herramienta seleccionada")
    parser.add_argument("--max-bytes", type=int, default=32768, help="Límite de lectura para read_file")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    agent = DungeonLifeAgent(documentation_path=args.docs, config_path=args.config)

    if args.list_docs:
        documents = agent.list_documents(mode=args.mode)
        for doc in documents:
            print(doc)
        return 0

    if args.tool:
        if not args.path:
            parser.error("--path es obligatorio al usar --tool")
        output = agent.use_tool(args.tool, mode=args.mode, path=args.path, max_bytes=args.max_bytes)
        print(output)
        return 0

    if args.classify:
        response = agent.classify(args.message or "", mode=args.mode)
        print(response.format_text())
        return 0

    if args.suggest:
        response = agent.suggest_actions(args.message or "", mode=args.mode, role=args.role)
        print(response.format_text())
        return 0

    if not args.message:
        parser.error("Debes proporcionar un mensaje o usar --list-docs/--tool")

    response = agent.query(args.message, mode=args.mode, role=args.role)
    print(response.format_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
