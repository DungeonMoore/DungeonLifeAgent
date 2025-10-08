#!/usr/bin/env python3
"""
Script de prueba para integración Ollama + Willow
Ejecutar desde el directorio raíz del proyecto
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ollama_connection():
    """Prueba básica de conexión con Ollama"""
    print("Probando conexion con Ollama...")

    try:
        from dungeon_life_agent.llm import OllamaClient

        # Crear cliente Ollama
        ollama = OllamaClient(model="gemma3:4b", host="http://localhost:11434")

        # Probar generación simple
        test_prompt = "¿Qué es la memoria colectiva en el contexto de un agente IA?"
        print(f"Enviando prompt: {test_prompt}")

        response = ollama.generate(test_prompt)
        print(f"Respuesta recibida: {response[:200]}...")

        return True

    except Exception as e:
        print(f"Error de conexion: {e}")
        return False

def test_willow_with_ollama():
    """Prueba Willow con integración Ollama"""
    print("\nProbando Willow con Ollama...")

    try:
        from dungeon_life_agent.llm import OllamaClient
        from dungeon_life_agent import DungeonLifeAgent

        # Crear cliente Ollama
        ollama = OllamaClient(model="gemma3:4b")

        # Crear agente con integración Ollama
        agent = DungeonLifeAgent(language_model=ollama)

        # Probar comandos disponibles
        print("Probando funcionalidades disponibles...")

        # 1. Generar respuesta con modelo
        prompt = "Resume qué es la memoria colectiva del agente"
        response = agent.generate_with_model(prompt)
        print(f"LM generar: {response[:150]}...")

        # 2. Listar pipelines disponibles
        pipelines = agent.list_asset_pipelines()
        print(f"Pipelines disponibles: {pipelines}")

        # 3. Listar plantillas
        templates = agent.list_templates()
        print(f"Plantillas disponibles: {templates}")

        # 4. Probar análisis de dataset
        dataset_plan = agent.plan_dataset_analysis({
            "formato": "csv",
            "dominio": "juegos",
            "tamanio": "1000"
        })
        print(f"Analisis dataset: {dataset_plan.overview}")

        return True

    except Exception as e:
        print(f"Error con Willow: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Iniciando pruebas de integracion Ollama + Willow")
    print("=" * 60)

    # Verificar si Ollama está corriendo
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        print("Ollama esta corriendo correctamente")
    except Exception as e:
        print(f"Ollama no esta corriendo. Error: {e}")
        print("Inicialo con: ollama serve")
        sys.exit(1)

    # Probar conexión básica
    if test_ollama_connection():
        print("\n" + "=" * 60)

        # Probar integración completa
        if test_willow_with_ollama():
            print("\nIntegracion exitosa! Willow + Ollama funcionando correctamente")
        else:
            print("\nProblemas con la integracion Willow-Ollama")
    else:
        print("\nNo se pudo conectar con Ollama")