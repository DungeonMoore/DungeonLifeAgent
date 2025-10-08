"""MVP funcional del Dungeon Life Agent (Willow).

Este paquete ofrece una implementación ligera del agente descrito en la
documentación del ecosistema Dungeon Life. Incluye capacidades básicas de
consulta, clasificación y asistencia contextual para diferentes roles
profesionales, operando de forma local y sin dependencias de modelos
externos.
"""

from .agent import DungeonLifeAgent
from .mode_manager import Mode

__all__ = ["DungeonLifeAgent", "Mode"]
