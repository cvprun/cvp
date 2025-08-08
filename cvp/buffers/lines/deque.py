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
    NOT_FOUND_INDEX,
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
        """
        Do not implement this by recursively calling `self.write()` method.
        Writing very large text may cause a `RecursionError`.
        """

        if not text:
            return

        remain_text = text

        while remain_text:
            index = remain_text.find(self._newline)
            if index == NOT_FOUND_INDEX:
                if self._lines:
                    self._lines[-1] += remain_text
                else:
                    self._lines.append(remain_text)
                return

            assert 0 <= index
            prefix_text = remain_text[:index]
            if self._lines:
                self._lines[-1] += prefix_text
            else:
                self._lines.append(prefix_text)

            self._lines.append(str())  # Add empty text at the newline position

            remain_begin = index + len(self._newline)
            remain_text = remain_text[remain_begin:]
