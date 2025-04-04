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
from cvp.imgui.flags.table import ONVIF_TABLE_FLAGS
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.text_centered import text_centered
from cvp.ollama.ollama import Ollama
from cvp.types.override import override
from cvp.variables import (
    DEFAULT_MENU_WIDTH,
    FULL_HEIGHT,
    FULL_SIZE,
    FULL_WIDTH,
    NOT_FOUND_INDEX,
)


class OllamaPreference(BasePreference):
    @unique
    class RunnerCommand(StrEnum):
        list_ = "list"
        show = auto()

    def __init__(self, context: Context):
        super().__init__(context)
        self._runner = context.pm.create_thread_runner(self._on_runner_main)

    @classmethod
    @override
    def get_menu_name(cls) -> str:
        return "Ollama"

    def _on_runner_main(self, ollama: Ollama, command: RunnerCommand, *args: str):
        match command:
            case self.RunnerCommand.list_:
                ollama.update_model_names()
            case self.RunnerCommand.show:
                assert 1 == len(args)
                assert isinstance(args[0], str)
                model_name = args[0]
                ollama.show_model(model_name)
            case _:
                assert False, "Inaccessible section"

    @property
    def ollamas(self):
        return self.context.ollamas

    __submenu_filename_key__ = "filename"

    @property
    def selected_submenu_filename(self) -> str:
        return self.get_selected_submenu(self.__submenu_filename_key__)

    @selected_submenu_filename.setter
    def selected_submenu_filename(self, value: str) -> None:
        self.set_selected_submenu(self.__submenu_filename_key__, value)

    __submenu_model_key__ = "model"

    @property
    def selected_submenu_model(self) -> str:
        return self.get_selected_submenu(self.__submenu_model_key__)

    @selected_submenu_model.setter
    def selected_submenu_model(self, value: str) -> None:
        self.set_selected_submenu(self.__submenu_model_key__, value)

    @override
    def do_process(self) -> None:
        width = DEFAULT_MENU_WIDTH
        child_flags = RESIZE_X | BORDERS

        with begin_child_context("Menu", width, child_flags=child_flags):
            if imgui.button("Reload"):
                self.ollamas.reload_all_files()
            imgui.same_line()
            if imgui.button("Add"):
                self.selected_submenu_filename = self.ollamas.add_new()[0]
            imgui.same_line()
            disabled_delete = self.selected_submenu_filename not in self.ollamas
            if button("Del", disabled=disabled_delete):
                del self.ollamas[self.selected_submenu_filename]

            if imgui.begin_list_box("##List", FULL_SIZE):
                try:
                    for filename, ollama in self.ollamas.items():
                        label = f"{ollama.name}###{filename}"
                        selected = filename == self.selected_submenu_filename
                        if imgui.selectable(label, selected)[1]:
                            self.selected_submenu_filename = filename
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if ollama := self.ollamas.get(self.selected_submenu_filename):
                if imgui.begin_tab_bar("MainTabBar"):
                    try:
                        if imgui.begin_tab_item("Config")[0]:
                            try:
                                self.do_ollama_config(
                                    self.selected_submenu_filename,
                                    ollama,
                                )
                            finally:
                                imgui.end_tab_item()

                        if imgui.begin_tab_item("APIs")[0]:
                            try:
                                self.do_ollama_apis(ollama)
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

    def do_ollama_apis(self, ollama: Ollama) -> None:
        running = self._runner.running
        has_error = bool(self._runner.error)

        if imgui.begin_list_box("##APIList", (DEFAULT_MENU_WIDTH, FULL_HEIGHT)):
            try:
                if imgui.button("Reload"):
                    self._runner(ollama, self.RunnerCommand.list_)
                if not running and not has_error:
                    for model_name in ollama.model_names:
                        selected = model_name == self.selected_submenu_model
                        if imgui.selectable(model_name, selected)[1]:
                            self.selected_submenu_model = model_name
            finally:
                imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("APIMain", FULL_WIDTH, FULL_HEIGHT):
            if running:
                text_centered("Requesting a list of models...")
            elif has_error:
                assert not running
                error_message = str(self._runner.error)
                imgui.text_colored(self.context.error_color, error_message)
            else:
                assert not running
                assert not has_error
                try:
                    index = ollama.model_names.index(self.selected_submenu_model)
                    self.do_ollama_model_details(ollama, index)
                except ValueError:
                    text_centered("Please select a item")
                    return

    def do_ollama_model_details(self, ollama: Ollama, model_index: int) -> None:
        model_name = ollama.model_names[model_index]

        with style_disable_input_context():
            input_text_value("Model Name", model_name)

        imgui.separator()

        if imgui.button("Show"):
            self._runner(ollama, self.RunnerCommand.show, model_name)

        imgui.separator()

        detail = ollama.details.get(model_name)
        if detail is None:
            return

        modified_at = detail.modified_at.isoformat() if detail.modified_at else str()
        template = detail.template if detail.template else str()
        model_file = detail.model_file if detail.model_file else str()
        license_ = detail.license if detail.license else str()
        # model_info = detail.model_info if detail.model_info else dict()
        parameters = detail.parameters if detail.parameters else str()

        parent_model = detail.parent_model if detail.parent_model else str()
        format_ = detail.format if detail.format else str()
        family = detail.family if detail.family else str()
        # families = detail.families if detail.families else list()
        parameter_size = detail.parameter_size if detail.parameter_size else str()
        quantization = detail.quantization_level if detail.quantization_level else str()

        with style_disable_input_context():
            input_text_value("Modified At", modified_at)
            input_text_value("Template", template)
            input_text_value("Model File", model_file)
            input_text_value("License", license_)
            input_text_value("Parameters", parameters)

            input_text_value("Parent Model", parent_model)
            input_text_value("Format", format_)
            input_text_value("Family", family)
            input_text_value("Parameter Size", parameter_size)
            input_text_value("Quantization Level", quantization)
