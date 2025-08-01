# -*- coding: utf-8 -*-

import os
from abc import ABC
from os import PathLike
from pathlib import Path
from typing import BinaryIO, Optional, Union
from weakref import finalize

from cvp.buffers.lines.interface import LinesInterface
from cvp.buffers.lines.utils import close_binary_io, open_file_with_readonly_binary
from cvp.variables import DEFAULT_STRING_ENCODING, DEFAULT_STRING_ERRORS


class LinesBase(LinesInterface, ABC):
    _file: Optional[BinaryIO]
    _finalizer: Optional[finalize]

    def __init__(
        self,
        path: Union[str, PathLike[str]],
        encoding=DEFAULT_STRING_ENCODING,
        errors=DEFAULT_STRING_ERRORS,
    ):
        self._path = Path(path)
        self._encoding = encoding
        self._errors = errors
        self._cursor = 0
        self._file = None
        self._finalizer = None

    @property
    def path(self) -> Path:
        return self._path

    @property
    def pathname(self) -> str:
        return str(self._path)

    @property
    def encoding(self) -> str:
        return self._encoding

    @property
    def errors(self) -> str:
        return self._errors

    @property
    def cursor(self) -> int:
        return self._cursor

    @property
    def closed(self):
        if self._file is not None:
            return self._file.closed
        else:
            return False

    def open(self) -> None:
        assert self._file is None
        assert self._finalizer is None
        self._file = open_file_with_readonly_binary(self._path)
        self._finalizer = finalize(self, close_binary_io, self._file)

    def close(self) -> None:
        assert self._file is not None
        assert self._finalizer is not None

        if self._finalizer.detach():
            close_binary_io(self._file)

        self._file = None
        self._finalizer = None

    def get_filesize(self) -> int:
        if not os.path.isfile(self._path):
            raise FileNotFoundError(f"Not found regular file: '{self.pathname}'")
        if not os.access(self._path, os.R_OK):
            raise PermissionError(f"Not readable file: '{self.pathname}'")

        return os.path.getsize(self._path)

    def update_safe(self) -> int:
        size = self.get_filesize()
        if size <= self._cursor:
            return 0

        if self.closed:
            self.open()

        return self.update_to_index(size)

    def update(self) -> int:
        return self.update_to_index(self.get_filesize())

    def update_to_index(self, index: int) -> int:
        if self.closed:
            raise ValueError("The file is closed")

        if index < self._cursor:
            raise ValueError("'index' must be greater than 'cursor'")

        if self._cursor == index:
            return 0

        size = index - self._cursor
        assert 0 < size
        assert self._file is not None
        data = self._file.read(size)
        self.write(str(data, encoding=self._encoding, errors=self._errors))
        self._cursor = index
        return size

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
