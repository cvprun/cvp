# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.flags import table_column
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.table import ONVIF_TABLE_FLAGS
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.text_centered import text_centered
from cvp.ollama.ollama import Ollama
from cvp.types.override import override
from cvp.variables import DEFAULT_MENU_WIDTH, FULL_SIZE


class OllamaPreference(BasePreference):
    @unique
    class _OllamaCommand(StrEnum):
        list_ = auto()

    def __init__(self, context: Context):
        super().__init__(context)
        self._runner = context.pm.create_thread_runner(self._on_runner_main)

    @classmethod
    @override
    def get_menu_name(cls) -> str:
        return "Ollama"

    def _on_runner_main(self, ollama: Ollama, command: _OllamaCommand, *args: str):
        match command:
            case self._OllamaCommand.list_:
                self.__on_list(ollama)
            case _:
                assert False, "Inaccessible section"

    @staticmethod
    def __on_list(ollama: Ollama):
        response = ollama.client.list()
        ollama.model_names = list(response.models)

    @property
    def ollamas(self):
        return self.context.ollamas

    @property
    def selected(self) -> str:
        return self.context.config.ollama.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.context.config.ollama.selected = value

    @override
    def do_process(self) -> None:
        width = DEFAULT_MENU_WIDTH
        child_flags = RESIZE_X | BORDERS

        with begin_child_context("Menu", width, child_flags=child_flags):
            if imgui.button("Reload"):
                self.ollamas.reload_all_files()
            imgui.same_line()
            if imgui.button("New"):
                self.selected = self.ollamas.add_new()[0]
            imgui.same_line()
            if button("Remove", disabled=self.selected not in self.ollamas):
                del self.ollamas[self.selected]

            if imgui.begin_list_box("##List", FULL_SIZE):
                try:
                    for filename, ollama in self.ollamas.items():
                        label = f"{ollama.name}###{filename}"
                        if imgui.selectable(label, filename == self.selected)[1]:
                            self.selected = filename
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if ollama := self.ollamas.get(self.selected):
                self.do_ollama_process(self.selected, ollama)
            else:
                text_centered("Please select a item")

    def do_ollama_process(self, filename: str, ollama: Ollama) -> None:
        running = self._runner.running
        has_error = bool(self._runner.error)

        imgui.text(ollama.name)
        imgui.separator()

        with style_disable_input_context():
            input_text_value("Filename", filename)

        exists_path = self.ollamas.exists(filename)
        if button("Save"):
            self.ollamas.write(filename)
        imgui.same_line()
        if button("Load", disabled=not exists_path):
            self.ollamas.read(filename)
        imgui.same_line()
        if button("Remove", disabled=not exists_path):
            self.ollamas.remove(filename)
        if not exists_path:
            imgui.same_line()
            imgui.text_colored(self.context.warning_color, "The file does not exist")

        ollama.name = input_text_value("Ollama Name", ollama.name)
        ollama.url = input_text_value("Ollama URL", ollama.url)

        imgui.text("Headers")

        if imgui.begin_table("Headers", 2, ONVIF_TABLE_FLAGS):
            try:
                imgui.table_setup_column("Key")
                imgui.table_setup_column("Value")
                imgui.table_headers_row()
                for key, value in ollama.headers.items():
                    imgui.table_next_row()
                    imgui.table_set_column_index(0)
                    imgui.text(key)
                    imgui.table_set_column_index(1)
                    imgui.text(value)
            finally:
                imgui.end_table()

        for model_name in ollama.model_names:
            imgui.text(model_name)
