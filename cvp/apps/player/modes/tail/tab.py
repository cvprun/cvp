# -*- coding: utf-8 -*-

from typing import Iterable, Optional

from cvp.buffers.lines.deque import LinesDeque
from cvp.config.sections.tail import TailConfig
from cvp.imgui.widgets.input_terminal import InputTerminal
from cvp.variables import (
    DEFAULT_STRING_ENCODING,
    DEFAULT_STRING_ERRORS,
    DEFAULT_STRING_NEWLINE,
)


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
    ):
        self.canvas = InputTerminal(label=path, autoscroll=autoscroll)
        self.buffer = LinesDeque(
            path=path,
            encoding=encoding,
            errors=errors,
            maxlen=maxlen,
            newline=newline,
            initial_lines=initial_lines,
        )

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
    def newline(self) -> str:
        return self.buffer.newline

    @newline.setter
    def newline(self, value: str) -> None:
        self.buffer.newline = value

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

    def update_buffer(self) -> None:
        self.buffer.update_safe()

    def do_process(self) -> None:
        self.canvas.do_process(self.buffer.lines)
