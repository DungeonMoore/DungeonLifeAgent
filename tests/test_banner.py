from dungeon_life_agent import banner


def test_render_banner_without_color_uses_monochrome():
    class DummyStream:
        def isatty(self) -> bool:
            return False

    output = banner.render_banner(stream=DummyStream())

    # No secuencias ANSI presentes cuando el flujo no soporta color
    assert "\x1b" not in output


def test_get_banner_returns_variant():
    variant = banner.get_banner("classic")
    rendered = variant.render(width=60, use_color=False)
    assert "Willow" not in rendered  # Solo valida que devuelve contenido del rostro
    assert "╭" in rendered
