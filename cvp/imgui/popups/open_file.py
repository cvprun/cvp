# -*- coding: utf-8 -*-

import os
from enum import IntFlag, auto, unique
from functools import reduce
from os import PathLike
from pathlib import Path
from shutil import rmtree
from typing import Callable, List, Optional, Union

from imgui_bundle import imgui

from cvp.assets.fonts import mdi
from cvp.imgui.begin_child import begin_child, end_child
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.child import BORDERS
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.flags.selectable import ALLOW_DOUBLE_CLICK
from cvp.imgui.flags.window import WindowFlags
from cvp.imgui.footer_height_to_reverse import footer_height_as_reverse
from cvp.imgui.input_text import input_text
from cvp.imgui.popups._base import PopupBase
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.push_item_width import item_width_context
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.logging.loggers import logger
from cvp.types.colors import RED_RGBA
from cvp.types.override import override


@unique
class _OpenFilePopupMode(IntFlag):
    select_file = auto()
    select_directory = auto()
    input_filename = auto()
    show_hidden = auto()
    overwrite_popup = auto()


def merge_open_file_popup_modes(*modes: _OpenFilePopupMode) -> _OpenFilePopupMode:
    return reduce(lambda x, y: x | y, modes)


class OpenFilePopup(PopupBase[str]):
    __cvp_popup_min_width__ = 520
    __cvp_popup_min_height__ = 420

    Mode = _OpenFilePopupMode

    SELECT_FILE = _OpenFilePopupMode.select_file
    SELECT_DIRECTORY = _OpenFilePopupMode.select_directory
    INPUT_FILENAME = _OpenFilePopupMode.input_filename
    SHOW_HIDDEN = _OpenFilePopupMode.show_hidden
    OVERWRITE_POPUP = _OpenFilePopupMode.overwrite_popup

    SELECT_FILE_AND_DIRECTORY = merge_open_file_popup_modes(
        _OpenFilePopupMode.select_file,
        _OpenFilePopupMode.select_directory,
    )

    SAVE_FILE = merge_open_file_popup_modes(
        _OpenFilePopupMode.input_filename,
        _OpenFilePopupMode.overwrite_popup,
    )

    def __init__(
        self,
        title: Optional[str] = None,
        directory: Optional[Union[str, PathLike]] = None,
        flags: Union[WindowFlags, int] = 0,
        *,
        mode=Mode.select_file,
        error_color=RED_RGBA,
        ok_button_label="Open",
        cancel_button_label="Cancel",
        ok_dir_button_label="Select Current Location",
        target: Optional[Callable[[str], None]] = None,
        oneshot: Optional[bool] = None,
        identifier: Optional[str] = None,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        centered=True,
    ):
        super().__init__(
            title=title,
            flags=flags,
            target=target,
            oneshot=oneshot,
            identifier=identifier,
            min_width=min_width,
            min_height=min_height,
            centered=centered,
        )

        self._location_text = str(self.location_path(directory))
        self._current_dir = str()
        self._items: List[str] = list()
        self._selected_item = str()
        self._input_filename = str()
        self._input_filter = str()
        self._mode = mode
        self._error_color = error_color
        self._propagate_overwrite_result = False
        self._ok_button_label = ok_button_label
        self._cancel_button_label = cancel_button_label
        self._ok_dir_button_label = ok_dir_button_label

        self._create_directory_popup = InputTextPopup(
            title="New Directory",
            label="Enter a new folder name",
            ok="Make",
            cancel="Cancel",
            validate=self.on_create_directory_validator,
            target=self.on_create_directory,
        )
        self._remove_item_popup = ConfirmPopup(
            title="Delete",
            label="Delete item?",
            ok="Delete",
            cancel="Cancel",
            target=self.on_remove_item,
        )
        self._overwrite_popup = ConfirmPopup(
            title="Overwrite",
            label="Do you want to overwrite the file?",
            ok="Overwrite",
            cancel="Cancel",
            target=self.on_overwrite_item,
        )

    def has_mode_flag(self, mode: _OpenFilePopupMode) -> bool:
        return bool(self._mode & mode)

    def set_mode_flag(self, mode: _OpenFilePopupMode, enabled: bool) -> None:
        if enabled:
            self._mode |= mode
        else:
            self._mode &= ~mode

    @property
    def select_file_flag(self) -> bool:
        return self.has_mode_flag(self.Mode.select_file)

    @select_file_flag.setter
    def select_file_flag(self, value: bool) -> None:
        self.set_mode_flag(self.Mode.select_file, value)

    @property
    def select_directory_flag(self) -> bool:
        return self.has_mode_flag(self.Mode.select_directory)

    @select_directory_flag.setter
    def select_directory_flag(self, value: bool) -> None:
        self.set_mode_flag(self.Mode.select_directory, value)

    @property
    def input_filename_flag(self) -> bool:
        return self.has_mode_flag(self.Mode.input_filename)

    @input_filename_flag.setter
    def input_filename_flag(self, value: bool) -> None:
        self.set_mode_flag(self.Mode.input_filename, value)

    @property
    def show_hidden_flag(self) -> bool:
        return self.has_mode_flag(self.Mode.show_hidden)

    @show_hidden_flag.setter
    def show_hidden_flag(self, value: bool) -> None:
        self.set_mode_flag(self.Mode.show_hidden, value)

    @property
    def overwrite_popup_flag(self) -> bool:
        return self.has_mode_flag(self.Mode.overwrite_popup)

    @overwrite_popup_flag.setter
    def overwrite_popup_flag(self, value: bool) -> None:
        self.set_mode_flag(self.Mode.overwrite_popup, value)

    @property
    def any_subpopup_open(self) -> bool:
        return any(
            (
                self._create_directory_popup.opened,
                self._remove_item_popup.opened,
                self._overwrite_popup.opened,
            )
        )

    def on_create_directory_validator(self, value: str) -> bool:
        return not os.path.exists(os.path.join(self._current_dir, value))

    def on_create_directory(self, value: str) -> None:
        if not value:
            return

        path = os.path.join(self._current_dir, value)
        if os.path.exists(path):
            return

        os.makedirs(path, exist_ok=True)

    def on_remove_item(self, value: bool) -> None:
        if not value:
            return

        if not os.path.exists(self._selected_item):
            return

        if os.path.isfile(self._selected_item):
            os.remove(self._selected_item)
        elif os.path.isdir(self._selected_item):
            rmtree(self._selected_item)
        else:
            assert False, "Inaccessible section"

        self._selected_item = str()

    def on_overwrite_item(self, value: bool) -> None:
        self._propagate_overwrite_result = value

    @staticmethod
    def location_path(path: Optional[Union[str, PathLike]] = None) -> Path:
        if isinstance(path, Path):
            if path.is_dir():
                return path
            elif path.is_file():
                return path.parent
        elif isinstance(path, str):
            if os.path.isdir(path):
                return Path(path)
            elif os.path.isfile(path):
                return Path(path).parent
        return Path.home()

    def set_location(self, path: Optional[Union[str, PathLike]] = None) -> None:
        self._location_text = str(self.location_path(path))
        self._current_dir = str()
        self._items = list()
        self._selected_item = str()
        self._input_filename = str()

    @staticmethod
    def list_items(location: Union[str, PathLike], show_hidden=False) -> List[str]:
        dirs = list()
        files = list()

        items = os.listdir(location)
        items.sort()

        for item in items:
            if not show_hidden and item.startswith("."):
                continue
            item_path = os.path.join(location, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            elif os.path.isfile(item_path):
                files.append(item)

        return dirs + files

    def button_select(self, label="Open", pressed_enter_key=False) -> bool:
        if not self._selected_item:
            button(label, disabled=True)
            hovered_tooltip_text("No item has been selected", self._error_color)
            return False

        if not os.path.exists(self._selected_item):
            if self.input_filename_flag:
                result = button(label) or pressed_enter_key
                hovered_tooltip_text("Click to create the entered file")
                return result
            else:
                button(label, disabled=True)
                hovered_tooltip_text("No such file exists", self._error_color)
                return False

        isfile = os.path.isfile(self._selected_item)
        isdir = os.path.isdir(self._selected_item)
        assert isfile != isdir or (not isfile and not isdir)

        if isfile:
            if self.input_filename_flag:
                result = False
                if button(label) or pressed_enter_key:
                    if self.overwrite_popup_flag:
                        self._overwrite_popup.show()
                    else:
                        result = True
                hovered_tooltip_text("Click to overwrite the selected file")
                return result
            elif self.select_file_flag:
                result = button(label) or pressed_enter_key
                hovered_tooltip_text("Click to open the selected file")
                return result
            else:
                button(label, disabled=True)
                hovered_tooltip_text("Cannot select the file", self._error_color)
                return False
        elif isdir:
            if self.select_directory_flag:
                result = button(label) or pressed_enter_key
                hovered_tooltip_text("Click to open the selected directory")
                return result
            else:
                if button(label) or pressed_enter_key:
                    self._location_text = self._selected_item
                hovered_tooltip_text("Click to navigate to the selected directory")
                return False
        else:
            button(label, disabled=True)
            hovered_tooltip_text("This file type is not supported", self._error_color)
            return False

    @override
    def on_main_process(self) -> Optional[str]:
        try:
            return self.do_main_process()
        finally:
            self._create_directory_popup.on_process()
            self._remove_item_popup.on_process()
            self._overwrite_popup.on_process()

    def do_main_process(self) -> Optional[str]:
        if button(mdi.HOME):
            self._location_text = str(Path.home())
        hovered_tooltip_text("Home Directory")

        imgui.same_line()

        if button(mdi.ARROW_UP_BOLD):
            self._location_text = str(Path(self._location_text).parent)
        hovered_tooltip_text("Parent Directory")

        imgui.same_line()

        if button(mdi.FOLDER_PLUS):
            self._create_directory_popup.show()
        hovered_tooltip_text("New Directory")

        imgui.same_line()

        selected = bool(self._selected_item)
        if selected:
            isfile = os.path.isfile(self._selected_item)
            isdir = os.path.isdir(self._selected_item)
        else:
            isfile = False
            isdir = False
        assert isfile != isdir or (not isfile and not isdir)

        enabled_delete = selected and (isfile or isdir)
        if button(mdi.DELETE, disabled=not enabled_delete):
            if os.path.isfile(self._selected_item):
                name = os.path.basename(self._selected_item)
                self._remove_item_popup.label = f"Delete '{name}' file?"
                self._remove_item_popup.show()
            elif os.path.isdir(self._selected_item):
                name = os.path.basename(self._selected_item)
                self._remove_item_popup.label = f"Delete '{name}' directory?"
                self._remove_item_popup.show()

        if isfile:
            hovered_tooltip_text("Remove the selected file")
        elif isdir:
            hovered_tooltip_text("Remove the selected directory")
        else:
            hovered_tooltip_text("Remove the selected item")

        imgui.same_line()

        show_hidden_icon = mdi.EYE if self.show_hidden_flag else mdi.EYE_OFF
        if button(show_hidden_icon):
            self.set_mode_flag(self.Mode.show_hidden, not self.show_hidden_flag)
            self._items = self.list_items(self._current_dir, self.show_hidden_flag)
        hovered_tooltip_text("Show Hidden Files and Directories")

        imgui.same_line()

        if button(mdi.REFRESH):
            self._items = self.list_items(self._current_dir, self.show_hidden_flag)
        hovered_tooltip_text("Refresh Current Directory")

        imgui.same_line()

        with item_width_context(FIT_WIDTH):
            filter_result = imgui.input_text_with_hint(
                "##Filter",
                "Filter",
                self._input_filter,
            )
            if filter_result[0]:
                self._input_filter = filter_result[1]

        with item_width_context(FIT_WIDTH):
            if location_result := input_text(
                "##LocationBar",
                self._location_text,
                ENTER_RETURNS_TRUE,
            ):
                location_text = location_result.value
                if os.path.isfile(location_text):
                    if self.select_file_flag:
                        self.close()
                        return location_text
                elif os.path.isdir(location_text):
                    self._location_text = location_text
                else:
                    logger.warning(f"Invalid location: '{location_text}'")

        files_child_height = footer_height_as_reverse()
        if self.input_filename_flag:
            extra_filename_input_height = footer_height_as_reverse()
            files_child_height += extra_filename_input_height

        if begin_child("Files", (FIT_WIDTH, files_child_height), BORDERS):
            try:
                if self._current_dir != self._location_text:
                    # Update items
                    self._current_dir = self._location_text
                    self._selected_item = str()
                    self._input_filename = str()
                    self._items = self.list_items(
                        location=self._current_dir,
                        show_hidden=self.show_hidden_flag,
                    )

                for item in self._items:
                    if self._input_filter and item.find(self._input_filter) == -1:
                        continue

                    item_path = os.path.join(self._current_dir, item)
                    selected = item_path == self._selected_item

                    if os.path.isfile(item_path):
                        if not self.select_file_flag:
                            continue

                        label = f"{mdi.FILE} {item}"
                        if imgui.selectable(label, selected, ALLOW_DOUBLE_CLICK)[0]:
                            self._selected_item = item_path
                            self._input_filename = item
                            if imgui.is_mouse_double_clicked(0):
                                self.close()
                                return item_path
                    elif os.path.isdir(item_path):
                        label = f"{mdi.FOLDER} {item}/"
                        if imgui.selectable(label, selected, ALLOW_DOUBLE_CLICK)[0]:
                            self._selected_item = item_path
                            self._input_filename = item
                            if imgui.is_mouse_double_clicked(0):
                                self._location_text = item_path
            finally:
                end_child()

        imgui.separator()

        if self.input_filename_flag:
            with item_width_context(FIT_WIDTH):
                if filename_result := input_text("##Filename", self._input_filename):
                    self._input_filename = filename_result.value
                    self._selected_item = os.path.join(
                        self._current_dir,
                        self._input_filename,
                    )

        if self.any_subpopup_open:
            pressed_enter_key = False
            pressed_escape_key = False
        else:
            pressed_enter_key = imgui.is_key_pressed(imgui.Key.enter)
            pressed_escape_key = imgui.is_key_pressed(imgui.Key.escape)

        if button(self._cancel_button_label):
            self.close()
            return None

        imgui.same_line()
        if self.button_select(
            label=self._ok_button_label,
            pressed_enter_key=pressed_enter_key,
        ):
            self.close()
            return self._selected_item

        if self.select_directory_flag:
            imgui.same_line()
            if button(self._ok_dir_button_label):
                self.close()
                return self._current_dir
            hovered_tooltip_text("Click to open the current location directory")

        if pressed_escape_key:
            self.close()
            return None

        if self._propagate_overwrite_result:
            self._propagate_overwrite_result = False
            self.close()
            return self._selected_item

        return None
