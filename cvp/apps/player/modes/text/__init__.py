# -*- coding: utf-8 -*-

# from os import PathLike
# from typing import BinaryIO, Union
#
# from imgui_bundle import imgui
# from pygame import DROPFILE
# from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FILE_DOCUMENT
from cvp.concurrency.threading.progress_value import ProgressValue
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.menu_container import MenuList
from cvp.imgui.menu_item import menu_item
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.tab_container import TabList
from cvp.logging.loggers import logger
from cvp.types.override import override


class TextMode(BaseMode):
    __cvp_mode_name__ = "Text"
    __cvp_mode_icon__ = FILE_DOCUMENT

    def __init__(self, context: Context):
        super().__init__(context)
        self._open_file_popup = OpenFilePopup(
            title="Open file",
            target=self.on_open_file,
        )
        self._open_runner = context.create_thread_runner(self.on_open_runner)
        self._open_progress = ProgressValue()

        self._menus = MenuList(("File", self.on_file_menu))
        self._popups = PopupList(self._open_file_popup)
        self._tabs = TabList()

    @property
    def config(self):
        return self.context.config.text

    def on_open_file(self, file: str) -> None:
        # self.open_text_file(file)
        pass

    def on_open_runner(self, path: str) -> str:
        encoding = self.config.encoding
        errors = self.config.errors
        try:
            self._open_progress.set(0, limit=100)
            with open(path, "rt", encoding=encoding, errors=errors) as f:
                text = f.read()
            logger.info(f"Text file loaded: '{path}'")
            self._open_progress.set(100, limit=100)
            return text
        except BaseException as e:
            logger.error(f"Failed to load text file '{path}': {e}")
            raise

    # def open_text_file(self, file: Union[str, PathLike[str], BinaryIO]) -> None:
    #     if self._open_runner.running:
    #         raise ValueError("Open runner is already running")
    #
    #     self.editor.set_text("")
    #
    #     try:
    #         self._open_runner(file)
    #
    #         if not hasattr(file, "read"):
    #             self.add_recent_item(str(file))
    #     except BaseException as e:
    #         logger.exception(e)
    #         self.context.toast_error(f"Text file open failed: '{e}'")

    # def close(self) -> None:
    #     if self._open_runner.running:
    #         raise ValueError("Open runner is already running")
    #
    #     self.editor.set_text("")
    #     logger.info("Text file closed")

    # @override
    # def on_main_menu(self) -> None:
    #     self._menus.do_process()

    # @override
    # def on_status_menu(self) -> None:
    #     if self._open_runner.running:
    #         value, limit, _ = self._open_progress.get()
    #         imgui.text(f"Opening {value}/{limit} ...")
    #         return
    #
    #     if self._open_runner.error is not None:
    #         error_message = str(self._open_runner.error)
    #         imgui.text_colored(self.error_color, error_message)
    #         return

    # @override
    # def on_event(self, event: Event) -> bool:
    #     if event.type == DROPFILE:
    #         self.open_text_file(event.file)
    #         return True
    #     return False

    def on_file_menu(self) -> None:
        if menu_item("Open file"):
            self._open_file_popup.show()

        # if recent_item := menu_recent_items(
        #     label="Recent files",
        #     config=self.context.config.navigation,
        #     cls=type(self),
        #     append_clear_menu=True,
        #     clear_menu_label="Clear recent files",
        # ):
        #     self.open_text_file(recent_item.value)
        #
        # imgui.separator()
        # if menu_item("Close file", enabled=bool(self.editor.get_text())):
        #     self.close()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                self._tabs.do_process("EditorTab")

        self._popups.do_process()
