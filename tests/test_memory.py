import json

from dungeon_life_agent.memory import CollectiveMemory


def test_collective_memory_capture_and_search(tmp_path):
    storage = tmp_path / "memoria.json"
    memory = CollectiveMemory(storage)
    memory.capture(channel="general", author="alice", summary="Resumen", content="Se definió pipeline Blender", tags=["pipeline"], decisions=["medio:documentar"])
    memory.capture(channel="general", author="bob", summary="Otro", content="Reunión de roadmap", tags=["roadmap"], decisions=[])

    results = memory.search("pipeline")
    assert results
    assert results[0].channel == "general"

    channels = memory.channels()
    assert channels == ["general"]

    # Verifica persistencia
    with storage.open("r", encoding="utf-8") as stream:
        raw = json.load(stream)
    assert len(raw) == 2
