from dungeon_life_agent.datasets import DatasetAnalysisAgent


def test_dataset_analysis_agent_generates_plan():
    agent = DatasetAnalysisAgent()
    plan = agent.analyze({"formato": "csv", "dominio": "economia", "tamanio": "12000"})
    rendered = plan.render()
    assert "Dataset detectado" in rendered
    assert "Great Expectations" in rendered
    assert "correlaciones" in rendered
