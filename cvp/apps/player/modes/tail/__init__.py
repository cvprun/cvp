# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Dict, Final, Optional

from imgui_bundle import imgui
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.tail.tab import TailTab
from cvp.assets.fonts.mdi import FILE_EYE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.begin_tab_item import begin_tab_item, end_tab_item
from cvp.imgui.flags.tab_bar import (
    AUTO_SELECT_NEW_TABS,
    FITTING_POLICY_SCROLL,
    REORDERABLE,
)
from cvp.imgui.flags.tab_item import SET_SELECTED
from cvp.imgui.menu_container import MenuList
from cvp.imgui.menu_item import menu_item
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.text_centered import text_centered
from cvp.logging.loggers import logger
from cvp.types.override import override


class TailMode(BaseMode):
    __cvp_mode_name__ = "Tail"
    __cvp_mode_icon__ = FILE_EYE

    TAB_FLAGS: Final[int] = REORDERABLE | AUTO_SELECT_NEW_TABS | FITTING_POLICY_SCROLL

    _force_select: Optional[str]
    _tails: Dict[str, TailTab]

    def __init__(self, context: Context):
        super().__init__(context)
        self._open_file_popup = OpenFilePopup("Open file", target=self.on_open_file)
        self._popups = PopupList(self._open_file_popup)
        self._menus = MenuList(
            ("File", self.on_file_menu),
            ("Settings", self.on_settings_menu),
            ("View", self.on_view_menu),
        )
        self._force_select = None
        self._tails = dict()

    @property
    def config(self):
        return self.context.config.tail

    @property
    def selected_tail(self) -> Optional[TailTab]:
        if not self._tails:
            return None
        elif 1 == len(self._tails):
            return next(iter(self._tails.values()))
        else:
            assert 2 <= len(self._tails)
            return self._tails.get(self.selected_submenu, None)

    @staticmethod
    def file_label(file: str) -> str:
        return os.path.basename(file) + "###" + file

    def on_open_file(self, file: str) -> None:
        self.open_text_file(file)

    def open_text_file(self, file: str) -> None:
        file = str(Path(file).resolve())

        if file in self._tails:
            raise Exception(f"File already opened: '{file}'")

        try:
            self._tails[file] = TailTab.from_config(file, self.config)
            self.add_recent_item(file)
            logger.info(f"File opened successfully: '{file}'")
        except BaseException as e:
            self.context.toast_error(f"Text file open failed: '{e}'", logger)

    def close_text_file(self, file: str) -> None:
        file = str(Path(file).resolve())

        try:
            self._tails.pop(file)
            logger.info(f"File closed successfully: '{file}'")
        except BaseException as e:
            self.context.toast_error(f"Text file close failed: '{e}'", logger)

    @override
    def on_main_menu(self) -> None:
        self._menus.do_process()

    @override
    def on_status_menu(self) -> None:
        tail = self.selected_tail
        if tail is None:
            imgui.text("No file selected.")
            return

        assert isinstance(tail, TailTab)

        maxlen = tail.lines.maxlen if tail.lines.maxlen is not None else "INF"
        imgui.text(f"Lines {len(tail.lines)}, Max {maxlen}")
        imgui.separator()

        newline = repr(tail.newline)
        imgui.text(f"Newline {newline}")
        imgui.separator()

        autoscroll = "ON" if tail.autoscroll else "OFF"
        imgui.text(f"Autoscroll {autoscroll}")
        imgui.separator()

        imgui.text(tail.pathname)
        imgui.separator()

    @override
    def on_event(self, event: Event) -> bool:
        if event.type == DROPFILE:
            self.open_text_file(event.file)
            return True

        return False

    @override
    def on_file_modified(self, src: str, dest: str, isdir: bool):
        if isdir:
            return

        assert src == dest
        file = str(Path(src).resolve())
        tail = self._tails.get(file)
        if tail is None:
            return

        tail.update_buffer()

    def on_file_menu(self) -> None:
        if menu_item("Open file"):
            self._open_file_popup.show()

        if recent_item := self.menu_recent_items():
            self.open_text_file(recent_item.value)

        imgui.separator()

        selected_tail = self.selected_tail
        if menu_item("Close file", enabled=selected_tail is not None):
            assert selected_tail is not None
            self.close_text_file(selected_tail.path)

    @staticmethod
    def do_disabled_settings_menu() -> None:
        menu_item("Autoscroll", enabled=False)

    @staticmethod
    def do_enabled_settings_menu(tail: TailTab) -> None:
        autoscroll = tail.autoscroll
        if menu_item("Autoscroll", selected=autoscroll):
            tail.autoscroll = not autoscroll

    def on_settings_menu(self) -> None:
        if tail := self.selected_tail:
            self.do_enabled_settings_menu(tail)
        else:
            self.do_disabled_settings_menu()

    def on_view_menu(self) -> None:
        if not self._tails:
            menu_item("[EMPTY]", enabled=False)
            return

        for file in self._tails.keys():
            if menu_item(self.file_label(file)):
                self._force_select = file

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_main_process()
        self._popups.do_process()

    def do_main_process(self) -> None:
        with begin_child_context("Main"):
            if not self._tails:
                text_centered("Please open the text file")
            elif 1 == len(self._tails):
                next(iter(self._tails.values())).do_process()
            else:
                assert 2 <= len(self._tails)
                self.do_tabs_process()

    def do_tabs_process(self) -> None:
        if imgui.begin_tab_bar("Tabs", self.TAB_FLAGS):
            remove_keys = list()
            try:
                for file, terminal in self._tails.items():
                    flags = 0

                    if self._force_select == file:
                        flags |= SET_SELECTED
                        self._force_select = None

                    label = self.file_label(file)
                    tab_result = begin_tab_item(label, opened=True, flags=flags)

                    if not tab_result.opened_state:
                        remove_keys.append(file)

                    if tab_result.selected:
                        self.selected_submenu = file
                        try:
                            terminal.do_process()
                        finally:
                            end_tab_item()
            finally:
                imgui.end_tab_bar()

                assert len(remove_keys) in (0, 1)
                if remove_keys:
                    remove_key = remove_keys.pop()
                    assert not remove_keys

                    self.close_text_file(remove_key)
