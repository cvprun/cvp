# -*- coding: utf-8 -*-

from os import PathLike
from typing import Optional, Union

from overrides import override

from cvp.buffers.lines.base import LinesBase
from cvp.variables import (
    DEFAULT_STRING_ENCODING,
    DEFAULT_STRING_ERRORS,
    DEFAULT_STRING_LINE_CONTINUATION_CHARACTER,
    DEFAULT_STRING_NEWLINE,
)


class LinesBuffer(LinesBase):
    def __init__(
        self,
        path: Union[str, PathLike[str]],
        encoding=DEFAULT_STRING_ENCODING,
        errors=DEFAULT_STRING_ERRORS,
        maxsize: Optional[int] = None,
        newline_size: Optional[int] = None,
        newline=DEFAULT_STRING_NEWLINE,
        line_continuation_character=DEFAULT_STRING_LINE_CONTINUATION_CHARACTER,
    ):
        super().__init__(path=path, encoding=encoding, errors=errors)
        self._buffer = str()
        self._maxsize = maxsize
        self._newline_size = newline_size
        self._newline = newline
        self._line_continuation_character = line_continuation_character

    @staticmethod
    def merge(buffer: str, text: str, maxsize: Optional[int] = None) -> str:
        if maxsize is not None:
            overflow_size = len(buffer) + len(text) - maxsize
            if 0 < overflow_size:
                result = buffer[overflow_size:] + text
            else:
                result = buffer + text
            assert len(result) <= maxsize
            return result
        else:
            return buffer + text

    @property
    def pseudo_suffix(self) -> str:
        return self._line_continuation_character + self._newline

    def enqueue_text(self, text: str):
        self._buffer = self.merge(self._buffer, text, self._maxsize)

    @override
    def getvalue(self) -> str:
        return self._buffer

    @override
    def write(self, text: str) -> None:
        if not text:
            return

        if self._newline_size is None:
            self.enqueue_text(text)
            return

        last_line_begin = self._buffer.rfind(self._newline)
        if last_line_begin == -1:
            last_line_size = len(self._buffer)
        else:
            last_line_size = len(self._buffer) - last_line_begin - 1

        remain_line_size = self._newline_size - last_line_size
        assert 0 <= remain_line_size

        if len(text) <= remain_line_size:
            self.enqueue_text(text)
            return

        newline_text_index = text.find(self._newline)
        if newline_text_index == -1:
            text1 = text[:remain_line_size] + self.pseudo_suffix
            text2 = text[remain_line_size:]
            self.enqueue_text(text1)
            self.write(text2)
            return

        additional_line_size = newline_text_index + 1
        text1 = text[:additional_line_size]
        text2 = text[additional_line_size:]

        if additional_line_size <= remain_line_size:
            self.enqueue_text(text1)
        else:
            text1_1 = text1[:remain_line_size] + self.pseudo_suffix
            text1_2 = text1[remain_line_size:]
            self.enqueue_text(text1_1)
            self.write(text1_2)

        self.write(text2)
