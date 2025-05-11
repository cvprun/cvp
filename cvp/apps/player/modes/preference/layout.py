# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import READ_ONLY
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.text_centered import text_centered
from cvp.imgui.text_colored import text_colored
from cvp.types.colors import GREEN_RGBA, RED_RGBA
from cvp.types.override import override


class LayoutPreference(BasePreference):
    __cvp_menu_name__ = "Layout"

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
        self._filenames = self._find_layout_filenames()

        self._rename_candidate = str()
        self._rename_input = InputTextPopup(
            title="Layout Rename",
            label="Rename the layout filename?",
            ok="Rename",
            cancel="Cancel",
            target=self.on_rename_input,
            validate=self.on_rename_input_validate,
        )

        self._remove_candidate = Path()
        self._confirm_remove = ConfirmPopup(
            title="Layout Remove",
            label="Are you sure you want to remove layout?",
            ok="Remove",
            cancel="Cancel",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Layout Clear",
            label="Are you sure you want to remove all layout?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

    @property
    def filenames(self):
        return self._filenames

    def _find_layout_filenames(self):
        return self.context.home.layouts.list_layout_filenames()

    def reload_layout_filenames(self) -> None:
        self._filenames = self._find_layout_filenames()

    def on_rename_input(self, value: str) -> None:
        if not value:
            return

        src = self.get_layout_filepath(self._rename_candidate)
        dest = self.get_layout_filepath(value)

        assert src.is_file()
        assert not dest.exists()

        shutil.move(src, dest)

        self.reload_layout_filenames()
        self.selected_submenu = value

    def on_rename_input_validate(self, value: str) -> bool:
        if not self.get_layout_filepath(self._rename_candidate).is_file():
            return False
        if self.get_layout_filepath(value).exists():
            return False
        assert self._rename_candidate != value
        return True

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        path = self._remove_candidate
        assert path.is_file()
        path.unlink()
        self.reload_layout_filenames()

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        for filename in self._filenames:
            self.get_layout_filepath(filename).unlink(missing_ok=True)
        self.reload_layout_filenames()

    def get_layout_filepath(self, filename: str):
        return self.context.home.layouts.as_path() / filename

    def load_layout(self, filename: str) -> None:
        imgui.load_ini_settings_from_disk(str(self.get_layout_filepath(filename)))
        self.context.msgs.append_toast(f"Load layout file: '{filename}'")

    def save_layout(self, filename: str) -> None:
        imgui.save_ini_settings_to_disk(str(self.get_layout_filepath(filename)))
        self.context.msgs.append_toast(f"Save layout file: '{filename}'")

    def save_new_layout(self, *, select=False, reload=False) -> None:
        filename = self.context.home.layouts.generate_nonexistent_filename()
        self.save_layout(filename)
        if select:
            self.selected_submenu = filename
        if reload:
            self.reload_layout_filenames()

    def show_remove_popup(self, filename: str) -> None:
        filepath = self.get_layout_filepath(filename)
        if not filepath.is_file():
            self.context.msgs.append_toast(f"Layout file not found: '{filename}'")
            return

        self._remove_candidate = filepath
        self._confirm_remove.show()

    @override
    def on_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.button("Reload"):
                self.reload_layout_filenames()
            imgui.same_line()
            if imgui.button("New"):
                filename = self.context.home.layouts.generate_nonexistent_filename()
                self.save_layout(filename)
                self.selected_submenu = filename
                self.reload_layout_filenames()
            imgui.same_line()
            disabled_delete = self.selected_submenu not in self._filenames
            if button("Del", disabled=disabled_delete):
                self.show_remove_popup(self.selected_submenu)
            imgui.same_line()
            if button("Clear", disabled=not self._filenames):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for filename in self._filenames:
                        selected = filename == self.selected_submenu
                        if imgui.selectable(filename, selected)[1]:
                            self.selected_submenu = filename
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            try:
                filename_index = self._filenames.index(self.selected_submenu)
                assert 0 <= filename_index < len(self._filenames)
                self.do_filename_process(self._filenames[filename_index])
            except ValueError:
                text_centered("Please select a item")

    def do_filename_process(self, filename: str) -> None:
        filepath = self.context.home.layouts / filename
        has_layout = filepath.is_file()

        input_text_disabled("Filename", filename, READ_ONLY)

        if button("Save"):
            self.save_layout(filename)
        imgui.same_line()
        if button("Load", disabled=not has_layout):
            self.load_layout(filename)
        imgui.same_line()
        if button("Rename"):
            self._rename_candidate = filename
            self._rename_input.text = filename
            self._rename_input.show()
        imgui.same_line()
        if button("Remove", disabled=not has_layout):
            self.show_remove_popup(filename)

        if has_layout:
            status_text = "Layout file exists"
            status_color = GREEN_RGBA
        else:
            status_text = "The layout file does not exist"
            status_color = RED_RGBA

        text_colored(status_text, status_color)

    @override
    def on_postprocess(self) -> None:
        self._rename_input.on_process()
        self._confirm_remove.on_process()
        self._confirm_clear.on_process()
