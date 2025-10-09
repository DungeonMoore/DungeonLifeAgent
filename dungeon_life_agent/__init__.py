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

try:  # pragma: no cover - import opcional para mantener compatibilidad
    from .advanced_embeddings import EmbeddingSystem
except Exception:  # pragma: no cover - disponibilidad opcional
    EmbeddingSystem = None  # type: ignore

__all__ = ["DungeonLifeAgent", "Mode"]

if EmbeddingSystem is not None:  # pragma: no branch - exporta solo si está disponible
    __all__.append("EmbeddingSystem")
