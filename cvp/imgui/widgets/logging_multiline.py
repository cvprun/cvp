# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    Handler,
    Logger,
    LogRecord,
    getLogger,
)
from typing import Callable, Deque, Final, NamedTuple, Optional, Sequence, Union
from weakref import finalize

from imgui_bundle import imgui

from cvp.imgui.checkbox import checkbox
from cvp.imgui.combo import combo
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags import color_var
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.text_colored import text_colored
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
from cvp.palette.basic import BLUE, LIME, MAROON, RED, YELLOW
from cvp.patterns.delta import Delta
from cvp.types.colors import RGBA
from cvp.types.override import override

LEVEL_NAMES: Final[Sequence[str]] = (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)

DEFAULT_LEVEL_INDEX: Final[int] = LEVEL_NAMES.index(SEVERITY_NAME_NOTSET)
DEFAULT_LINES: Final[int] = 1_000


@dataclass
class LoggingMultilineOptions:
    level_index: int = DEFAULT_LEVEL_INDEX

    lines: int = DEFAULT_LINES
    autoscroll: bool = False
    filter: str = field(default_factory=str)

    critical_color: RGBA = field(default_factory=lambda: (*MAROON, 1.0))
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    info_color: RGBA = field(default_factory=lambda: (*LIME, 1.0))
    debug_color: RGBA = field(default_factory=lambda: (*BLUE, 1.0))


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


def _unregister_handler(logger: Logger, handler: _LoggingHandler) -> None:
    logger.removeHandler(handler)


class LoggingMultiline:
    def __init__(
        self,
        label: str,
        logger: Optional[Union[str, Logger]] = None,
        options: Optional[LoggingMultilineOptions] = None,
    ):
        self._label = label
        self._options = options if options else LoggingMultilineOptions()

        if logger is None:
            self._logger = getLogger()
        elif isinstance(logger, Logger):
            self._logger = logger
        else:
            assert isinstance(logger, str)
            self._logger = getLogger(logger)

        self._mouse_wheel = Delta.from_single_value(0.0)
        self._records = Deque[_LineRecord](maxlen=self._options.lines)
        self._handler = _LoggingHandler(self.on_logging)

        self._logger.addHandler(self._handler)
        self._finalizer = finalize(
            self,
            _unregister_handler,
            self._logger,
            self._handler,
        )

    def on_logging(self, record: LogRecord, message: str) -> None:
        self._records.append(_LineRecord(record.levelno, record.levelname, message))

    @property
    def filter(self) -> str:
        return self._options.filter

    @filter.setter
    def filter(self, value: str) -> None:
        self._options.filter = value

    @property
    def autoscroll(self) -> bool:
        return self._options.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self._options.autoscroll = value

    @property
    def lines(self) -> int:
        return self._options.lines

    @lines.setter
    def lines(self, value: int) -> None:
        self._options.lines = value

    @property
    def level_index(self) -> int:
        return self._options.level_index

    @level_index.setter
    def level_index(self, value: int) -> None:
        self._options.level_index = value

    def get_level_number(self) -> int:
        return convert_level_number(LEVEL_NAMES[self.level_index])

    def get_level_color(self, level: int) -> RGBA:
        if ERROR < level <= CRITICAL:
            return self._options.critical_color
        elif WARNING < level <= ERROR:
            return self._options.error_color
        elif INFO < level <= WARNING:
            return self._options.warning_color
        elif DEBUG < level <= INFO:
            return self._options.info_color
        elif NOTSET < level <= DEBUG:
            return self._options.debug_color
        else:
            vec4 = imgui.get_style().color_(color_var.TEXT)
            return vec4.x, vec4.y, vec4.z, vec4.w

    def update_records_maxlen(self, maxlen: int) -> None:
        new_lines = type(self._records)(maxlen=maxlen)
        new_lines.extend(self._records)
        self._records = new_lines

    def do_toolbar_process(self) -> None:
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
        imgui.set_next_item_width(FIT_WIDTH)
        self.filter = imgui.input_text_with_hint("##Filter", "Filter", self.filter)[1]

    def do_logging_process(self) -> None:
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

        filter_level = self.get_level_number()

        for line in self._records:
            if line.level < filter_level:
                continue
            if line.message.find(self.filter) == -1:
                continue

            color = self.get_level_color(line.level)
            text_colored(f"[{line.levelname}] {line.message}", color)

        if self.autoscroll:
            imgui.set_scroll_here_y(1.0)
