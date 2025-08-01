# -*- coding: utf-8 -*-

from os import PathLike
from typing import Optional, Union

from cvp.buffers.lines import LinesBuffer
from cvp.types.override import override
from cvp.variables import (
    DEFAULT_STRING_ENCODING,
    DEFAULT_STRING_ERRORS,
    DEFAULT_STRING_LINE_CONTINUATION_CHARACTER,
    DEFAULT_STRING_NEWLINE,
)


class StreamBuffer(LinesBuffer):
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
        super().__init__(
            path=path,
            encoding=encoding,
            errors=errors,
            maxsize=maxsize,
            newline_size=newline_size,
            newline=newline,
            line_continuation_character=line_continuation_character,
        )
        self.writable = open(path, "wb")
        try:
            self.open()
        except:  # noqa
            self.writable.close()

    def writable_fileno(self) -> int:
        return self.writable.fileno()

    def readable_fileno(self) -> Optional[int]:
        return self._file.fileno() if self._file is not None else None

    @override
    def close(self) -> None:
        super().close()
        self.writable.close()


class StreamBufferPair:
    def __init__(
        self,
        stdout: Optional[StreamBuffer] = None,
        stderr: Optional[StreamBuffer] = None,
    ):
        self.stdout = stdout
        self.stderr = stderr

    @classmethod
    def from_args(
        cls,
        stdout: Optional[Union[str, PathLike[str]]] = None,
        stderr: Optional[Union[str, PathLike[str]]] = None,
        encoding=DEFAULT_STRING_ENCODING,
        errors=DEFAULT_STRING_ERRORS,
        maxsize: Optional[int] = None,
        newline_size: Optional[int] = None,
        newline=DEFAULT_STRING_NEWLINE,
        line_continuation_character=DEFAULT_STRING_LINE_CONTINUATION_CHARACTER,
    ):
        if stdout:
            stdout_buffer = StreamBuffer(
                path=stdout,
                encoding=encoding,
                errors=errors,
                maxsize=maxsize,
                newline_size=newline_size,
                newline=newline,
                line_continuation_character=line_continuation_character,
            )
        else:
            stdout_buffer = None

        if stderr:
            stderr_buffer = StreamBuffer(
                path=stderr,
                encoding=encoding,
                errors=errors,
                maxsize=maxsize,
                newline_size=newline_size,
                newline=newline,
                line_continuation_character=line_continuation_character,
            )
        else:
            stderr_buffer = None

        return cls(stdout_buffer, stderr_buffer)

    def close(self):
        if self.stdout is not None:
            self.stdout.close()
        if self.stderr is not None:
            self.stderr.close()
