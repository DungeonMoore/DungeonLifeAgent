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


def test_suggest_returns_titles_by_prefix():
    index = DocumentationIndex("Documentacion")
    suggestions = index.suggest("tax")
    assert suggestions, "Se esperaban sugerencias para prefijos conocidos"
    assert any("tax" in suggestion.lower() for suggestion in suggestions)


def test_refresh_updates_modified_documents(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    source = docs / "guia.md"
    source.write_text("# Guia\nContenido inicial sobre agentes.", encoding="utf-8")

    index = DocumentationIndex(docs)
    assert index.search("inicial"), "El contenido original debería indexarse"

    source.write_text("# Guia\nContenido actualizado con dragones.", encoding="utf-8")
    index.refresh(paths=[source])
    results = index.search("dragones")
    assert results, "La búsqueda debería reflejar el nuevo contenido"
