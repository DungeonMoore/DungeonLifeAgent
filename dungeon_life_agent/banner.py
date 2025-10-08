"""Banner interactivo para la CLI de Willow.

El módulo encapsula la representación en ASCII/Unicode de la cara de
Willow junto con utilidades para detectar soporte de color y centrar el
banner dentro del ancho de la terminal. El objetivo es que el banner sea
fácilmente reemplazable por futuras variantes (feliz, triste, etc.).
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from dataclasses import dataclass
from typing import Dict, List, Sequence

ANSI_RE = re.compile(r"\x1b\[[0-9;:]*m")


def _visible_length(value: str) -> int:
    """Length of the string ignoring ANSI escape sequences."""

    return len(ANSI_RE.sub("", value))


def supports_color(stream: object | None = None) -> bool:
    """Return True if the provided stream seems to support ANSI colors."""

    stream = stream or sys.stdout
    if not hasattr(stream, "isatty") or not stream.isatty():  # type: ignore[attr-defined]
        return False
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    term = os.environ.get("TERM", "")
    if term.lower() == "dumb":
        return False
    return True


@dataclass(frozen=True)
class BannerVariant:
    """Describes a banner illustration with color and monochrome variants."""

    name: str
    color_lines: Sequence[str]
    monochrome_lines: Sequence[str]

    def render(self, *, width: int | None = None, use_color: bool = True) -> str:
        """Return the banner formatted within a Unicode panel."""

        lines = self.color_lines if use_color else self.monochrome_lines
        content_width = max(_visible_length(line) for line in lines)

        def pad_line(raw: str) -> str:
            visible = _visible_length(raw)
            total_padding = content_width - visible
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            return f"│ {' ' * left_padding}{raw}{' ' * right_padding} │"

        top = f"╭{'─' * (content_width + 2)}╮"
        bottom = f"╰{'─' * (content_width + 2)}╯"

        panel_lines: List[str] = [top] + [pad_line(line) for line in lines] + [bottom]

        terminal_width = width or shutil.get_terminal_size((80, 20)).columns
        centered = [line.center(terminal_width) for line in panel_lines]
        return "\n".join(centered)


def _build_classic_variant() -> BannerVariant:
    beard = "\x1b[38;2;245;245;245m"
    skin = "\x1b[38;2;255;220;180m"
    shading = "\x1b[38;2;230;190;140m"
    eye_white = "\x1b[38;2;255;255;255m"
    pupil = "\x1b[38;2;40;40;40m"
    mouth = "\x1b[38;2;210;120;100m"
    reset = "\x1b[0m"

    color_lines = [
        f"{beard}      ⠀⣀⣤⣤⣤⣀⠀⠀      {reset}",
        f"{beard}   ⣤⠞⠋⠉⠉⠉⠉⠙⠳⣄   {reset}",
        f"{beard} ⣴⠋ {skin} ⠀⣀⣀⣀⣀⠀ {beard} ⠙⣦ {reset}",
        f"{beard}⣼⡇ {skin} ⣰{eye_white}◕{pupil}◉{eye_white}◕{skin}⣆ {beard} ⢸⣧{reset}",
        f"{beard}⣿⡇ {skin}⢸⣿⣿⣿⣿⣿⡇{beard} ⢸⣿{reset}",
        f"{beard}⣿⡇ {skin}⢸⣿{mouth}⠉⠉{skin}⣿⡇{beard} ⢸⣿{reset}",
        f"{beard}⣿⡇ {skin} ⠘⠿⠿⠿⠟⠀ {beard} ⢸⣿{reset}",
        f"{beard}⠹⣧⡀⠀⠀{shading}⣀⣀{beard}⠀⠀⢀⣼⠏{reset}",
        f"{beard}  ⠙⠻⢶⣶⣶⣶⡶⠟⠋  {reset}",
    ]

    monochrome_lines = [
        "      ⠀⣀⣤⣤⣤⣀⠀⠀      ",
        "   ⣤⠞⠋⠉⠉⠉⠉⠙⠳⣄   ",
        " ⣴⠋   ⠀⣀⣀⣀⣀⠀   ⠙⣦ ",
        "⣼⡇  ⣰◕◉◕⣆  ⢸⣧",
        "⣿⡇  ⢸⣿⣿⣿⣿⣿⡇ ⢸⣿",
        "⣿⡇  ⢸⣿⠉⠉⣿⡇ ⢸⣿",
        "⣿⡇   ⠘⠿⠿⠿⠟   ⢸⣿",
        "⠹⣧⡀   ⣀⣀   ⢀⣼⠏",
        "  ⠙⠻⢶⣶⣶⣶⡶⠟⠋  ",
    ]

    return BannerVariant(name="classic", color_lines=color_lines, monochrome_lines=monochrome_lines)


VARIANTS: Dict[str, BannerVariant] = {"classic": _build_classic_variant()}


def get_banner(name: str = "classic") -> BannerVariant:
    """Retrieve a banner variant by name."""

    try:
        return VARIANTS[name]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise ValueError(f"Banner '{name}' no disponible") from exc


def render_banner(*, stream: object | None = None, name: str = "classic") -> str:
    """Renderiza el banner adaptado al ancho de la terminal."""

    banner = get_banner(name)
    color = supports_color(stream)
    width = shutil.get_terminal_size((80, 20)).columns
    return banner.render(width=width, use_color=color)


def print_welcome(stream: object | None = None) -> None:
    """Imprime el banner y la leyenda de bienvenida."""

    stream = stream or sys.stdout
    banner_text = render_banner(stream=stream)
    print(banner_text, file=stream)

    width = shutil.get_terminal_size((80, 20)).columns
    subtitle = "Willow CLI v0.1".center(width)
    instructions = "Escribe willow help para ver los comandos disponibles.".center(width)
    print(subtitle, file=stream)
    print(instructions, file=stream)
    print("", file=stream)
