# -*- coding: utf-8 -*-

from logging import Handler, LogRecord
from typing import Callable, Deque, Final, NamedTuple
from weakref import finalize

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import DOG
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.fit_size import FIT_SIZE, FIT_WIDTH
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS, RESIZE_X, RESIZE_Y
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS
from cvp.imgui.flags.table_column import WIDTH_STRETCH
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.logging.loggers import watchdog_logger as logger
from cvp.msgs.callbacks import MsgCallbacks
from cvp.msgs.msg import Msg
from cvp.msgs.msg_map import create_msg_map
from cvp.patterns.delta import Delta
from cvp.types.override import override
from cvp.watchdog.item import WatchdogItem, WatchdogKey


class _LoggingHandler(Handler):
    def __init__(self, callback: Callable[[LogRecord, str], None]):
        super().__init__()
        self._callback = callback

    @override
    def emit(self, record: LogRecord):
        self._callback(record, self.format(record))


class _LineRecord(NamedTuple):
    level: int
    levelname: str
    message: str


def _unregister_handler(handler: _LoggingHandler) -> None:
    logger.removeHandler(handler)


class WatchdogMode(BaseMode, MsgCallbacks):
    __cvp_mode_name__ = "Watchdog"
    __cvp_mode_icon__ = DOG

    _TOP_CHILD_FLAGS: Final[int] = RESIZE_Y

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _TABLE_COLUMNS: Final[int] = 8
    _TABLE_FLAGS: Final[int] = DEFAULT_TABLE_FLAGS

    def __init__(self, context: Context):
        super().__init__(context)
        self._stopping = False
        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove watchdog?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all watchdog?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )
        self._file_browser = OpenFilePopup(
            "Select file or directory",
            target=self.on_file_selected,
            mode=OpenFilePopup.Mode.select_file,
        )
        self._popups = PopupList(
            self._confirm_remove,
            self._confirm_clear,
            self._file_browser,
        )

        self.autoscroll = False
        self._mouse_wheel = Delta.from_single_value(0.0)
        self._maxlen = 100
        self._records = Deque[_LineRecord](maxlen=self._maxlen)
        self._handler = _LoggingHandler(self.on_logging)
        logger.addHandler(self._handler)
        self._finalizer = finalize(self, _unregister_handler, self._handler)
        self._msg_mapping = create_msg_map(self)

    def on_logging(self, record: LogRecord, message: str) -> None:
        self._records.append(_LineRecord(record.levelno, record.levelname, message))

    @property
    def success_color(self):
        return self.context.config.appearance.success_color

    @property
    def warning_color(self):
        return self.context.config.appearance.warning_color

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_success(self, text: str) -> None:
        imgui.text_colored(self.success_color, text)

    def text_warning(self, text: str) -> None:
        imgui.text_colored(self.warning_color, text)

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    @property
    def config(self):
        return self.context.config.watchdog

    @property
    def watchdogs(self):
        return self.context.watchdogs

    @property
    def selected_watchdog(self):
        return self.watchdogs.get(WatchdogKey(self.selected_submenu))

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        assert self._remove_candidate in self.watchdogs
        self.watchdogs.remove(self._remove_candidate)

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.watchdogs.remove_all()

    def on_file_selected(self, file: str) -> None:
        if not file:
            return

        selected_watchdog = self.selected_watchdog
        assert selected_watchdog is not None
        selected_watchdog.file = file

    @override
    def on_msg(self, msg: Msg) -> bool:
        if wrapper := self._msg_mapping.get(msg.mtype):
            return wrapper(msg)
        else:
            return False

    @override
    def on_file_moved(self, src: str, dest: str, isdir: bool):
        logger.info(f"{self.on_file_moved.__name__}({src=}, {dest=}, {isdir=})")

    @override
    def on_file_created(self, src: str, dest: str, isdir: bool):
        logger.info(f"{self.on_file_created.__name__}({src=}, {dest=}, {isdir=})")

    @override
    def on_file_deleted(self, src: str, dest: str, isdir: bool):
        logger.info(f"{self.on_file_deleted.__name__}({src=}, {dest=}, {isdir=})")

    @override
    def on_file_modified(self, src: str, dest: str, isdir: bool):
        logger.info(f"{self.on_file_modified.__name__}({src=}, {dest=}, {isdir=})")

    @override
    def on_file_closed(self, src: str, dest: str, isdir: bool):
        logger.info(f"{self.on_file_closed.__name__}({src=}, {dest=}, {isdir=})")

    @override
    def on_file_closed_no_write(self, src: str, dest: str, isdir: bool):
        method_name = self.on_file_closed_no_write.__name__
        logger.info(f"{method_name}({src=}, {dest=}, {isdir=})")

    @override
    def on_file_opened(self, src: str, dest: str, isdir: bool):
        logger.info(f"{self.on_file_opened.__name__}({src=}, {dest=}, {isdir=})")

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            half_height = imgui.get_content_region_avail().y / 2
            with begin_child_context(
                label="Top",
                size=(0, half_height),
                child_flags=self._TOP_CHILD_FLAGS,
            ):
                self.do_top_process()

            imgui.separator()

            with begin_child_context("Bottom"):
                with begin_child_context("BottomToolbar", child_flags=AUTO_RESIZE_Y):
                    self.do_bottom_toolbar_process()
                with begin_child_context("BottomLogging"):
                    self.do_bottom_logging_process()

        self._popups.do_process()

    def do_top_process(self):
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if button("Reload"):
                self.watchdogs.read_all_config_files()
            imgui.same_line()
            if button("Add"):
                self.watchdogs.add_watchdog()
            imgui.same_line()
            if button("Del", disabled=self.selected_submenu not in self.watchdogs):
                self._remove_candidate = self.selected_submenu
                self._confirm_remove.show()
            imgui.same_line()
            if button("Clear", disabled=not self.watchdogs):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for key, watchdog in self.watchdogs.items():
                        label = f"{watchdog.name}###{key}" if watchdog.name else key
                        selected = key == self.selected_submenu
                        if imgui.selectable(label, selected)[1]:
                            self.selected_submenu = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if selected_item := self.watchdogs.get(WatchdogKey(self.selected_submenu)):
                self.do_main_process(selected_item)
            else:
                text_centered("Please select a item")

    def do_main_process(self, item: WatchdogItem) -> None:
        input_text_disabled("UUID", item.uuid)
        has_watcher = item.has_watcher

        if item.managed:
            self.text_warning("This event is system-managed and cannot be modified")

        imgui.begin_disabled(has_watcher or item.managed)
        try:
            if name := input_text("Name", item.name):
                item.name = name.value

            if file := input_text("File", item.file):
                item.file = file.value
            if button("Browse"):
                self._file_browser.set_location(item.file)
                self._file_browser.show()

            if recursive := checkbox("Recursive", item.recursive):
                item.recursive = recursive.state
            hovered_tooltip_text("Recursively monitor paths")

            if enabled := checkbox("Enabled", item.enabled):
                item.enabled = enabled.state
            hovered_tooltip_text("Automatically starts when the program launches")

            imgui.text("Event Filters")

            with begin_child_context(
                label="##EventFiltersChild",
                size=(imgui.calc_item_width(), 0),
                child_flags=AUTO_RESIZE_Y | BORDERS,
            ):
                imgui.begin_table("EventFiltersTable", 3, outer_size=(FIT_WIDTH, 0))
                try:
                    imgui.table_setup_column("##Column1", WIDTH_STRETCH)
                    imgui.table_setup_column("##Column2", WIDTH_STRETCH)
                    imgui.table_setup_column("##Column3", WIDTH_STRETCH)

                    for event_filter in WatchdogItem.EVENT_FILTERS:
                        imgui.table_next_column()

                        filter_name = event_filter.__name__
                        has_filter = item.has_event_filter(event_filter)

                        if check_filter := checkbox(filter_name, has_filter):
                            if check_filter.state:
                                item.add_event_filter(event_filter)
                            else:
                                item.remove_event_filter(event_filter)
                finally:
                    imgui.end_table()
        finally:
            imgui.end_disabled()

        if button("Schedule", disabled=has_watcher):
            self.watchdogs.schedule(item.key)
        imgui.same_line()
        if button("Unschedule", disabled=not has_watcher):
            self.watchdogs.unschedule(item.key)

    def do_bottom_toolbar_process(self) -> None:
        running = self.watchdogs.is_alive()
        if not running:
            self._stopping = False

        if self._stopping:
            button("Start", disabled=True)
            imgui.same_line()
            button("Stop", disabled=True)
        else:
            if button("Start", disabled=running):
                self.watchdogs.start_safe()
            imgui.same_line()
            if button("Stop", disabled=not running):
                self.watchdogs.stop()
                self._stopping = True

        imgui.same_line()

        if self._stopping:
            self.text_warning("Stopping watchdog ...")
        elif running:
            self.text_success("Watchdog is running ...")
        else:
            self.text_error("Watchdog is idle")

    def do_bottom_logging_process(self) -> None:
        if imgui.is_window_hovered(ROOT_AND_CHILD_WINDOWS):
            if self._mouse_wheel.update(imgui.get_io().mouse_wheel):
                if 0 < self._mouse_wheel.value:
                    # Drag Up
                    if imgui.get_scroll_y() < imgui.get_scroll_max_y():
                        self.autoscroll = False
                elif self._mouse_wheel.value < 0:
                    # Drag Down
                    if imgui.get_scroll_max_y() <= imgui.get_scroll_y():
                        self.autoscroll = True
                else:
                    assert 0 == self._mouse_wheel.value

        for line in self._records:
            imgui.text(f"[{line.levelname}] {line.message}")

        if self.autoscroll:
            imgui.set_scroll_here_y(1.0)
