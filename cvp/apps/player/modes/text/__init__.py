# -*- coding: utf-8 -*-

from collections import deque
from typing import Deque, Dict, Final, NamedTuple, Optional

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
from cvp.logging.loggers import logger
from cvp.text.item import TextItem, TextKey
from cvp.types.override import override


class _TextOpenResult(NamedTuple):
    path: str
    encoding: str
    errors: str
    text: str


class TextMode(BaseMode):
    __cvp_mode_name__ = "Text"
    __cvp_mode_icon__ = FILE_DOCUMENT

    TAB_FLAGS: Final[int] = REORDERABLE | AUTO_SELECT_NEW_TABS | FITTING_POLICY_SCROLL

    _editors: Dict[TextKey, TextEditor]
    _force_select: Optional[TextKey]
    _current_key: Optional[TextKey]
    _open_file_queue: Deque[str]

    def __init__(self, context: Context):
        super().__init__(context)

        self._open_file_popup = OpenFilePopup(
            title="Open file",
            target=self.on_open_file,
        )
        self._save_file_popup = OpenFilePopup(
            title="Save file",
            target=self.on_save_file,
            mode=OpenFilePopup.SAVE_FILE,
        )
        self._save_as_file_popup = OpenFilePopup(
            title="Save as ...",
            target=self.on_save_file,
            mode=OpenFilePopup.SAVE_FILE,
        )
        self._open_runner = context.create_thread_runner(self.on_open_runner)
        self._open_progress = ProgressValue()

        self._menus = MenuList(
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Settings", self.on_settings_menu),
            ("Tabs", self.on_tabs_menu),
        )
        self._popups = PopupList(
            self._open_file_popup,
            self._save_file_popup,
            self._save_as_file_popup,
        )

        self._editors = dict()
        self._force_select = None
        self._current_key = None

        self._open_file_queue = deque()
        for text_path in context.texts.unique_paths():
            self._open_file_queue.append(text_path)

    @property
    def config(self):
        return self.context.config.text

    @property
    def tabs_order(self):
        return [TextKey(uuid) for uuid in self.config.tabs_order]

    @property
    def manager(self):
        return self.context.texts

    @property
    def ordered_texts(self):
        return self.manager.ordered_values(self.tabs_order)

    @property
    def selected_text(self):
        if self._current_key is None:
            return None
        return self.manager.get(self._current_key, None)

    def on_open_file(self, file: str) -> None:
        self.open_text_file(file)

    def on_save_file(self, file: str) -> None:
        self.save_text_file(file)

    def on_open_runner(self, path: str, encoding: str, errors: str) -> _TextOpenResult:
        text = read_progressive(
            path=path,
            encoding=encoding,
            errors=errors,
            logger=logger,
            progress=self._open_progress,
        )
        return _TextOpenResult(path, encoding, errors, text)

    def open_text_file(self, path: str) -> None:
        if self._open_runner.running:
            raise ValueError("Open runner is already running")

        try:
            self._open_runner(path, self.config.encoding, self.config.errors)
        except BaseException as e:
            logger.exception(e)
            self.context.toast_error(f"Text file open failed: '{e}'")

    def save_text_file(self, path: str) -> None:
        pass

    def close_text(self, key: TextKey) -> None:
        self.manager.remove(key)

        try:
            self.tabs_order.remove(key)
        except:  # noqa
            pass

        logger.info(f"Closed text with key: {key}")

    def add_new_text(self, path: Optional[str] = None):
        return self.manager.add_new(
            path=path,
            encoding=self.config.encoding,
            errors=self.config.errors,
        )

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
        is_opening = self._open_runner.running
        is_selected_text = self.selected_text is not None

        if menu_item("New file", shortcut="Ctrl+N"):
            self.add_new_text()
        if menu_item("Open file ...", shortcut="Ctrl+O", enabled=not is_opening):
            if self._open_runner.running:
                raise ValueError("Open runner is already running")
            self._open_file_popup.show()
        if recent_item := self.menu_recent_items():
            self.open_text_file(recent_item.value)

        if menu_item("Save", shortcut="Ctrl+S", enabled=is_selected_text):
            self._save_file_popup.show()
        if menu_item("Save as ...", enabled=is_selected_text):
            self._save_as_file_popup.show()

        imgui.separator()
        if menu_item("Close file", enabled=is_selected_text):
            if self._current_key is not None:
                self.close_text(self._current_key)

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

    def on_tabs_menu(self) -> None:
        for item in self.ordered_texts:
            if menu_item(item.label):
                self._force_select = item.key
                item.opened = True

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                self.preprocess_open_runner()
                self.do_editor_tabs()

        self._popups.do_process()

    def preprocess_open_runner(self) -> None:
        if self._open_runner.running:
            return

        if self._open_runner.result is None:
            # If there are files left in the queue to open, run the runner.
            if self._open_file_queue:
                self.open_text_file(self._open_file_queue.popleft())
            return

        result = self._open_runner.result
        assert isinstance(result, _TextOpenResult)

        path = result.path
        encoding = result.encoding
        errors = result.errors
        text = result.text

        self.add_recent_item(path)

        if text_items := self.manager.find_with_path(path):
            for text_item in text_items:
                text_item.encoding = encoding
                text_item.errors = errors
                self.add_editor(text_item, text)
        else:
            _, text_item = self.add_new_text(path)
            self.add_editor(text_item, text)

        self._open_runner.clear()

    def add_editor(self, item: TextItem, content: str, *, no_select=False) -> None:
        text_editor = self._editors.get(item.key)
        if text_editor is None:
            text_editor = TextEditor(item)
            self._editors[item.key] = text_editor

        assert isinstance(text_editor, TextEditor)
        text_editor.set_text(content)

        if not no_select:
            self._force_select = item.key

    def do_editor_tabs(self) -> None:
        if imgui.begin_tab_bar("EditorTab", self.TAB_FLAGS):
            remove_keys = list()

            try:
                for item in self.manager.ordered_values(self.tabs_order):
                    flags = 0

                    if self._force_select == item.key:
                        flags |= SET_SELECTED
                        self._force_select = None

                    tab_result = begin_tab_item(item.label, opened=True, flags=flags)

                    if not tab_result.opened_state:
                        remove_keys.append(item.key)

                    if tab_result.selected:
                        self._current_key = item.key
                        try:
                            if text_editor := self._editors.get(item.key):
                                text_editor.do_process()
                        finally:
                            end_tab_item()

                if imgui.tab_item_button("+", TRAILING):
                    self.add_new_text()
            finally:
                imgui.end_tab_bar()

                for remove_key in remove_keys:
                    self.close_text(remove_key)
