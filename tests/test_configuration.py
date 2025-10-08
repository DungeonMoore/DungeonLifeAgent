import pytest

from dungeon_life_agent.config import load_config, ConfigurationError


def test_default_configuration_contains_modes_and_roles():
    config = load_config()
    assert "consultor" in config.modes
    assert "guionista" in config.roles


def test_missing_config_file_raises(tmp_path):
    missing = tmp_path / "missing.yaml"
    try:
        load_config(missing)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Se esperaba FileNotFoundError al cargar configuración inexistente")


def test_yaml_config_is_rejected(tmp_path):
    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text("modes: {}\n", encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_config(yaml_file)
