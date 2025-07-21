# -*- coding: utf-8 -*-

from typing import Dict, NamedTuple

from imgui_bundle import imgui
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.text.editor import TextEditor
from cvp.assets.fonts.mdi import FILE_DOCUMENT
from cvp.concurrency.threading.progress_value import ProgressValue
from cvp.context.context import Context
from cvp.filesystem.read import read_progressive
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.begin_tab_item import begin_tab_item, end_tab_item
from cvp.imgui.menu_container import MenuList
from cvp.imgui.menu_item import menu_item
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.logging.loggers import logger
from cvp.text.item import TextKey
from cvp.types.override import override


class TextOpenResult(NamedTuple):
    path: str
    encoding: str
    errors: str
    text: str


class TextMode(BaseMode):
    __cvp_mode_name__ = "Text"
    __cvp_mode_icon__ = FILE_DOCUMENT

    _editors: Dict[TextKey, TextEditor]

    def __init__(self, context: Context):
        super().__init__(context)
        self._open_file_popup = OpenFilePopup(
            title="Open file",
            target=self.on_open_file,
        )
        self._open_runner = context.create_thread_runner(self.on_open_runner)
        self._open_progress = ProgressValue()

        self._menus = MenuList(
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Settings", self.on_settings_menu),
        )
        self._popups = PopupList(self._open_file_popup)
        self._editors = dict()

    @property
    def config(self):
        return self.context.config.text

    @property
    def manager(self):
        return self.context.texts

    def on_open_file(self, file: str) -> None:
        self.open_text_file(file)

    def on_open_runner(self, path: str, encoding: str, errors: str) -> TextOpenResult:
        text = read_progressive(
            path=path,
            encoding=encoding,
            errors=errors,
            logger=logger,
            progress=self._open_progress,
        )
        return TextOpenResult(path, encoding, errors, text)

    def open_text_file(self, path: str) -> None:
        if self._open_runner.running:
            raise ValueError("Open runner is already running")

        try:
            self._open_runner(path, self.config.encoding, self.config.errors)
        except BaseException as e:
            logger.exception(e)
            self.context.toast_error(f"Text file open failed: '{e}'")

    def close(self) -> None:
        if self._open_runner.running:
            raise ValueError("Open runner is already running")

        # self.editor.set_text("")
        logger.info("Text file closed")

    @override
    def on_main_menu(self) -> None:
        self._menus.do_process()

    @override
    def on_status_menu(self) -> None:
        if self._open_runner.running:
            value, limit, _ = self._open_progress.get()
            imgui.text(f"Opening {value}/{limit} ...")

        if self._open_runner.error is not None:
            error_message = str(self._open_runner.error)
            imgui.text_colored(self.error_color, error_message)

    @override
    def on_event(self, event: Event) -> bool:
        if event.type == DROPFILE:
            self.open_text_file(event.file)
            return True
        return False

    def on_file_menu(self) -> None:
        if menu_item("New file", shortcut="Ctrl+N"):
            self.manager.add_new()
        if menu_item("Open file ...", shortcut="Ctrl+O"):
            self._open_file_popup.show()
        if recent_item := self.menu_recent_items():
            self.open_text_file(recent_item.value)
        if menu_item("Save", shortcut="Ctrl+S"):
            pass
        if menu_item("Save as ..."):
            pass

        imgui.separator()
        if menu_item("Close file"):
            self.close()

    @staticmethod
    def do_disabled_edit_menu() -> None:
        menu_item("Undo", shortcut="Ctrl+Z", enabled=False)
        menu_item("Redo", shortcut="Ctrl+Y", enabled=False)
        imgui.separator()
        menu_item("Cut", shortcut="Ctrl+X", enabled=False)
        menu_item("Copy", shortcut="Ctrl+C", enabled=False)
        menu_item("Paste", shortcut="Ctrl+V", enabled=False)
        menu_item("Delete", shortcut="Del", enabled=False)
        imgui.separator()
        menu_item("Select all", shortcut="Ctrl+A", enabled=False)

    def on_edit_menu(self) -> None:
        self.do_disabled_edit_menu()

    def on_settings_menu(self) -> None:
        pass

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                self.preprocess_open_runner()
                self.do_editor_tabs()

        self._popups.do_process()

    def preprocess_open_runner(self) -> bool:
        if self._open_runner.running:
            return False

        if self._open_runner.result is not None:
            result = self._open_runner.result
            assert isinstance(result, TextOpenResult)
            self.add_recent_item(result.path)

            try:
                text_item = self.manager.find_with_path(result.path)
                text_key = text_item.key
                text_item.encoding = result.encoding
                text_item.errors = result.errors
            except ValueError:
                text_key, text_item = self.manager.add_new(
                    path=result.path,
                    encoding=result.encoding,
                    errors=result.errors,
                )

            text_editor = self._editors.get(text_key)
            if text_editor is None:
                text_editor = TextEditor(text_item)
                self._editors[text_key] = text_editor

            text_editor.set_text(result.text)

            self._open_runner.clear()

        return True

    def do_editor_tabs(self) -> None:
        if imgui.begin_tab_bar("EditorTab"):
            try:
                for tab_uuid in self.config.tabs_order:
                    tab_key = TextKey(tab_uuid)
                    tab_item = self.manager.get(tab_key)
                    if tab_item is None:
                        continue

                    tab_result = begin_tab_item(tab_item.name, tab_item.opened)
                    selected = tab_result.selected
                    opened = tab_result.opened_state

                    if (
                        opened is not None
                        and tab_item.opened is not None
                        and tab_item.opened != opened
                    ):
                        tab_item.opened = opened

                    if selected:
                        try:
                            if text_editor := self._editors.get(tab_key):
                                text_editor.do_process()
                        finally:
                            end_tab_item()
            finally:
                imgui.end_tab_bar()
