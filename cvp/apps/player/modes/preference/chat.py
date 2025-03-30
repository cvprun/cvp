# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.types.override import override


class Chat(BasePreference):
    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def chat_ollama_url(self) -> str:
        return self.context.config.chat.ollama_url

    @chat_ollama_url.setter
    def chat_ollama_url(self, value: str) -> None:
        self.context.config.chat.ollama_url = value

    @override
    def do_process(self) -> None:
        self.chat_ollama_url = imgui.input_text("Ollama URL", self.chat_ollama_url)[1]
