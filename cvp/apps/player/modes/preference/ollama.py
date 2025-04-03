# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.flags import table_column
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import InputTextFlags
from cvp.imgui.flags.table import ONVIF_TABLE_FLAGS
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.text_centered import text_centered
from cvp.ollama.ollama import Ollama
from cvp.types.override import override
from cvp.variables import DEFAULT_MENU_WIDTH, FULL_SIZE, NOT_FOUND_INDEX, FULL_HEIGHT, FULL_WIDTH


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
                ollama.update_model_names()
            case _:
                assert False, "Inaccessible section"

    @property
    def ollamas(self):
        return self.context.ollamas

    __selected_filename_key__ = "filename"

    @property
    def selected_filename(self) -> str:
        return self.get_selected(self.__selected_filename_key__)

    @selected_filename.setter
    def selected_filename(self, value: str) -> None:
        self.set_selected(self.__selected_filename_key__, value)

    __selected_api_key__ = "api"

    @property
    def selected_api(self) -> str:
        return self.get_selected(self.__selected_api_key__)

    @selected_api.setter
    def selected_api(self, value: str) -> None:
        self.set_selected(self.__selected_api_key__, value)

    @override
    def do_process(self) -> None:
        width = DEFAULT_MENU_WIDTH
        child_flags = RESIZE_X | BORDERS

        with begin_child_context("Menu", width, child_flags=child_flags):
            if imgui.button("Reload"):
                self.ollamas.reload_all_files()
            imgui.same_line()
            if imgui.button("Add"):
                self.selected_filename = self.ollamas.add_new()[0]
            imgui.same_line()
            if button("Del", disabled=self.selected_filename not in self.ollamas):
                del self.ollamas[self.selected_filename]

            if imgui.begin_list_box("##List", FULL_SIZE):
                try:
                    for filename, ollama in self.ollamas.items():
                        label = f"{ollama.name}###{filename}"
                        selected = filename == self.selected_filename
                        if imgui.selectable(label, selected)[1]:
                            self.selected_filename = filename
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if ollama := self.ollamas.get(self.selected_filename):
                if imgui.begin_tab_bar("MainTabBar"):
                    try:
                        if imgui.begin_tab_item("Config")[0]:
                            try:
                                self.do_ollama_config(self.selected_filename, ollama)
                            finally:
                                imgui.end_tab_item()

                        if imgui.begin_tab_item("APIs")[0]:
                            try:
                                self.do_ollama_apis(self.selected_filename, ollama)
                            finally:
                                imgui.end_tab_item()
                    finally:
                        imgui.end_tab_bar()
            else:
                text_centered("Please select a item")

    def do_ollama_config(self, filename: str, ollama: Ollama) -> None:
        imgui.text(ollama.name)
        imgui.separator()

        with style_disable_input_context():
            input_text_value("Filename", filename)

        if ollama.has_error:
            imgui.text_colored(self.context.error_color, str(ollama.error))
            if button("Remove"):
                self.ollamas.remove(filename)
                self.context.mq.append_toast("Remove ollama file")
            return

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
                    if imgui.button(f"Del###Del{i}"):
                        remove_index = i

                if remove_index != NOT_FOUND_INDEX:
                    ollama.headers.pop(remove_index)

                imgui.get_column_width(0)
            finally:
                imgui.end_table()

        if redirect_result := checkbox("Follow redirects", ollama.follow_redirects):
            ollama.follow_redirects = redirect_result.state

        if timeout_result := input_float("HTTP timeout (seconds)", ollama.timeout, 1.0):
            ollama.timeout = timeout_result.value

        imgui.separator()

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

        for model_name in ollama.model_names:
            imgui.text(model_name)

    def do_ollama_apis(self, filename: str, ollama: Ollama) -> None:
        running = self._runner.running
        has_error = bool(self._runner.error)

        if imgui.begin_list_box("##APIList", (DEFAULT_MENU_WIDTH, FULL_HEIGHT)):
            try:
                if imgui.selectable("list", self.selected_api == "list")[0]:
                    self.selected_api = "list"
                if imgui.selectable("ps", self.selected_api == "ps")[0]:
                    self.selected_api = "ps"
            finally:
                imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("APIMain", FULL_WIDTH, FULL_HEIGHT):
            pass
