"""MVP funcional del Dungeon Life Agent (Willow).

Este paquete ofrece una implementación ligera del agente descrito en la
documentación del ecosistema Dungeon Life. Incluye capacidades básicas de
consulta, clasificación y asistencia contextual para diferentes roles
profesionales, operando de forma local y sin dependencias de modelos
externos. Incluye memoria colectiva, pipelines especializados y puntos de
integración con modelos de lenguaje locales como Ollama.
"""

from .agent import DungeonLifeAgent
from .mode_manager import Mode

__all__ = ["DungeonLifeAgent", "Mode"]
