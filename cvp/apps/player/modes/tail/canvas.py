# -*- coding: utf-8 -*-

from typing import Iterable, Optional

from cvp.buffers.lines.deque import LinesDeque
from cvp.config.sections.tail import TailConfig
from cvp.imgui.widgets.terminal_canvas import TerminalCanvas
from cvp.variables import (
    DEFAULT_STRING_ENCODING,
    DEFAULT_STRING_ERRORS,
    DEFAULT_STRING_NEWLINE,
)


class TailCanvas:
    def __init__(
        self,
        path: str,
        encoding=DEFAULT_STRING_ENCODING,
        errors=DEFAULT_STRING_ERRORS,
        maxlen: Optional[int] = None,
        newline=DEFAULT_STRING_NEWLINE,
        initial_lines: Optional[Iterable[str]] = None,
        autoscroll=True,
    ):
        self.canvas = TerminalCanvas(label=path, autoscroll=autoscroll)
        self.buffer = LinesDeque(
            path=path,
            encoding=encoding,
            errors=errors,
            maxlen=maxlen,
            newline=newline,
            initial_lines=initial_lines,
        )

    @classmethod
    def from_config(cls, path: str, config: TailConfig):
        return cls(
            path,
            encoding=config.encoding,
            errors=config.errors,
            maxlen=config.maxlen,
            newline=config.newline,
            autoscroll=config.autoscroll,
        )

    def do_process(self) -> None:
        self.buffer.update_safe()
        self.canvas.do_process(self.buffer.lines)
