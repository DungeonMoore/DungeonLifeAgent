"""Interfaz gráfica minimalista para conversar con Willow mediante CustomTkinter."""

from __future__ import annotations

import os
import sys
import re
import json
import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:  # pragma: no cover - import opcional para entornos headless
    import customtkinter as ctk
except ModuleNotFoundError:  # pragma: no cover - degradado controlado
    ctk = None  # type: ignore[assignment]

try:  # pragma: no cover - import opcional para syntax highlighting
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
    from pygments.formatters import TerminalFormatter
    from pygments.util import ClassNotFound
    PYGMENTS_AVAILABLE = True
except ModuleNotFoundError:  # pragma: no cover - degradado controlado
    PYGMENTS_AVAILABLE = False

from .agent import DungeonLifeAgent
from .llm import OllamaClient, OllamaServiceStatus, probe_ollama_service
from .interactive import HELP_TEXT, process_interactive_message


DEFAULT_GREETING = "Me alegro de verte, guardián. ¿Listo para explorar el bosque digital?"


class ConversationHistory:
    """Gestión de historial de conversaciones."""

    def __init__(self, history_file: str = "conversation_history.json"):
        self.history_file = Path(history_file)
        self.messages: List[Dict[str, Any]] = []
        self._load_history()

    def _load_history(self) -> None:
        """Cargar historial desde archivo."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.messages = data.get('messages', [])
            except (json.JSONDecodeError, IOError):
                self.messages = []

    def _save_history(self) -> None:
        """Guardar historial a archivo."""
        try:
            self.history_file.parent.mkdir(exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'messages': self.messages,
                    'last_updated': datetime.datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
        except IOError:
            pass  # Silenciar errores de escritura

    def add_message(self, author: str, content: str) -> None:
        """Agregar un mensaje al historial."""
        message = {
            'timestamp': datetime.datetime.now().isoformat(),
            'author': author,
            'content': content
        }
        self.messages.append(message)
        self._save_history()

    def get_messages(self) -> List[Dict[str, Any]]:
        """Obtener todos los mensajes."""
        return self.messages.copy()

    def clear_history(self) -> None:
        """Limpiar historial."""
        self.messages.clear()
        self._save_history()

    def export_markdown(self, filename: str) -> bool:
        """Exportar conversación como Markdown."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# Conversación con Willow\n\n")
                for msg in self.messages:
                    timestamp = datetime.datetime.fromisoformat(msg['timestamp']).strftime('%Y-%m-%d %H:%M')
                    f.write(f"## {msg['author']} ({timestamp})\n\n{msg['content']}\n\n")
            return True
        except IOError:
            return False


class MessageFormatter:
    """Formateador de mensajes con soporte para código y markdown."""

    CODE_BLOCK_PATTERN = re.compile(r'```(\w+)?\n?(.*?)\n?```', re.DOTALL)
    INLINE_CODE_PATTERN = re.compile(r'`([^`]+)`')

    @staticmethod
    def format_message(content: str) -> str:
        """Formatear mensaje con soporte básico para markdown."""
        if not content:
            return ""

        # Procesar bloques de código primero
        content = MessageFormatter._process_code_blocks(content)

        # Procesar código inline
        content = MessageFormatter._process_inline_code(content)

        return content

    @staticmethod
    def _process_code_blocks(content: str) -> str:
        """Procesar bloques de código con syntax highlighting."""
        def replace_code_block(match):
            language = match.group(1) or 'text'
            code = match.group(2).strip()

            if PYGMENTS_AVAILABLE:
                try:
                    lexer = get_lexer_by_name(language)
                    formatter = TerminalFormatter()
                    highlighted = highlight(code, lexer, formatter)
                    return f"\n```\n{highlighted.rstrip()}\n```\n"
                except ClassNotFound:
                    pass

            # Fallback sin highlighting
            return f"\n```\n{code}\n```\n"

        return MessageFormatter.CODE_BLOCK_PATTERN.sub(replace_code_block, content)

    @staticmethod
    def _process_inline_code(content: str) -> str:
        """Procesar código inline."""
        def replace_inline_code(match):
            code = match.group(1)
            if PYGMENTS_AVAILABLE:
                try:
                    lexer = guess_lexer(code)
                    formatter = TerminalFormatter()
                    highlighted = highlight(code, lexer, formatter).strip()
                    return highlighted
                except:
                    pass
            return code

        return MessageFormatter.INLINE_CODE_PATTERN.sub(replace_inline_code, content)


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
            ctk.set_default_color_theme("blue")

            self.title("Willow · Dungeon Life Agent")
            self.geometry("1000x700")
            self.minsize(800, 600)

            self.agent = agent or DungeonLifeAgent()
            self.greeting = greeting or DEFAULT_GREETING
            self.conversation_history = ConversationHistory()
            self.is_processing = False
            self.ollama_status_icon = None
            self.ollama_status_label = None
            self._ollama_status_job_id: str | None = None
            self._ollama_last_available: bool | None = None

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            self._build_header()
            self._build_chat_area()
            self._build_input_area()
            self._update_ollama_status()

            # Configurar estilos de mensajes
            self._configure_message_tags()

            # Cargar historial de conversación si existe
            self._load_conversation_history()

            # Mostrar saludo solo si no hay historial previo
            if not self._has_recent_history():
                self._append_message("Willow", self.greeting)

            self.entry.focus_set()

            self.bind("<Return>", self._on_return)
            self.bind("<Control-c>", self._copy_selected)
            self.bind("<Control-v>", self._paste_to_entry)
            self.protocol("WM_DELETE_WINDOW", self._on_close)

        def _build_header(self) -> None:
            header = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=0)
            header.grid(row=0, column=0, pady=(0, 12), sticky="ew")
            header.grid_columnconfigure(0, weight=0)
            header.grid_columnconfigure(1, weight=1)
            header.grid_columnconfigure(2, weight=0)

            # Logo/Avatar area
            avatar_frame = ctk.CTkFrame(header, fg_color="transparent")
            avatar_frame.grid(row=0, column=0, sticky="w", padx=24)

            # Avatar circle
            avatar = ctk.CTkFrame(
                avatar_frame,
                width=50,
                height=50,
                corner_radius=25,
                fg_color="#4a90e2",
                bg_color="transparent"
            )
            avatar.pack(side="left", padx=(0, 12))

            avatar_label = ctk.CTkLabel(
                avatar,
                text="W",
                font=("Segoe UI", 24, "bold"),
                text_color="white",
                fg_color="transparent"
            )
            avatar_label.place(relx=0.5, rely=0.5, anchor="center")

            # Title and subtitle
            title_frame = ctk.CTkFrame(header, fg_color="transparent")
            title_frame.grid(row=0, column=1, sticky="w")

            title = ctk.CTkLabel(
                title_frame,
                text="Willow",
                font=("Segoe UI", 24, "bold"),
                text_color="white",
                fg_color="transparent",
                anchor="w",
            )
            title.pack(anchor="w")

            subtitle = ctk.CTkLabel(
                title_frame,
                text="Tu asistente IA especializado en Dungeon Life",
                font=("Segoe UI", 12),
                text_color=("#b0b0b0", "#d0d0d0"),
                fg_color="transparent",
                anchor="w",
            )
            subtitle.pack(anchor="w", pady=(2, 0))

            status_frame = ctk.CTkFrame(header, fg_color="transparent")
            status_frame.grid(row=0, column=2, sticky="e", padx=(0, 24))

            self.ollama_status_icon = ctk.CTkFrame(
                status_frame,
                width=16,
                height=16,
                corner_radius=8,
                fg_color="#666666",
                border_width=0,
            )
            self.ollama_status_icon.pack(side="left", padx=(0, 8), pady=4)

            self.ollama_status_label = ctk.CTkLabel(
                status_frame,
                text="Ollama sin detectar",
                font=("Segoe UI", 12),
                text_color="#999999",
                fg_color="transparent",
                anchor="e",
            )
            self.ollama_status_label.pack(side="left")

        def _build_chat_area(self) -> None:
            self.chat_display = ctk.CTkTextbox(
                self,
                wrap="word",
                font=("Consolas", 12),  # Fuente monoespaciada para mejor formato de código
                fg_color="#1a1a1a",
                text_color="white",
            )
            self.chat_display.grid(row=1, column=0, padx=24, pady=(0, 12), sticky="nsew")
            self.chat_display.configure(state="disabled")

            # Crear menú contextual para copiar
            self._create_context_menu()

        def _create_context_menu(self) -> None:
            """Crear menú contextual para el área de chat."""
            self.context_menu = ctk.CTkFrame(self, fg_color="#2a2a2a")

            copy_button = ctk.CTkButton(
                self.context_menu,
                text="Copiar",
                command=self._copy_selected_text,
                fg_color="#4a90e2",
                hover_color="#357abd",
                font=("Segoe UI", 11)
            )
            copy_button.pack(padx=2, pady=2)

            # Ocultar menú inicialmente
            self.context_menu.place_forget()

            # Bind para mostrar menú contextual con clic derecho
            self.chat_display.bind("<Button-3>", self._show_context_menu)

        def _show_context_menu(self, event) -> None:
            """Mostrar menú contextual en posición del cursor."""
            try:
                # Seleccionar texto en posición del cursor
                self.chat_display.focus_set()
                self.chat_display.mark_set("insert", f"@{event.x},{event.y}")

                # Mostrar menú cerca del cursor
                self.context_menu.place(x=event.x_root - self.winfo_rootx() + 10,
                                      y=event.y_root - self.winfo_rooty() + 10)
            except:
                pass

        def _copy_selected_text(self) -> None:
            """Copiar texto seleccionado desde menú contextual."""
            try:
                selected_text = self.chat_display.get("sel.first", "sel.last")
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                self.context_menu.place_forget()
            except:
                self.context_menu.place_forget()

        def _clear_history(self) -> None:
            """Limpiar historial de conversación."""
            try:
                # Confirmar limpieza
                confirm = ctk.CTkToplevel(self)
                confirm.title("Confirmar limpieza")
                confirm.geometry("400x150")
                confirm.resizable(False, False)

                # Centrar ventana
                confirm.transient(self)
                confirm.grab_set()

                # Hacer modal
                x = self.winfo_x() + (self.winfo_width() // 2) - (400 // 2)
                y = self.winfo_y() + (self.winfo_height() // 2) - (150 // 2)
                confirm.geometry(f"+{x}+{y}")

                # Contenido
                msg_label = ctk.CTkLabel(
                    confirm,
                    text="¿Estás seguro de que quieres limpiar\ntodo el historial de conversación?",
                    font=("Segoe UI", 12),
                    justify="center"
                )
                msg_label.pack(pady=(20, 15))

                button_frame = ctk.CTkFrame(confirm, fg_color="transparent")
                button_frame.pack(pady=(0, 20))

                def do_clear():
                    """Ejecutar limpieza del historial."""
                    try:
                        # Limpiar historial
                        self.conversation_history.clear_history()

                        # Limpiar área de chat visualmente
                        self.chat_display.configure(state="normal")
                        self.chat_display.delete("1.0", "end")

                        # Mostrar saludo inicial
                        self._append_message("Willow", self.greeting)

                        # Actualizar estado
                        self.status_label.configure(text="Historial limpiado", text_color="#28a745")
                        self.after(2000, lambda: self.status_label.configure(text="Listo", text_color="#888"))

                    except Exception as e:
                        self.status_label.configure(text=f"Error al limpiar: {str(e)}", text_color="#dc3545")
                        self.after(3000, lambda: self.status_label.configure(text="Listo", text_color="#888"))

                    confirm.destroy()

                def cancel_clear():
                    """Cancelar limpieza."""
                    confirm.destroy()

                # Botones
                clear_btn = ctk.CTkButton(
                    button_frame,
                    text="Limpiar",
                    command=do_clear,
                    fg_color="#dc3545",
                    hover_color="#c82333",
                    width=80
                )
                clear_btn.pack(side="left", padx=(0, 10))

                cancel_btn = ctk.CTkButton(
                    button_frame,
                    text="Cancelar",
                    command=cancel_clear,
                    fg_color="#6c757d",
                    hover_color="#5a6268",
                    width=80
                )
                cancel_btn.pack(side="left")

                # Enfocar botón cancelar
                cancel_btn.focus_set()

            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}", text_color="#dc3545")

        def _build_input_area(self) -> None:
            # Crear barra de estado
            self.status_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", height=30)
            self.status_frame.grid(row=3, column=0, padx=24, pady=(0, 12), sticky="ew")
            self.status_frame.columnconfigure(1, weight=1)

            self.status_label = ctk.CTkLabel(
                self.status_frame,
                text="Listo",
                font=("Segoe UI", 10),
                text_color="#888",
                fg_color="transparent",
                anchor="w"
            )
            self.status_label.grid(row=0, column=0, padx=(16, 0), pady=8, sticky="w")

            # Área de entrada principal
            container = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a1a")
            container.grid(row=2, column=0, padx=24, pady=(0, 24), sticky="ew")
            container.columnconfigure(0, weight=1)

            self.entry = ctk.CTkEntry(
                container,
                placeholder_text="Escribe tu mensaje aquí... (Ctrl+V para pegar)",
                placeholder_text_color="#888",
                font=("Segoe UI", 13),
                fg_color="#2a2a2a",
                border_color="#4a90e2",
                border_width=2,
                corner_radius=8,
                height=45,
            )
            self.entry.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="ew")

            button_frame = ctk.CTkFrame(container, fg_color="transparent")
            button_frame.grid(row=0, column=1, padx=(8, 16), pady=16)

            send_button = ctk.CTkButton(
                button_frame,
                text="Enviar",
                command=self._on_send,
                width=100,
                height=45,
                corner_radius=8,
                font=("Segoe UI", 12, "bold"),
                fg_color="#4a90e2",
                hover_color="#357abd",
                state="normal"
            )
            send_button.pack(side="left")

            help_button = ctk.CTkButton(
                button_frame,
                text="?",
                width=45,
                height=45,
                corner_radius=8,
                command=self._show_help,
                font=("Segoe UI", 14, "bold"),
                fg_color="#333",
                hover_color="#555",
                text_color="#4a90e2",
            )
            help_button.pack(side="left", padx=(8, 0))

            clear_button = ctk.CTkButton(
                button_frame,
                text="🗑️",
                width=45,
                height=45,
                corner_radius=8,
                command=self._clear_history,
                font=("Segoe UI", 14, "bold"),
                fg_color="#dc3545",
                hover_color="#c82333",
                text_color="white"
            )
            clear_button.pack(side="left", padx=(8, 0))

            # Referencias para actualizar estado
            self.send_button = send_button

        def _resolve_ollama_configuration(self) -> Tuple[str, str | None]:
            """Determina host y modelo configurados para Ollama."""
            host = os.getenv("WILLOW_LLM_HOST", "http://localhost:11434")
            model = os.getenv("WILLOW_LLM_MODEL")
            language_model = getattr(self.agent, "language_model", None)
            if isinstance(language_model, OllamaClient):
                host = language_model.host or host
                model = language_model.model or model
            return host, model

        def _update_ollama_status(self) -> None:
            """Consulta el servicio de Ollama y actualiza la cabecera."""
            if self.ollama_status_icon is None or self.ollama_status_label is None:
                return

            host, configured_model = self._resolve_ollama_configuration()
            status: OllamaServiceStatus
            try:
                status = probe_ollama_service(host=host, configured_model=configured_model)
            except Exception as exc:  # pragma: no cover - defensa extra
                status = OllamaServiceStatus(False, host, configured_model, str(exc))

            self._apply_ollama_status(status)
            self._ollama_status_job_id = self.after(10000, self._update_ollama_status)

        def _apply_ollama_status(self, status: OllamaServiceStatus) -> None:
            """Aplica estilos y mensajes seg�n el estado del servicio."""
            if self.ollama_status_icon is None or self.ollama_status_label is None:
                return

            if status.available:
                icon_color = "#4ade80"
                text_color = "#d1fae5"
                model_name = status.model or "sin modelo"
                label_text = f"Ollama activo - {model_name}"
            else:
                icon_color = "#f87171"
                text_color = "#fca5a5"
                label_text = "Ollama inactivo"

            self.ollama_status_icon.configure(fg_color=icon_color)
            self.ollama_status_label.configure(text=label_text, text_color=text_color)

            previous = self._ollama_last_available
            self._ollama_last_available = status.available

            if status.available:
                if previous is False and hasattr(self, "status_label"):
                    self.status_label.configure(text="Ollama disponible", text_color="#4ade80")
                    self.after(3000, lambda: self.status_label.configure(text="Listo", text_color="#888"))
            else:
                if previous is not False and hasattr(self, "status_label"):
                    detail = status.detail or "No se pudo conectar al servicio."
                    self.status_label.configure(
                        text=f"Ollama inactivo: {detail}",
                        text_color="#f87171",
                    )
                    self.after(5000, lambda: self.status_label.configure(text="Listo", text_color="#888"))

        def _append_message(self, author: str, text: str) -> None:
            if not text:
                return
            self.chat_display.configure(state="normal")

            # Insertar timestamp sutil
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M")

            if author == "Tú":
                # Mensaje del usuario - formateado simplemente
                self.chat_display.insert("end", f"Usuario ({timestamp}): {text.strip()}\n")
            else:
                # Mensaje de Willow - formateado simplemente
                self.chat_display.insert("end", f"Willow ({timestamp}): {text.strip()}\n")

            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

        def _configure_message_tags(self) -> None:
            """Configurar estilos para diferentes tipos de mensajes."""
            # CustomTkinter no soporta tag configuration como tkinter estándar
            # Los estilos se aplican directamente en el texto
            pass

        def _on_return(self, event) -> None:  # type: ignore[override]
            if event.state & 0x0001:  # Shift presionado para salto de línea
                return
            self._on_send()

        def _on_send(self) -> None:
            message = self.entry.get().strip()
            if not message or self.is_processing:
                return

            self.entry.delete(0, "end")
            self._append_message("Tú", message)

            # Mostrar indicador de escritura
            self._show_typing_indicator()

            # Procesar mensaje en segundo plano para mantener responsividad
            self.after(100, lambda: self._process_message_async(message))

        def _process_message_async(self, message: str) -> None:
            """Procesar mensaje de forma asíncrona."""
            try:
                should_continue, response = process_interactive_message(
                    self.agent, message, show_debug=False
                )

                # Ocultar indicador de escritura
                self._hide_typing_indicator()

                if response:
                    self._append_message("Willow", response)

                if not should_continue:
                    self.after(200, self.destroy)

            except Exception as e:
                # Ocultar indicador de escritura en caso de error
                self._hide_typing_indicator()

                # Mostrar mensaje de error
                error_msg = f"Error al procesar mensaje: {str(e)}"
                self._append_message("Willow", error_msg)

        def _show_help(self) -> None:
            # Crear ventana popup con información del agente
            info_window = ctk.CTkToplevel(self)
            info_window.title("Información de Willow")
            info_window.geometry("800x600")
            info_window.resizable(True, True)

            # Hacer que la ventana sea modal
            info_window.transient(self)
            info_window.grab_set()

            # Crear área de texto con scrollbar para mostrar la información
            text_frame = ctk.CTkFrame(info_window)
            text_frame.pack(fill="both", expand=True, padx=10, pady=10)

            text_widget = ctk.CTkTextbox(
                text_frame,
                wrap="word",
                font=("Consolas", 11),  # Fuente monoespaciada para mantener formato
            )
            text_widget.pack(side="left", fill="both", expand=True)

            scrollbar = ctk.CTkScrollbar(text_frame, command=text_widget.yview)
            scrollbar.pack(side="right", fill="y")
            text_widget.configure(yscrollcommand=scrollbar.set)

            # Obtener información formateada del agente
            agent_info = self.agent.get_agent_info_display()

            # Insertar la información en el widget de texto
            text_widget.insert("1.0", agent_info)
            text_widget.configure(state="disabled")

            # Botón para cerrar
            close_button = ctk.CTkButton(
                info_window,
                text="Cerrar",
                command=info_window.destroy,
                width=100
            )
            close_button.pack(pady=(0, 10))

            # Centrar la ventana
            info_window.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() // 2) - (info_window.winfo_width() // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (info_window.winfo_height() // 2)
            info_window.geometry(f"+{x}+{y}")

            # Enfocar el botón de cerrar
            close_button.focus_set()

        def _load_conversation_history(self) -> None:
            """Cargar historial de conversación reciente."""
            messages = self.conversation_history.get_messages()
            if messages:
                # Mostrar solo los últimos 10 mensajes para no sobrecargar
                recent_messages = messages[-10:] if len(messages) > 10 else messages

                for msg in recent_messages:
                    formatted_content = MessageFormatter.format_message(msg['content'])
                    self._append_message_raw(msg['author'], formatted_content, msg['timestamp'])

        def _has_recent_history(self) -> bool:
            """Verificar si hay historial reciente (últimas 24 horas)."""
            messages = self.conversation_history.get_messages()
            if not messages:
                return False

            last_message = messages[-1]
            try:
                msg_time = datetime.datetime.fromisoformat(last_message['timestamp'])
                time_diff = datetime.datetime.now() - msg_time
                return time_diff.total_seconds() < 24 * 60 * 60  # 24 horas
            except (ValueError, KeyError):
                return False

        def _append_message_raw(self, author: str, text: str, timestamp: str = None) -> None:
            """Agregar mensaje formateado al área de chat."""
            if not text:
                return

            self.chat_display.configure(state="normal")

            # Insertar timestamp sutil
            if timestamp:
                try:
                    dt = datetime.datetime.fromisoformat(timestamp)
                    display_time = dt.strftime("%H:%M")
                except ValueError:
                    display_time = datetime.datetime.now().strftime("%H:%M")
            else:
                display_time = datetime.datetime.now().strftime("%H:%M")

            # Formatear el mensaje
            formatted_text = MessageFormatter.format_message(text)

            if author == "Tú":
                # Mensaje del usuario - formateado simplemente
                self.chat_display.insert("end", f"Usuario ({display_time}): {formatted_text.strip()}\n")
            else:
                # Mensaje de Willow - formateado simplemente
                self.chat_display.insert("end", f"Willow ({display_time}): {formatted_text.strip()}\n")

            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

        def _append_message(self, author: str, text: str) -> None:
            """Agregar mensaje y guardarlo en el historial."""
            self._append_message_raw(author, text)
            self.conversation_history.add_message(author, text)

        def _show_typing_indicator(self) -> None:
            """Mostrar indicador de que Willow está escribiendo."""
            if self.is_processing:
                return

            self.is_processing = True
            self.send_button.configure(state="disabled", text="Procesando...")
            self.status_label.configure(text="Procesando mensaje...", text_color="#ffa500")
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", "Willow está escribiendo...")
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

        def _hide_typing_indicator(self) -> None:
            """Ocultar indicador de escritura."""
            if not self.is_processing:
                return

            self.is_processing = False
            self.send_button.configure(state="normal", text="Enviar")
            self.status_label.configure(text="Listo", text_color="#888")
            self.chat_display.configure(state="normal")
            # Encontrar y eliminar la línea del indicador de escritura
            content = self.chat_display.get("1.0", "end-1c")
            lines = content.split("\n")

            # Buscar la línea del indicador y eliminarla
            for i, line in enumerate(lines):
                if "Willow está escribiendo" in line:
                    # Eliminar la línea
                    start_idx = f"{i+1}.0"
                    end_idx = f"{i+2}.0"
                    self.chat_display.delete(start_idx, end_idx)
                    break

            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

        def _show_context_menu(self, event) -> None:
            """Mostrar menú contextual en posición del cursor."""
            # Ocultar menú si ya está visible
            self.context_menu.place_forget()

            try:
                # Seleccionar texto en posición del cursor
                self.chat_display.focus_set()
                self.chat_display.mark_set("insert", f"@{event.x},{event.y}")

                # Mostrar menú cerca del cursor
                self.context_menu.place(x=event.x_root - self.winfo_rootx() + 10,
                                      y=event.y_root - self.winfo_rooty() + 10)

                # Bind para ocultar menú al hacer clic fuera
                self.chat_display.bind("<Button-1>", self._hide_context_menu, add="+")
            except:
                pass

        def _hide_context_menu(self, event=None) -> None:
            """Ocultar menú contextual."""
            self.context_menu.place_forget()
            # Remover el bind temporal
            self.chat_display.unbind("<Button-1>")

        def _copy_selected(self, event) -> None:
            """Copiar texto seleccionado."""
            try:
                selected_text = self.chat_display.get("sel.first", "sel.last")
                self.clipboard_clear()
                self.clipboard_append(selected_text)
            except:
                pass  # No hay selección

        def _paste_to_entry(self, event) -> None:
            """Pegar texto en el campo de entrada."""
            try:
                clipboard_text = self.clipboard_get()
                self.entry.insert("insert", clipboard_text)
            except:
                pass  # No hay contenido en el portapapeles

        def _on_close(self) -> None:
            """Manejar cierre de ventana limpiando recursos."""
            # Ocultar menú contextual si está visible
            self.context_menu.place_forget()
            if self._ollama_status_job_id is not None:
                try:
                    self.after_cancel(self._ollama_status_job_id)
                except Exception:
                    pass
                self._ollama_status_job_id = None
            self.destroy()

        def export_conversation(self) -> None:
            """Exportar conversación actual como Markdown."""
            try:
                from tkinter import filedialog
                filename = filedialog.asksaveasfilename(
                    defaultextension=".md",
                    filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
                    title="Exportar conversación"
                )
                if filename:
                    success = self.conversation_history.export_markdown(filename)
                    if success:
                        self.status_label.configure(text=f"Conversación exportada: {filename}", text_color="#4ade80")
                        self.after(3000, lambda: self.status_label.configure(text="Listo", text_color="#888"))
                    else:
                        self.status_label.configure(text="Error al exportar conversación", text_color="#ff6b6b")
            except ImportError:
                # Fallback si tkinter no está disponible
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"conversacion_willow_{timestamp}.md"
                success = self.conversation_history.export_markdown(filename)
                if success:
                    self.status_label.configure(text=f"Conversación exportada: {filename}", text_color="#4ade80")
                else:
                    self.status_label.configure(text="Error al exportar conversación", text_color="#ff6b6b")

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

