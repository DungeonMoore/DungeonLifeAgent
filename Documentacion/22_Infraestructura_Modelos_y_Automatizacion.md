---
title: "Infraestructura de Modelos y Automatización Fase 3"
version: "0.1.0"
date: "2024-06-08"
status: "draft"
author: "Dungeon Life Agent Team"
tags: ["infraestructura", "modelos", "ollama", "metricas", "pipelines"]
---

# 🧩 Infraestructura de Modelos y Automatización – Fase 3

Este documento consolida los elementos técnicos liberados durante la Fase 3 para preparar al Dungeon Life Agent ante la integración de modelos locales (ej. Ollama), automatización colaborativa y seguimiento continuo de métricas.

## 🧠 Configuración de Modelos de Lenguaje

### Cliente Ollama

```bash
# Instalar Ollama en la estación local
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelo sugerido
ollama pull llama3
```

```python
from dungeon_life_agent import DungeonLifeAgent
from dungeon_life_agent.llm import OllamaClient

agent = DungeonLifeAgent(language_model=OllamaClient(model="llama3"))
respuesta = agent.generate_with_model("Resume la última reunión de pipelines")
```

### Variables de entorno recomendadas

```bash
export WILLOW_LLM_HOST=http://localhost:11434
export WILLOW_LLM_MODEL=llama3
```

Luego ajustar el arranque:

```python
import os
from dungeon_life_agent import DungeonLifeAgent
from dungeon_life_agent.llm import OllamaClient

ollama = OllamaClient(model=os.getenv("WILLOW_LLM_MODEL", "llama3"), host=os.getenv("WILLOW_LLM_HOST", "http://localhost:11434"))
agent = DungeonLifeAgent(language_model=ollama)
```

## 🧾 Scripts y Automatizaciones

- `run_agent.py`: CLI extendido con comandos `memoria`, `pipeline`, `dataset`, `plantilla`, `metricas export` y `lm generar`.
- `dungeon_life_agent.metrics.MetricsRegistry.export_csv`: genera snapshot en CSV para tableros externos.
- `collective_memory` (CLI): persistencia en `Documentacion/memoria_colectiva.json` compatible con sincronización Git.

## 📊 Tablero de Métricas

1. Ejecutar sesiones de consulta y registrar productividad.
2. Exportar a CSV: `metricas export reportes/metrics.csv`.
3. Consumir el archivo desde hojas de cálculo o dashboards de BI.

Campos incluidos:

| Métrica | Descripción |
|---------|-------------|
| `search.count` | Total de consultas registradas |
| `search.average_latency` | Latencia promedio en segundos |
| `productivity.tasks_total` | Total de tareas reportadas |
| `productivity.tasks_per_hour` | Ritmo promedio de ejecución |
| `decisions.count` | Número de decisiones registradas |

## 🔄 Integraciones Futuras (Backlog)

- Invocar resúmenes automáticos desde Ollama al capturar eventos en memoria colectiva.
- Sincronizar pipelines con gestores externos (Jira/Notion) usando la información de `AssetPipelineNavigator`.
- Publicar métricas en dashboards Grafana utilizando el CSV exportado como fuente.

---

**Contacto:** `productor@dungeonlife.ecosystem`
