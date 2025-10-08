"""Script de comprobación rápida para el entorno local de Willow."""

from __future__ import annotations

import pathlib

from dungeon_life_agent.config import DEFAULT_CONFIG_PATH


def main() -> None:
    print("🌿 Preparando Willow para operar localmente...")
    config_path = DEFAULT_CONFIG_PATH
    if config_path.exists():
        print(f"✔ Configuración detectada en {config_path}")
    else:
        print(f"⚠ No se encontró la configuración base en {config_path}")
    docs_path = pathlib.Path("Documentacion")
    if docs_path.exists():
        total_docs = len(list(docs_path.glob("*.md")))
        print(f"✔ Documentación disponible ({total_docs} archivos .md)")
    else:
        print("⚠ No se encontró la carpeta Documentacion")
    print("Listo. Ejecuta 'python run_agent.py' o el comando 'willow' para comenzar.")


if __name__ == "__main__":
    main()
