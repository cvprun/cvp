# -*- coding: utf-8 -*-

from io import StringIO
from typing import Iterable, Optional

from cvp.buffers.lines.deque import LinesDeque
from cvp.config.sections.tail import TailConfig
from cvp.imgui.tooltip import tooltip_text_wrapped
from cvp.imgui.widgets.input_ansi_escape_text import InputAnsiEscapeText
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
        self.canvas = InputAnsiEscapeText(
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

    @property
    def selected_info(self) -> str:
        buffer = StringIO()
        buffer.write("Sel ")
        if sb := self.canvas.selected_begin:
            buffer.write(f"{sb.lineno}:{sb.column}")
            if se := self.canvas.selected_end:
                buffer.write(f"~{se.lineno}:{se.column}")
        else:
            buffer.write("None")
        return buffer.getvalue()

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
        if debug:
            tooltip_text_wrapped(self.as_unformatted_text())

    def as_unformatted_text(self) -> str:
        mx, my = self.canvas.mouse_pos
        cx, cy = self.canvas.cursor_pos
        csx, csy = self.canvas.cursor_screen_pos
        crw, crh = self.canvas.content_region_size
        terminal_coord_lineno = self.canvas.terminal_coord.lineno
        terminal_coord_column = self.canvas.terminal_coord.column
        tw, th = self.canvas.terminal_size
        return (
            f"Mouse pos: {mx:.02f}, {my:.02f}\n"
            f"Cursor pos: {cx:.02f}, {cy:.02f}\n"
            f"Cursor screen pos: {csx:.02f}, {csy:.02f}\n"
            f"Content region size: {crw:.02f}, {crh:.02f}\n"
            f"Terminal coord: {terminal_coord_column}x{terminal_coord_lineno}\n"
            f"Terminal size: {tw}x{th}\n"
        )
