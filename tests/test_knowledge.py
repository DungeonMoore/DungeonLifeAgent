from dungeon_life_agent.knowledge import DocumentationIndex


def test_search_returns_results():
    index = DocumentationIndex("Documentacion")
    results = index.search("arquitectura tecnica", limit=5)
    assert results, "Se esperaba al menos un resultado"
    assert all(result.section.document_path.suffix == ".md" for result in results)


def test_list_documents_returns_all_markdown_files():
    index = DocumentationIndex("Documentacion")
    docs = index.list_documents()
    assert any(doc.endswith("00_README_Principal.md") for doc in map(str, docs))
