# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.flags import table_column
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import InputTextFlags
from cvp.imgui.flags.table import ONVIF_TABLE_FLAGS
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.text_centered import text_centered
from cvp.ollama.ollama import Ollama
from cvp.types.override import override
from cvp.variables import DEFAULT_MENU_WIDTH, FULL_SIZE, NOT_FOUND_INDEX


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
            self.context.mq.append_toast("Save ollama file")

        imgui.same_line()
        if button("Load", disabled=not exists_path):
            self.ollamas.read(filename)
            self.context.mq.append_toast("Load ollama file")

        imgui.same_line()
        if button("Remove", disabled=not exists_path):
            self.ollamas.remove(filename)
            self.context.mq.append_toast("Remove ollama file")

        if not exists_path:
            imgui.same_line()
            imgui.text_colored(self.context.warning_color, "The file does not exist")

        ollama.name = input_text_value("Ollama Name", ollama.name)
        ollama.url = input_text_value("Ollama URL", ollama.url)

        imgui.text("Headers")
        imgui.same_line()
        if imgui.small_button("Add"):
            ollama.headers.append((str(), str()))

        if imgui.begin_table("Headers", 3, ONVIF_TABLE_FLAGS):
            try:
                imgui.table_setup_column("Key", table_column.WIDTH_STRETCH)
                imgui.table_setup_column("Value", table_column.WIDTH_STRETCH)
                imgui.table_setup_column("Action", table_column.WIDTH_FIXED)
                imgui.table_headers_row()

                remove_index = NOT_FOUND_INDEX
                for i in range(len(ollama.headers)):
                    key, value = ollama.headers[i]

                    imgui.table_next_row()

                    imgui.table_set_column_index(0)
                    imgui.set_next_item_width(-1)
                    key_result = imgui.input_text(f"###HeaderKey{i}", key)
                    if key_result[0]:
                        ollama.headers[i] = key_result[1], value

                    imgui.table_set_column_index(1)
                    imgui.set_next_item_width(-1)
                    val_result = imgui.input_text(f"###HeaderValue{i}", value)
                    if val_result[0]:
                        ollama.headers[i] = key, val_result[1]

                    imgui.table_set_column_index(2)
                    if imgui.button(f"Remove###Remove{i}"):
                        remove_index = i

                if remove_index != NOT_FOUND_INDEX:
                    ollama.headers.pop(remove_index)

                imgui.get_column_width(0)
            finally:
                imgui.end_table()

        for model_name in ollama.model_names:
            imgui.text(model_name)
