# -*- coding: utf-8 -*-

import os
from typing import Any, Final

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.flags.table import BORDERS, ROW_BG
from cvp.imgui.flags.table_column import WIDTH_FIXED, WIDTH_STRETCH
from cvp.imgui.input_text import input_text
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.types.dataclass.field_default import get_field_default
from cvp.types.dataclass.field_name import get_field_name
from cvp.types.override import override


class DirectoryPreference(BasePreference):
    __cvp_menu_name__ = "Directory"

    _TABLE_COLUMNS: Final[int] = 4
    _TABLE_FLAGS: Final[int] = BORDERS | ROW_BG

    def __init__(self, context: Context):
        super().__init__(context)
        self._directory_browser = OpenFilePopup(
            mode=OpenFilePopup.Mode.select_directory,
        )

    @property
    def config(self):
        return self.context.config.directory

    @property
    def success_color(self):
        return self.context.config.appearance.success_color

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def table_next_row(self, key: Any) -> None:
        assert isinstance(key, str)
        label = key.capitalize().replace("_", " ")

        imgui.table_next_row()

        imgui.table_set_column_index(0)
        imgui.text(label)

        imgui.table_set_column_index(1)
        imgui.set_next_item_width(FIT_WIDTH)
        value = getattr(self.config, key)

        if result := input_text(f"##LocationInput.{label}", value, ENTER_RETURNS_TRUE):
            value = result.value
            setattr(self.config, key, result.value)

        imgui.table_set_column_index(2)
        if os.path.isdir(value):
            imgui.text_colored(self.success_color, "Exists")
        else:
            imgui.text_colored(self.error_color, "Not exists")

        imgui.table_set_column_index(3)
        if imgui.button(f"Browse##BrowseButton.{label}"):
            self._directory_browser.show(
                title=f"Select {label} Directory",
                target=lambda x: setattr(self.config, key, x),
            )

        imgui.same_line()
        if imgui.button(f"Default##DefaultButton.{label}"):
            setattr(self.config, key, get_field_default(self.config, key))

    @override
    def on_process(self) -> None:
        if imgui.begin_table("Directory", self._TABLE_COLUMNS, self._TABLE_FLAGS):
            try:
                imgui.table_setup_column("Name", WIDTH_FIXED)
                imgui.table_setup_column("Location", WIDTH_STRETCH)
                imgui.table_setup_column("State", WIDTH_FIXED)
                imgui.table_setup_column("Action", WIDTH_FIXED)
                imgui.table_headers_row()

                self.table_next_row(get_field_name(self.config).user_documents)
                self.table_next_row(get_field_name(self.config).user_downloads)
                self.table_next_row(get_field_name(self.config).user_pictures)
                self.table_next_row(get_field_name(self.config).user_videos)
                self.table_next_row(get_field_name(self.config).user_music)
                self.table_next_row(get_field_name(self.config).user_desktop)
            finally:
                imgui.end_table()

    @override
    def on_postprocess(self) -> None:
        self._directory_browser.on_process()
