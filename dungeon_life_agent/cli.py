"""CLI mínima para interactuar con Willow."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from .agent import DungeonLifeAgent
from .banner import print_welcome
from .interactive import run_interactive


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
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Incluye la traza detallada del pipeline en la salida",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    # Solo mostrar banner si NO hay argumentos (es decir, se ejecutó solo "willow")
    if argv is None and not os.environ.get("WILLOW_HIDE_BANNER"):
        print_welcome()

    parser = build_parser()
    args = parser.parse_args(argv)

    # Si no hay argumentos, iniciar modo interactivo como python run_agent.py
    if argv is None and not args.message and not any([
        args.list_docs,
        args.tool,
        args.classify,
        args.suggest,
        args.suggest_queries,
        args.metrics,
        args.refresh_index,
    ]):
        # Iniciar Ollama automáticamente para modo interactivo
        try:
            from .ollama_manager import create_ollama_manager
            from .llm import OllamaClient

            ollama_manager = create_ollama_manager(verbose=False)
            ollama_available = ollama_manager.ensure_running()

            if ollama_available:
                print("[OK] Ollama iniciado - funcionalidades de IA local disponibles")
                ollama_client = OllamaClient(model=ollama_manager.model)
                agent = DungeonLifeAgent(language_model=ollama_client)
            else:
                print("[WARNING] Ejecutando sin Ollama - funcionalidades basicas disponibles")
                agent = DungeonLifeAgent()
        except Exception:
            print("[WARNING] Error iniciando Ollama - continuando con funcionalidades basicas")
            agent = DungeonLifeAgent()

        run_interactive(
            agent,
            greeting="Iniciando modo interactivo... (escribe 'salir' para terminar)\n",
        )
        return 0

    # Iniciar Ollama para comandos que podrían necesitar modelo de lenguaje
    needs_ollama = args.message or args.suggest or args.classify
    if needs_ollama:
        try:
            from .ollama_manager import create_ollama_manager
            from .llm import OllamaClient

            ollama_manager = create_ollama_manager(verbose=False)
            ollama_available = ollama_manager.ensure_running()

            if ollama_available:
                ollama_client = OllamaClient(model=ollama_manager.model)
                agent = DungeonLifeAgent(
                    documentation_path=args.docs,
                    config_path=args.config,
                    language_model=ollama_client
                )
            else:
                agent = DungeonLifeAgent(documentation_path=args.docs, config_path=args.config)
        except Exception:
            agent = DungeonLifeAgent(documentation_path=args.docs, config_path=args.config)
    else:
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

    if args.message and args.message.strip().lower() == "help":
        parser.print_help()
        return 0

    if not args.message:
        parser.print_help()
        return 0

    response = agent.query(args.message, mode=args.mode, role=args.role, limit=args.limit)
    print(response.format_text(show_debug=args.debug))
    return 0


if __name__ == "__main__":
    sys.exit(main())
