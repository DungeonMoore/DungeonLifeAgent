from dungeon_life_agent.knowledge import DocumentationIndex
from dungeon_life_agent.search_pipeline import SearchPipelineConfig


def _write_doc(path, metadata: str, body: str) -> None:
    path.write_text(f"---\n{metadata}\n---\n{body}", encoding="utf-8")


def test_role_bias_affects_ranking(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    atlas = docs / "atlas.md"
    rival = docs / "rival.md"

    body = """
# Eldertown
Eldertown es la capital narrativa de Atlas.
    """

    _write_doc(atlas, "role: guionista", body)
    _write_doc(rival, "role: tecnico", body)

    config = SearchPipelineConfig(role_bias=1.0)
    index = DocumentationIndex(docs, pipeline_config=config)

    biased = index.search("eldertown", limit=1, role="guionista")
    assert biased
    biased_top = biased[0].section.document_path.name

    assert biased_top == atlas.name, "El sesgo por rol debería priorizar la sección correcta"


def test_pipeline_respects_limit(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    content = """
# A
Atlas diseño cooperativo.
# B
Atlas integración técnica.
# C
Atlas documentación narrativa.
    """
    (docs / "atlas.md").write_text(content, encoding="utf-8")

    index = DocumentationIndex(docs)
    results = index.search("atlas", limit=2)
    assert len(results) == 2
