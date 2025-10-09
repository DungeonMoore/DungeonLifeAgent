#!/usr/bin/env python3
"""
Test script para verificar las mejoras del algoritmo de búsqueda
"""

import sys
import os
sys.path.append('.')

from dungeon_life_agent.knowledge import DocumentationIndex

def test_improved_search():
    """Prueba el algoritmo de búsqueda mejorado con consultas reales"""

    print("*** Probando algoritmo de busqueda mejorado ***")
    print("=" * 60)

    # Inicializar el índice de documentación
    try:
        index = DocumentationIndex("Documentacion")
        print(f"*** Indice cargado: {len(index.sections)} secciones encontradas")
    except Exception as e:
        print(f"*** Error cargando indice: {e}")
        return

    # Consultas de prueba
    test_queries = [
        "dime que es eldertown",
        "puedes decirme que es DTME",
        "información sobre eldertown",
        "qué es eldertown",
        "eldertown ubicación"
    ]

    for query in test_queries:
        print(f"\n*** Consulta: '{query}'")
        print("-" * 40)

        try:
            results = index.search(query, limit=3)

            if not results:
                print("*** No se encontraron resultados")
                continue

            for i, result in enumerate(results, 1):
                section = result.section
                score = result.score

                # Extraer información relevante del path y título
                path_parts = section.document_path.parts
                location = f"{path_parts[-2]}/{path_parts[-1]}" if len(path_parts) >= 2 else str(section.document_path)

                print(f"#{i} - Score: {score:.3f}")
                print(f"   Archivo: {location}")
                print(f"   Titulo: {section.title or 'Sin titulo'}")
                print(f"   Vista previa: {section.build_snippet(150)}")
                print()

        except Exception as e:
            print(f"*** Error procesando consulta '{query}': {e}")

    print("\n" + "=" * 60)
    print("*** Test completado")

if __name__ == "__main__":
    test_improved_search()