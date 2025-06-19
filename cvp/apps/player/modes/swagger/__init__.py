# -*- coding: utf-8 -*-

from os import PathLike
from typing import BinaryIO, Union

from imgui_bundle import imgui, imgui_color_text_edit
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import CODE_BRACES_BOX
from cvp.concurrency.threading.progress_value import ProgressValue
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.menu_container import MenuList
from cvp.imgui.menu_item import menu_item
from cvp.imgui.menu_recent_items import menu_recent_items
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.logging.loggers import logger
from cvp.types.override import override


class SwaggerMode(BaseMode):
    __cvp_mode_name__ = "Swagger"
    __cvp_mode_icon__ = CODE_BRACES_BOX

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

    def on_open_file(self, file: str) -> None:
        self.open_swagger_file(file)

    def on_open_runner(
        self,
        file: Union[str, PathLike[str], BinaryIO],
        progress: ProgressValue,
    ) -> str:
        filepath = ":memory:" if hasattr(file, "read") else str(file)
        try:
            progress.set(0, limit=100)
            if hasattr(file, "read"):
                text = file.read()
                if isinstance(text, bytes):
                    text = text.decode(encoding="utf-8", errors="strict")
                assert isinstance(text, str)
            else:
                with open(file, "rt") as f:
                    text = f.read()
            logger.info(f"Text file loaded: '{filepath}'")
            progress.set(100, limit=100)
            self.editor.set_text(text)
            return text
        except BaseException as e:
            logger.error(f"Failed to load text file '{filepath}': {e}")
            raise

    def open_swagger_file(self, file: Union[str, PathLike[str], BinaryIO]) -> None:
        if self._open_runner.running:
            raise ValueError("Open runner is already running")

        self.editor.set_text("")

        try:
            self._open_runner(file, self._open_progress)

            if not hasattr(file, "read"):
                self.add_recent_item(str(file))
        except BaseException as e:
            logger.exception(e)
            self.context.toast_error(f"Text file open failed: '{e}'")

    def close(self) -> None:
        if self._open_runner.running:
            raise ValueError("Open runner is already running")

        self.editor.set_text("")
        logger.info("Text file closed")

    @override
    def on_main_menu(self) -> None:
        self._menus.do_process()

    @override
    def on_status_menu(self) -> None:
        if self._open_runner.running:
            value, limit, _ = self._open_progress.get()
            imgui.text(f"Opening {value}/{limit} ...")
            return

        if self._open_runner.error is not None:
            error_message = str(self._open_runner.error)
            imgui.text_colored(self.error_color, error_message)
            return

    @override
    def on_event(self, event: Event) -> bool:
        if event.type == DROPFILE:
            self.open_swagger_file(event.file)
            return True

        return False

    def on_file_menu(self) -> None:
        if menu_item("Open file"):
            self._open_file_popup.show()

        if recent_item := menu_recent_items(
            label="Recent files",
            config=self.context.config.navigation,
            cls=type(self),
            append_clear_menu=True,
            clear_menu_label="Clear recent files",
        ):
            self.open_swagger_file(recent_item.value)

        imgui.separator()
        if menu_item("Close file", enabled=bool(self.editor.get_text())):
            self.close()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                self.do_child_process()
        self._popups.do_process()

    def do_child_process(self) -> None:
        pass
