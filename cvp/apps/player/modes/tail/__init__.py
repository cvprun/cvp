# -*- coding: utf-8 -*-

import os
from typing import Dict, Final, Optional

from imgui_bundle import imgui
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FILE_EYE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.begin_tab_item import begin_tab_item, end_tab_item
from cvp.imgui.flags.tab_bar import (
    AUTO_SELECT_NEW_TABS,
    FITTING_POLICY_SCROLL,
    REORDERABLE,
)
from cvp.imgui.flags.tab_item import SET_SELECTED, TRAILING
from cvp.imgui.menu_container import MenuList
from cvp.imgui.menu_item import menu_item
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.widgets.terminal_canvas import TerminalCanvas, TerminalCanvasOptions
from cvp.logging.loggers import logger
from cvp.types.override import override


class TailMode(BaseMode):
    __cvp_mode_name__ = "Tail"
    __cvp_mode_icon__ = FILE_EYE

    TAB_FLAGS: Final[int] = REORDERABLE | AUTO_SELECT_NEW_TABS | FITTING_POLICY_SCROLL

    _force_select: Optional[str]
    _terminals: Dict[str, TerminalCanvas]

    def __init__(self, context: Context):
        super().__init__(context)
        self._open_file_popup = OpenFilePopup("Open file", target=self.on_open_file)
        self._popups = PopupList(self._open_file_popup)
        self._menus = MenuList(
            ("File", self.on_file_menu),
            ("View", self.on_view_menu),
        )
        self._force_select = None
        self._terminals = dict()

    @property
    def config(self):
        return self.context.config.tail

    @property
    def selected_terminal(self) -> Optional[TerminalCanvas]:
        return self._terminals.get(self.selected_submenu)

    @staticmethod
    def file_label(file: str) -> str:
        return os.path.basename(file) + "###" + file

    def on_open_file(self, file: str) -> None:
        self.open_text_file(file)

    def open_text_file(self, file: str) -> None:
        if file in self._terminals:
            raise Exception(f"File already opened: '{file}'")

        try:
            options = TerminalCanvasOptions(
                lines=self.config.max_buffer_lines,
                autoscroll=True,
            )
            self._terminals[file] = TerminalCanvas(file, None, options)
            logger.info(f"File opened successfully: '{file}'")
        except BaseException as e:
            self.context.toast_error(f"Text file open failed: '{e}'", logger)

    def close_text_file(self, file: str) -> None:
        try:
            self._terminals.pop(file)
            logger.info(f"File closed successfully: '{file}'")
        except BaseException as e:
            self.context.toast_error(f"Text file close failed: '{e}'", logger)

    @override
    def on_main_menu(self) -> None:
        self._menus.do_process()

    @override
    def on_status_menu(self) -> None:
        pass

    @override
    def on_event(self, event: Event) -> bool:
        if event.type == DROPFILE:
            self.open_text_file(event.file)
            return True

        return False

    def on_file_menu(self) -> None:
        if menu_item("Open file"):
            self._open_file_popup.show()

        if recent_item := self.menu_recent_items():
            self.open_text_file(recent_item.value)

        imgui.separator()

        selected_file = self.selected_submenu
        if menu_item("Close file", enabled=selected_file in self._terminals):
            self.close_text_file(selected_file)

    def on_view_menu(self) -> None:
        if not self._terminals:
            menu_item("[EMPTY]", enabled=False)
            return

        for file in self._terminals.keys():
            if menu_item(self.file_label(file)):
                self._force_select = file

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                self.preprocess_read_runner()
                self.do_child_process()

        self._popups.do_process()

    def preprocess_read_runner(self) -> None:
        pass

    def do_child_process(self) -> None:
        if imgui.begin_tab_bar("TerminalTab", self.TAB_FLAGS):
            remove_keys = list()
            try:
                for file, terminal in self._terminals.items():
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

                if imgui.tab_item_button("+", TRAILING):
                    self._open_file_popup.show()
            finally:
                imgui.end_tab_bar()

                assert len(remove_keys) in (0, 1)
                if remove_keys:
                    remove_key = remove_keys.pop()
                    assert not remove_keys

                    self.close_text_file(remove_key)
