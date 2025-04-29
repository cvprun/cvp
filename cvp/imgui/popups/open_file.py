# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from shutil import rmtree
from typing import Callable, List, Optional, Union

import pygame
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
from cvp.imgui.push_item_width import item_width
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.logging.logging import logger
from cvp.types.override import override


class OpenFilePopup(PopupBase[str]):
    __cvp_popup_min_width__ = 520
    __cvp_popup_min_height__ = 420

    def __init__(
        self,
        title: Optional[str] = None,
        directory: Optional[Union[str, PathLike]] = None,
        flags: Union[WindowFlags, int] = 0,
        *,
        target: Optional[Callable[[str], None]] = None,
        oneshot: Optional[bool] = None,
        identifier: Optional[str] = None,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        centered=True,
        show_hidden=False,
        select_directory=False,
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
        self._selected = str()
        self._filter = str()
        self._show_hidden = show_hidden
        self._select_directory = select_directory

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

        if not os.path.exists(self._selected):
            return

        if os.path.isfile(self._selected):
            os.remove(self._selected)
        elif os.path.isdir(self._selected):
            rmtree(self._selected)

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
        self._selected = str()

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

    @override
    def on_process(self) -> Optional[str]:
        try:
            return self.on_main_process()
        finally:
            self._create_directory_popup.do_process()
            self._remove_item_popup.do_process()

    def on_main_process(self) -> Optional[str]:
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

        if button(mdi.CLOSE, disabled=not self._selected):
            if os.path.isfile(self._selected):
                name = os.path.basename(self._selected)
                self._remove_item_popup.label = f"Delete '{name}' file?"
                self._remove_item_popup.show()
            elif os.path.isdir(self._selected):
                name = os.path.basename(self._selected)
                self._remove_item_popup.label = f"Delete '{name}' directory?"
                self._remove_item_popup.show()
        hovered_tooltip_text("New Directory")

        imgui.same_line()

        show_hidden_icon = mdi.EYE if self._show_hidden else mdi.EYE_OFF
        if button(show_hidden_icon):
            self._show_hidden = not self._show_hidden
            self._items = self.list_items(self._current_dir, self._show_hidden)
        hovered_tooltip_text("Show Hidden Files and Directories")

        imgui.same_line()

        if button(mdi.REFRESH):
            self._items = self.list_items(self._current_dir, self._show_hidden)
        hovered_tooltip_text("Refresh Current Directory")

        imgui.same_line()

        with item_width(FIT_WIDTH):
            filter_result = imgui.input_text_with_hint(
                "##Filter",
                "Filter",
                self._filter,
            )
            if filter_result[0]:
                self._filter = filter_result[1]

        with item_width(FIT_WIDTH):
            if location_result := input_text(
                "##Location",
                self._location_text,
                ENTER_RETURNS_TRUE,
            ):
                location_text = location_result.value
                if os.path.isfile(location_text):
                    if not self._select_directory:
                        imgui.close_current_popup()
                        return location_text
                elif os.path.isdir(location_text):
                    self._location_text = location_text
                else:
                    logger.warning(f"Invalid location: '{location_text}'")

        if begin_child("Files", (0, footer_height_as_reverse()), BORDERS):
            try:
                if self._current_dir != self._location_text:
                    # Update items
                    self._current_dir = self._location_text
                    self._selected = str()
                    self._items = self.list_items(self._current_dir, self._show_hidden)

                for item in self._items:
                    if self._filter and item.find(self._filter) == -1:
                        continue

                    item_path = os.path.join(self._location_text, item)
                    selected = item_path == self._selected

                    if os.path.isfile(item_path):
                        if self._select_directory:
                            continue
                        label = f"{mdi.FILE} {item}"
                        if imgui.selectable(label, selected, ALLOW_DOUBLE_CLICK)[0]:
                            self._selected = item_path
                            if imgui.is_mouse_double_clicked(0):
                                imgui.close_current_popup()
                                return item_path
                    elif os.path.isdir(item_path):
                        label = f"{mdi.FOLDER} {item}/"
                        if imgui.selectable(label, selected, ALLOW_DOUBLE_CLICK)[0]:
                            self._selected = item_path
                            if imgui.is_mouse_double_clicked(0):
                                self._location_text = item_path
            finally:
                end_child()

        imgui.separator()

        if button("Close"):
            imgui.close_current_popup()
            return None

        if self._select_directory:
            imgui.same_line()
            if button("Select current location"):
                imgui.close_current_popup()
                return self._location_text

        imgui.same_line()

        select_file = os.path.isfile(self._selected)
        select_dir = os.path.isdir(self._selected)

        if button("Select", disabled=not select_file and not select_dir):
            if select_file:
                assert self._select_directory
                imgui.close_current_popup()
                return self._selected
            elif select_dir:
                if self._select_directory:
                    imgui.close_current_popup()
                    return self._selected
                else:
                    self._location_text = self._selected

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return None

        if self._selected and pygame.key.get_pressed()[pygame.K_RETURN]:
            if select_file:
                imgui.close_current_popup()
                return self._selected
            elif select_dir:
                self._location_text = self._selected

        return None
