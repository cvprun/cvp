# -*- coding: utf-8 -*-

from collections import deque
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Handler, LogRecord
from typing import Callable, Deque, NamedTuple
from weakref import finalize

import imgui

from cvp.imgui.begin_child import begin_child
from cvp.imgui.checkbox import checkbox
from cvp.imgui.combo import combo
from cvp.logging.logging import (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
    SEVERITY_NAME_WARNING,
    convert_level_number,
)
from cvp.logging.logging import flow_logger as logger
from cvp.patterns.delta import Delta
from cvp.renderer.context import RendererContext
from cvp.types.colors import RGBA
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.canvases import Canvases

LEVEL_NAMES = [
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
]


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


class LogsTab(TabItem[Canvases]):
    _records: Deque[_LineRecord]

    def __init__(self, context: RendererContext):
        super().__init__(context, "Logs")
        assert 1 <= self.context.config.flow_aui.logs.lines
        self._mouse_wheel = Delta.from_single_value(0.0)
        self._records = deque(maxlen=self.context.config.flow_aui.logs.lines)
        self._handler = _LoggingHandler(self.on_logging)
        logger.addHandler(self._handler)
        self._finalizer = finalize(self, _unregister_handler, self._handler)

    @property
    def filter(self) -> str:
        return self.context.config.flow_aui.logs.filter

    @filter.setter
    def filter(self, value: str) -> None:
        self.context.config.flow_aui.logs.filter = value

    @property
    def autoscroll(self) -> bool:
        return self.context.config.flow_aui.logs.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self.context.config.flow_aui.logs.autoscroll = value

    @property
    def lines(self) -> int:
        return self.context.config.flow_aui.logs.lines

    @lines.setter
    def lines(self, value: int) -> None:
        self.context.config.flow_aui.logs.lines = value

    @property
    def level_index(self) -> int:
        return self.context.config.flow_aui.logs.level_index

    @level_index.setter
    def level_index(self, value: int) -> None:
        self.context.config.flow_aui.logs.level_index = value

    def get_level_number(self) -> int:
        return convert_level_number(LEVEL_NAMES[self.level_index])

    def get_level_color(self, level: int) -> RGBA:
        logging_config = self.context.config.flow_aui.logs
        if ERROR < level <= CRITICAL:
            return logging_config.critical_color
        elif WARNING < level <= ERROR:
            return logging_config.error_color
        elif INFO < level <= WARNING:
            return logging_config.warning_color
        elif DEBUG < level <= INFO:
            return logging_config.info_color
        elif NOTSET < level <= DEBUG:
            return logging_config.debug_color
        else:
            return imgui.get_style().colors[imgui.COLOR_TEXT]

    def on_logging(self, record: LogRecord, message: str) -> None:
        self._records.append(_LineRecord(record.levelno, record.levelname, message))

    def update_records_maxlen(self, maxlen: int) -> None:
        new_lines = type(self._records)(maxlen=maxlen)
        new_lines.extend(self._records)
        self._records = new_lines

    @override
    def on_process(self) -> None:
        if self._records.maxlen != self.lines:
            self.update_records_maxlen(self.lines)

        self.autoscroll = checkbox("Autoscroll", self.autoscroll)[1]

        imgui.same_line()
        max_width = imgui.calc_text_size(SEVERITY_NAME_CRITICAL)[0]
        padding = imgui.get_style().item_spacing[0] * 2
        dropdown_width = 20.0
        imgui.set_next_item_width(max_width + dropdown_width + padding)
        if level_result := combo("##Levels", self.level_index, LEVEL_NAMES):
            self.level_index = level_result.value

        imgui.same_line()
        imgui.set_next_item_width(-1)
        self.filter = imgui.input_text_with_hint("##Filter", "Filter", self.filter)[1]

        imgui.separator()

        bottom_spacing = imgui.get_style().item_spacing.y
        with begin_child("##Logging", 0, -bottom_spacing, border=False):
            if imgui.is_window_hovered(imgui.HOVERED_ROOT_AND_CHILD_WINDOWS):
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

            filter_level = self.get_level_number()

            for line in self._records:
                if line.level < filter_level:
                    continue
                if line.message.find(self.filter) == -1:
                    continue

                color = self.get_level_color(line.level)
                imgui.text_colored(f"[{line.levelname}] {line.message}", *color)

            if self.autoscroll:
                imgui.set_scroll_here_y(1.0)
