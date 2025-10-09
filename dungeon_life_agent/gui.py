"""Interfaz gráfica minimalista para conversar con Willow mediante CustomTkinter."""

from __future__ import annotations

import os
import sys

try:  # pragma: no cover - import opcional para entornos headless
    import customtkinter as ctk
except ModuleNotFoundError:  # pragma: no cover - degradado controlado
    ctk = None  # type: ignore[assignment]

from .agent import DungeonLifeAgent
from .interactive import HELP_TEXT, process_interactive_message


DEFAULT_GREETING = "Me alegro de verte, guardián. ¿Listo para explorar el bosque digital?"


if ctk is not None:

    class AgentChatApp(ctk.CTk):
        """Ventana principal del chat con Willow."""

        def __init__(
            self,
            agent: DungeonLifeAgent | None = None,
            *,
            greeting: str | None = None,
        ) -> None:
            super().__init__()

            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")

            self.title("Willow · Dungeon Life Agent")
            self.geometry("900x600")
            self.minsize(720, 480)

            self.agent = agent or DungeonLifeAgent()
            self.greeting = greeting or DEFAULT_GREETING

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            self._build_header()
            self._build_chat_area()
            self._build_input_area()

            self._append_message("Willow", self.greeting)

            self.entry.focus_set()

            self.bind("<Return>", self._on_return)
            self.protocol("WM_DELETE_WINDOW", self._on_close)

        def _build_header(self) -> None:
            header = ctk.CTkFrame(self, fg_color="transparent")
            header.grid(row=0, column=0, pady=(24, 12), sticky="ew")
            header.columnconfigure(0, weight=1)

            title = ctk.CTkLabel(
                header,
                text="Willow",
                font=("Segoe UI", 28, "bold"),
                anchor="w",
            )
            title.grid(row=0, column=0, sticky="w", padx=24)

            subtitle = ctk.CTkLabel(
                header,
                text="Tu guardián digital de Dungeon Life",
                font=("Segoe UI", 14),
                text_color=("#a0a0a0", "#d0d0d0"),
                anchor="w",
            )
            subtitle.grid(row=1, column=0, sticky="w", padx=24, pady=(4, 0))

        def _build_chat_area(self) -> None:
            self.chat_display = ctk.CTkTextbox(
                self,
                wrap="word",
                font=("Segoe UI", 14),
            )
            self.chat_display.grid(row=1, column=0, padx=24, sticky="nsew")
            self.chat_display.configure(state="disabled")

        def _build_input_area(self) -> None:
            container = ctk.CTkFrame(self, corner_radius=18, fg_color="#111")
            container.grid(row=2, column=0, padx=24, pady=24, sticky="ew")
            container.columnconfigure(0, weight=1)

            self.entry = ctk.CTkEntry(
                container,
                placeholder_text="Pregunta lo que quieras",
                font=("Segoe UI", 14),
            )
            self.entry.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="ew")

            send_button = ctk.CTkButton(
                container,
                text="Enviar",
                command=self._on_send,
                width=120,
            )
            send_button.grid(row=0, column=1, padx=(8, 16), pady=16)

            help_button = ctk.CTkButton(
                container,
                text="?",
                width=48,
                command=self._show_help,
            )
            help_button.grid(row=0, column=2, padx=(0, 16), pady=16)

        def _append_message(self, author: str, text: str) -> None:
            if not text:
                return
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"{author}: {text.strip()}\n\n")
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

        def _on_return(self, event) -> None:  # type: ignore[override]
            if event.state & 0x0001:  # Shift presionado para salto de línea
                return
            self._on_send()

        def _on_send(self) -> None:
            message = self.entry.get().strip()
            if not message:
                return

            self.entry.delete(0, "end")
            self._append_message("Tú", message)

            should_continue, response = process_interactive_message(
                self.agent, message, show_debug=False
            )
            if response:
                self._append_message("Willow", response)

            if not should_continue:
                self.after(200, self.destroy)

        def _show_help(self) -> None:
            self._append_message("Willow", HELP_TEXT)

        def _on_close(self) -> None:
            self.destroy()

else:

    class AgentChatApp:  # pragma: no cover - stub minimal para entornos sin CustomTkinter
        """Stub que informa la ausencia de CustomTkinter."""

        def __init__(self, *_, **__) -> None:
            raise RuntimeError(
                "CustomTkinter no está instalado. Instala la dependencia para abrir la ventana."
            )


def launch_app() -> None:
    """Crea el agente y lanza la aplicación gráfica."""

    if ctk is None:
        raise RuntimeError(
            "CustomTkinter no está disponible en este entorno. Ejecuta 'pip install customtkinter'."
        )
    app = AgentChatApp()
    app.mainloop()


def supports_windowing() -> bool:
    """Indica si parece existir un entorno gráfico disponible."""

    if ctk is None:
        return False
    if sys.platform.startswith("win"):
        return True
    if sys.platform == "darwin":
        return True
    display = os.environ.get("DISPLAY")
    wayland = os.environ.get("WAYLAND_DISPLAY")
    session = os.environ.get("XDG_SESSION_TYPE")
    return bool(display or wayland or session == "wayland")


def run_headless_query(message: str, *, show_debug: bool = False) -> str:
    """Procesa un mensaje reutilizando la lógica de la ventana sin abrirla."""

    agent = DungeonLifeAgent()
    _, response = process_interactive_message(agent, message, show_debug=show_debug)
    return response


__all__ = ["AgentChatApp", "launch_app", "run_headless_query", "supports_windowing"]

