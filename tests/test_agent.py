import pytest

from dungeon_life_agent.agent import DungeonLifeAgent


def test_query_with_role_changes_tone():
    agent = DungeonLifeAgent()
    response = agent.query("estado del roadmap", role="productor")
    assert "Respuesta directa" in response.summary or "Resultado" in response.summary


def test_mode_permissions_are_enforced():
    agent = DungeonLifeAgent()
    with pytest.raises(PermissionError):
        agent.use_tool("git_status", mode="consultor", path=".")
