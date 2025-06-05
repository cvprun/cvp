# -*- coding: utf-8 -*-

from logging import Logger, LogRecord, getLogger
from typing import Deque, Optional, Union
from weakref import finalize

from imgui_bundle import imgui

from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.checkbox import checkbox
from cvp.imgui.combo import combo
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags import color_var
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.text_colored import text_colored
from cvp.logging.handlers.callable import CallableHandler
from cvp.logging.logging import (
    SEVERITY_NAME_CRITICAL,
    UNIQUE_LEVEL_NAMES,
    convert_level_number,
)
from cvp.logging.records.formatted import FormattedLogRecord
from cvp.logging.styles import GuiLoggingStyle
from cvp.types.colors import RGBA
from cvp.values.delta import DeltaValue


def _unregister_handler(logger: Logger, handler: CallableHandler) -> None:
    logger.removeHandler(handler)


class LoggingMultiline:
    def __init__(
        self,
        logger: Optional[Union[str, Logger]] = None,
        options: Optional[GuiLoggingStyle] = None,
    ):
        if logger is None:
            self.logger = getLogger()
        elif isinstance(logger, Logger):
            self.logger = logger
        else:
            assert isinstance(logger, str)
            self.logger = getLogger(logger)

        self.options = options if options else GuiLoggingStyle()
        self.mouse_wheel = DeltaValue.from_single_value(0.0)
        self.records = Deque[FormattedLogRecord](maxlen=self.options.lines)
        self.handler = CallableHandler(self.on_logging)
        self.logger.addHandler(self.handler)

        self._finalizer = finalize(
            self,
            _unregister_handler,
            self.logger,
            self.handler,
        )

    def on_logging(self, record: LogRecord, formatted_message: str) -> None:
        self.records.append(FormattedLogRecord.from_log(record, formatted_message))

    @property
    def filter(self) -> str:
        return self.options.filter

    @filter.setter
    def filter(self, value: str) -> None:
        self.options.filter = value

    @property
    def autoscroll(self) -> bool:
        return self.options.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self.options.autoscroll = value

    @property
    def lines(self) -> int:
        return self.options.lines

    @lines.setter
    def lines(self, value: int) -> None:
        self.options.lines = value

    @property
    def level_index(self) -> int:
        return self.options.level_index

    @level_index.setter
    def level_index(self, value: int) -> None:
        self.options.level_index = value

    @property
    def default_text_color(self) -> RGBA:
        vec4 = imgui.get_style().color_(color_var.TEXT)
        return vec4.x, vec4.y, vec4.z, vec4.w

    def get_level_number(self) -> int:
        return convert_level_number(UNIQUE_LEVEL_NAMES[self.level_index])

    def get_level_color(self, level: int) -> RGBA:
        return self.options.get_level_color(level, self.default_text_color)

    def update_records_maxlen(self, maxlen: int) -> None:
        new_lines = type(self.records)(maxlen=maxlen)
        new_lines.extend(self.records)
        self.records = new_lines

    def do_process(self, *, use_mouse_wheel=False):
        with begin_child_context(type(self).__name__):
            with begin_child_context("Toolbar", child_flags=AUTO_RESIZE_Y):
                self.do_toolbar_process()
            with begin_child_context("Logging"):
                self.do_logging_process(use_mouse_wheel=use_mouse_wheel)

    def do_toolbar_process(self) -> None:
        if self.records.maxlen != self.lines:
            self.update_records_maxlen(self.lines)

        self.autoscroll = checkbox("Autoscroll", self.autoscroll)[1]

        imgui.same_line()
        max_width = imgui.calc_text_size(SEVERITY_NAME_CRITICAL)[0]
        padding = imgui.get_style().item_spacing[0] * 2
        dropdown_width = 20.0
        imgui.set_next_item_width(max_width + dropdown_width + padding)
        if level_result := combo("##Levels", self.level_index, UNIQUE_LEVEL_NAMES):
            self.level_index = level_result.value

        imgui.same_line()
        imgui.set_next_item_width(FIT_WIDTH)
        self.filter = imgui.input_text_with_hint("##Filter", "Filter", self.filter)[1]

    def do_logging_process(self, *, use_mouse_wheel=False) -> None:
        if use_mouse_wheel and imgui.is_window_hovered(ROOT_AND_CHILD_WINDOWS):
            if self.mouse_wheel.update(imgui.get_io().mouse_wheel):
                if 0 < self.mouse_wheel.value:
                    # Drag Up
                    if imgui.get_scroll_y() < imgui.get_scroll_max_y():
                        self.autoscroll = False
                elif self.mouse_wheel.value < 0:
                    # Drag Down
                    if imgui.get_scroll_max_y() <= imgui.get_scroll_y():
                        self.autoscroll = True
                else:
                    assert 0 == self.mouse_wheel.value

        filter_level = self.get_level_number()

        for line in self.records:
            if line.levelno < filter_level:
                continue
            if line.formatted_message.find(self.filter) == -1:
                continue

            color = self.get_level_color(line.levelno)
            text_colored(line.formatted_message, color)

        if self.autoscroll:
            imgui.set_scroll_here_y(1.0)
