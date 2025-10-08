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
    parser.add_argument("--suggest-queries", action="store_true", help="Muestra sugerencias de autocompletado")
    parser.add_argument("--list-docs", action="store_true", help="Lista documentos disponibles")
    parser.add_argument("--config", help="Ruta alternativa de configuración YAML")
    parser.add_argument("--docs", help="Ruta a la carpeta de documentación", default="Documentacion")
    parser.add_argument("--tool", choices=["list_directory", "read_file", "git_status"], help="Herramienta a ejecutar")
    parser.add_argument("--path", help="Ruta utilizada por la herramienta seleccionada")
    parser.add_argument("--max-bytes", type=int, default=32768, help="Límite de lectura para read_file")
    parser.add_argument("--limit", type=int, default=5, help="Número máximo de resultados o sugerencias")
    parser.add_argument("--refresh-index", action="store_true", help="Reconstruye el índice de documentación")
    parser.add_argument("--metrics", action="store_true", help="Muestra métricas acumuladas del agente")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    agent = DungeonLifeAgent(documentation_path=args.docs, config_path=args.config)

    if args.refresh_index:
        paths = [args.message] if args.message else None
        agent.refresh_knowledge(paths=paths)
        print("Índice actualizado correctamente.")
        if not any([args.list_docs, args.tool, args.classify, args.suggest, args.suggest_queries, args.metrics]):
            return 0

    if args.metrics:
        print(agent.get_metrics_report())
        if not any([args.list_docs, args.tool, args.classify, args.suggest, args.suggest_queries]):
            return 0

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

    if args.suggest_queries:
        if not args.message:
            parser.error("Debes proporcionar un prefijo de consulta para --suggest-queries")
        suggestions = agent.suggest_queries(args.message, mode=args.mode, limit=args.limit)
        for suggestion in suggestions:
            print(suggestion)
        return 0

    if not args.message:
        parser.error("Debes proporcionar un mensaje o usar --list-docs/--tool")

    response = agent.query(args.message, mode=args.mode, role=args.role, limit=args.limit)
    print(response.format_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
