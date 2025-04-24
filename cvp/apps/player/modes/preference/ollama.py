# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final, Tuple

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.fit_size import FIT_HEIGHT, FIT_SIZE
from cvp.imgui.flags import table_column
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.table import ONVIF_TABLE_FLAGS
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.text_centered import text_centered
from cvp.ollama.ollama import Ollama
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX


class OllamaPreference(BasePreference):
    __cvp_menu_name__ = "Ollama"

    _MENU_SPLIT_X: Final[int] = 150
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS
    _API_LIST_SIZE: Final[Tuple[int, int]] = 150, int(FIT_HEIGHT)

    @unique
    class RunnerCommand(StrEnum):
        list_ = "list"
        show = auto()

    def __init__(self, context: Context):
        super().__init__(context)
        self._selected_model = str()
        self._runner = context.create_thread_runner(self._on_runner_main)

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

    def get_selected_submenu_model(self, ollama: Ollama) -> str:
        return self.get_selected_submenu(suffix=ollama.uuid)

    def set_selected_submenu_model(self, ollama: Ollama, value: str) -> None:
        self.set_selected_submenu(value, suffix=ollama.uuid)

    @override
    def do_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.button("Reload"):
                self.ollamas.read_all_config_files()
            imgui.same_line()
            if imgui.button("Add"):
                self.selected = self.ollamas.add_new()[0]
            imgui.same_line()
            disabled_delete = self.selected not in self.ollamas
            if button("Del", disabled=disabled_delete):
                self.ollamas.remove(self.selected)

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for filename, ollama in self.ollamas.items():
                        label = f"{ollama.name}###{filename}"
                        selected = filename == self.selected
                        if imgui.selectable(label, selected)[1]:
                            self.selected = filename
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if ollama := self.ollamas.get(self.selected):
                if imgui.begin_tab_bar("MainTabBar"):
                    try:
                        if imgui.begin_tab_item("Config")[0]:
                            try:
                                self.do_ollama_config(self.selected, ollama)
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

    def do_ollama_apis(self, ollama: Ollama) -> None:
        running = self._runner.running
        has_error = bool(self._runner.error)

        if imgui.begin_list_box("##APIList", size=self._API_LIST_SIZE):
            try:
                if imgui.button("Reload"):
                    self._runner(ollama, self.RunnerCommand.list_)
                for model_name in ollama.model_names:
                    selected = model_name == self._selected_model
                    if imgui.selectable(model_name, selected)[1]:
                        self._selected_model = model_name
            finally:
                imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("APIMain", FIT_SIZE):
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
                    index = ollama.model_names.index(self._selected_model)
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
        template = detail.template
        model_file = detail.model_file
        license_ = detail.license
        model_info = detail.model_info
        parameters = detail.parameters

        parent_model = detail.parent_model
        format_ = detail.format
        family = detail.family
        families = detail.families
        parameter_size = detail.parameter_size
        quantization = detail.quantization_level

        with style_disable_input_context():
            input_text_value("Modified At", modified_at)
            imgui.input_text_multiline("Template", template)
            imgui.input_text_multiline("Model File", model_file)
            imgui.input_text_multiline("License", license_)

            if imgui.tree_node("Model info"):
                try:
                    for mk, mv in model_info.items():
                        input_text_value(mk, mv)
                finally:
                    imgui.tree_pop()

            imgui.input_text_multiline("Parameters", parameters)
            input_text_value("Parent Model", parent_model)
            input_text_value("Format", format_)
            input_text_value("Family", family)

            if imgui.tree_node("Families"):
                try:
                    for fi, fv in enumerate(families):
                        input_text_value(str(fi), fv)
                finally:
                    imgui.tree_pop()

            input_text_value("Parameter Size", parameter_size)
            input_text_value("Quantization Level", quantization)
