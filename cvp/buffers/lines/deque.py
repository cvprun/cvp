# -*- coding: utf-8 -*-

from collections import deque
from io import StringIO
from os import PathLike
from typing import Deque, Iterable, Optional, Union

from overrides import override

from cvp.buffers.lines.base import LinesBase
from cvp.variables import (
    DEFAULT_STRING_ENCODING,
    DEFAULT_STRING_ERRORS,
    DEFAULT_STRING_NEWLINE,
)


class LinesDeque(LinesBase):
    _lines: Deque[str]

    def __init__(
        self,
        path: Union[str, PathLike[str]],
        encoding=DEFAULT_STRING_ENCODING,
        errors=DEFAULT_STRING_ERRORS,
        maxlen: Optional[int] = None,
        newline=DEFAULT_STRING_NEWLINE,
        initial_lines: Optional[Iterable[str]] = None,
    ):
        super().__init__(path=path, encoding=encoding, errors=errors)
        self._lines = deque(initial_lines or (), maxlen=maxlen)
        self._newline = newline

    @property
    def lines(self):
        return self._lines

    @property
    def newline(self) -> str:
        return self._newline

    @newline.setter
    def newline(self, value: str) -> None:
        self._newline = value

    @override
    def getvalue(self) -> str:
        if len(self._lines) == 0:
            return str()

        if len(self._lines) == 1:
            return self._lines[0]

        assert len(self._lines) >= 2
        buffer = StringIO()
        buffer.write(self._lines[0])

        for i in range(1, len(self._lines)):
            buffer.write(self._newline)
            buffer.write(self._lines[i])

        return buffer.getvalue()

    @override
    def write(self, text: str) -> None:
        if not text:
            return

        index = text.find(self._newline)
        if 0 <= index:
            prefix_text = text[:index]
            if self._lines:
                self._lines[-1] += prefix_text
            else:
                self._lines.append(prefix_text)

            self._lines.append(str())  # Add empty text at the newline position

            remain_begin = index + len(self._newline)
            remain_text = text[remain_begin:]
            self.write(remain_text)
        else:
            assert index == -1
            if self._lines:
                self._lines[-1] += text
            else:
                self._lines.append(text)
