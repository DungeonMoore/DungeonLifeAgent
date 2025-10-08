import pytest

from dungeon_life_agent.agent import DungeonLifeAgent
from dungeon_life_agent.llm import EchoLanguageModel


def test_query_with_role_changes_tone():
    agent = DungeonLifeAgent()
    response = agent.query("estado del roadmap", role="productor")
    assert "Respuesta directa" in response.summary or "Resultado" in response.summary


def test_mode_permissions_are_enforced():
    agent = DungeonLifeAgent()
    with pytest.raises(PermissionError):
        agent.use_tool("git_status", mode="consultor", path=".")


def test_suggest_queries_returns_values():
    agent = DungeonLifeAgent()
    suggestions = agent.suggest_queries("tax")
    assert suggestions


def test_metrics_snapshot_records_queries():
    agent = DungeonLifeAgent()
    agent.query("arquitectura tecnica")
    snapshot = agent.metrics_snapshot()
    assert snapshot.get("search.count", 0) >= 1


def test_agent_collective_memory_and_pipelines():
    agent = DungeonLifeAgent()
    record = agent.capture_memory_event(
        channel="general",
        author="tester",
        content="Se integró pipeline Blender",
        summary="Integración pipeline",
        tags=["pipeline"],
        decisions=["medio:documentar"]
    )
    assert record.channel == "general"
    results = agent.search_memory("pipeline")
    assert results
    pipelines = agent.list_asset_pipelines()
    assert "unreal" in pipelines


def test_agent_dataset_and_templates():
    agent = DungeonLifeAgent()
    plan = agent.plan_dataset_analysis({"formato": "csv", "dominio": "narrativa", "tamanio": "500"})
    assert "Dataset" in plan.overview
    templates = agent.list_templates()
    assert "bitacora_sesion" in templates
    rendered = agent.apply_template(
        "bitacora_sesion",
        {
            "rol": "productor",
            "objetivo": "Revisión Fase 3",
            "decisiones": "Se adoptó memoria colectiva.",
            "seguimiento": "Actualizar dashboard"
        },
    )
    assert "Bitácora" in rendered


def test_agent_generates_with_language_model():
    agent = DungeonLifeAgent(language_model=EchoLanguageModel())
    output = agent.generate_with_model("Hola equipo")
    assert "Hola equipo" in output
