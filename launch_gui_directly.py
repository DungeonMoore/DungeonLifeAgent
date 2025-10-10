#!/usr/bin/env python3
"""
Script directo para lanzar la GUI mejorada de Willow
"""

import os
import sys

# Configurar codificación UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    """Lanzar la GUI directamente."""
    print("🚀 DUNGEON LIFE AGENT - GUI MEJORADA")
    print("=" * 50)
    print("🎯 Características implementadas:")
    print("✅ Formateo enriquecido con syntax highlighting")
    print("✅ Persistencia automática de conversaciones")
    print("✅ Botón para limpiar historial de chat")
    print("✅ Feedback visual (estados, indicadores)")
    print("✅ Funcionalidad copiar/pegar mejorada")
    print("✅ Menú contextual con clic derecho")
    print()
    print("💡 La ventana gráfica se abrirá en unos segundos...")
    print("⏳ Iniciando interfaz mejorada...")

    try:
        from dungeon_life_agent.gui import launch_app

        print("✅ Importación exitosa")
        print("🔧 Lanzando interfaz gráfica mejorada...")

        # Lanzar la aplicación
        launch_app()

    except KeyboardInterrupt:
        print("\n\n👋 GUI cerrada por el usuario")
    except Exception as e:
        print(f"\n❌ Error al lanzar GUI: {e}")
        print("\n🔧 Soluciones alternativas:")
        print("• Usa headless: python run_gui.py --ask 'tu pregunta'")
        print("• Usa CLI: python -m dungeon_life_agent.cli")
        print("• Verifica que tengas entorno gráfico disponible")

if __name__ == "__main__":
    main()