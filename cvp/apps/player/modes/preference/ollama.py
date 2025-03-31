# -*- coding: utf-8 -*-

from typing import List

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.input_text_value import input_text_value
from cvp.types.override import override
from ollama import Client, ListResponse


class Ollama(BasePreference):
    _models: List[ListResponse.Model]

    def __init__(self, context: Context):
        super().__init__(context)
        self._list_runner = context.pm.create_thread_runner(self._on_list_main)
        self._models: List[ListResponse.Model] = list()

    def _on_list_main(self, host: str):
        client = Client(host=host)
        response = client.list()
        self._models = list(response.models)

    @property
    def ollama_url(self) -> str:
        return self.context.config.chat.ollama_url

    @ollama_url.setter
    def ollama_url(self, value: str) -> None:
        self.context.config.chat.ollama_url = value

    @override
    def do_process(self) -> None:
        list_running = self._list_runner.running
        self.ollama_url = input_text_value("Ollama URL", self.ollama_url)

        if button("list", disabled=list_running):
            assert not list_running
            self._list_runner(self.ollama_url)

        if list_running:
            return

        for model in self._models:
            name = model.model if model.model else str()
            imgui.text(name)
