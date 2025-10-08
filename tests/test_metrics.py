from dungeon_life_agent.metrics import MetricsRegistry


def test_metrics_registry_tracks_extended_events(tmp_path):
    metrics = MetricsRegistry()
    metrics.record_search("consultor", latency=0.5, results=3)
    metrics.record_productivity(role="productor", tasks_completed=4, minutes=60)
    metrics.record_decision(identifier="abc", mode="colaborador", description="alto:activar dashboard")

    report = metrics.format_report()
    assert "Consultas" in report
    assert "Productividad" in report
    assert "Decisiones" in report

    output = tmp_path / "metrics.csv"
    exported = metrics.export_csv(output)
    assert exported.exists()
    content = exported.read_text(encoding="utf-8")
    assert "search.count" in content
