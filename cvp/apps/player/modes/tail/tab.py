# -*- coding: utf-8 -*-

from typing import Iterable, Optional

from cvp.buffers.lines.deque import LinesDeque
from cvp.config.sections.tail import TailConfig
from cvp.imgui.widgets.input_terminal import InputTerminal
from cvp.values.interval import IntervalTimer
from cvp.variables import (
    DEFAULT_STRING_ENCODING,
    DEFAULT_STRING_ERRORS,
    DEFAULT_STRING_NEWLINE,
)
from cvp.watchdog.item import WatchdogKey


class TailTab:
    def __init__(
        self,
        path: str,
        encoding=DEFAULT_STRING_ENCODING,
        errors=DEFAULT_STRING_ERRORS,
        maxlen: Optional[int] = None,
        newline=DEFAULT_STRING_NEWLINE,
        initial_lines: Optional[Iterable[str]] = None,
        autoscroll=True,
        show_lineno=False,
        show_whitespace=False,
        interval: Optional[float] = None,
        latest_time: Optional[float] = None,
        watchdog_key: Optional[WatchdogKey] = None,
    ):
        self.canvas = InputTerminal(
            label=path,
            readonly=True,
            autoscroll=autoscroll,
            show_lineno=show_lineno,
            show_whitespace=show_whitespace,
        )
        self.buffer = LinesDeque(
            path=path,
            encoding=encoding,
            errors=errors,
            maxlen=maxlen,
            newline=newline,
            initial_lines=initial_lines,
        )
        self.interval = IntervalTimer(interval=interval, latest_time=latest_time)
        self.watchdog_key = watchdog_key

    @property
    def path(self) -> str:
        assert isinstance(self.buffer.path, str)
        return self.buffer.path

    @property
    def pathname(self) -> str:
        assert isinstance(self.buffer.pathname, str)
        return self.buffer.pathname

    @property
    def lines(self):
        return self.buffer.lines

    @property
    def autoscroll(self) -> bool:
        return self.canvas.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self.canvas.autoscroll = value

    @property
    def show_lineno(self) -> bool:
        return self.canvas.show_lineno

    @show_lineno.setter
    def show_lineno(self, value: bool) -> None:
        self.canvas.show_lineno = value

    @property
    def show_whitespace(self) -> bool:
        return self.canvas.show_whitespace

    @show_whitespace.setter
    def show_whitespace(self, value: bool) -> None:
        self.canvas.show_whitespace = value

    @property
    def newline(self) -> str:
        return self.buffer.newline

    @newline.setter
    def newline(self, value: str) -> None:
        self.buffer.newline = value

    @classmethod
    def from_config(
        cls,
        path: str,
        config: TailConfig,
        *,
        watchdog_key: Optional[WatchdogKey] = None,
    ):
        return cls(
            path,
            encoding=config.encoding,
            errors=config.errors,
            maxlen=config.maxlen,
            newline=config.newline,
            autoscroll=config.autoscroll,
            show_lineno=config.show_lineno,
            show_whitespace=config.show_whitespace,
            interval=config.manually_update_interval,
            watchdog_key=watchdog_key,
        )

    def update_buffer(self, *, force=False) -> bool:
        if force or self.interval.update():
            self.buffer.update_safe()
            return True
        else:
            return False

    def do_process(self, *, debug=False) -> None:
        self.canvas.do_process(self.buffer.lines, debug=debug)
