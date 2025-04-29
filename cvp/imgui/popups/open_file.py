# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
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
        show_hidden=False,
        flags: Union[WindowFlags, int] = 0,
        *,
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
        self._selected = str()
        self._show_hidden = show_hidden

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
        if imgui.button(mdi.HOME):
            self._location_text = str(Path.home())
        hovered_tooltip_text("Home Directory")

        imgui.same_line()

        if imgui.button(mdi.ARROW_UP_BOLD):
            self._location_text = str(Path(self._location_text).parent)
        hovered_tooltip_text("Parent Directory")

        imgui.same_line()

        show_hidden_icon = mdi.EYE if self._show_hidden else mdi.EYE_OFF
        if imgui.button(show_hidden_icon):
            self._show_hidden = not self._show_hidden
            self._items = self.list_items(self._current_dir, self._show_hidden)
        hovered_tooltip_text("Show Hidden Files and Directories")

        imgui.same_line()

        if imgui.button(mdi.REFRESH):
            self._items = self.list_items(self._current_dir, self._show_hidden)
        hovered_tooltip_text("Refresh Current Directory")

        imgui.same_line()

        with item_width(FIT_WIDTH):
            loc_result = input_text(
                "##Location",
                self._location_text,
                ENTER_RETURNS_TRUE,
            )

        loc_changed = loc_result.changed
        loc_text = loc_result.value

        if loc_changed:
            if os.path.isfile(loc_text):
                imgui.close_current_popup()
                return loc_text
            elif os.path.isdir(loc_text):
                self._location_text = loc_text
            else:
                logger.warning(f"Invalid location: '{loc_text}'")

        if begin_child("Files", (0, footer_height_as_reverse()), BORDERS):
            try:
                if self._current_dir != self._location_text:
                    # Update items
                    self._current_dir = self._location_text
                    self._selected = str()
                    self._items = self.list_items(self._current_dir, self._show_hidden)

                for item in self._items:
                    item_path = os.path.join(self._location_text, item)
                    selected = item_path == self._selected

                    if os.path.isfile(item_path):
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

        if imgui.button("Close"):
            imgui.close_current_popup()
            return None

        imgui.same_line()

        select_file = os.path.isfile(self._selected)
        select_dir = os.path.isdir(self._selected)
        enabled_open = select_file or select_dir

        if button("Open", disabled=not enabled_open):
            if select_file:
                imgui.close_current_popup()
                return self._selected
            elif select_dir:
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
