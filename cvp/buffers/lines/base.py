# -*- coding: utf-8 -*-

import os
from abc import ABC
from typing import BinaryIO, Optional
from weakref import finalize

from cvp.buffers.lines.interface import LinesInterface
from cvp.buffers.lines.utils import close_binary_io, open_file_with_readonly_binary
from cvp.paths.types import PathLike
from cvp.variables import DEFAULT_STRING_ENCODING, DEFAULT_STRING_ERRORS


class LinesBase(LinesInterface, ABC):
    _file: Optional[BinaryIO]
    _finalizer: Optional[finalize]

    def __init__(
        self,
        path: PathLike,
        encoding=DEFAULT_STRING_ENCODING,
        errors=DEFAULT_STRING_ERRORS,
    ):
        self._path = path
        self._encoding = encoding
        self._errors = errors
        self._file = None
        self._finalizer = None

    @property
    def path(self):
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
    def closed(self) -> bool:
        if self._file is not None:
            return self._file.closed
        else:
            return True

    @property
    def file(self) -> BinaryIO:
        if self.closed:
            raise ValueError("The file is closed")

        assert self._file is not None
        return self._file

    @property
    def cursor(self) -> int:
        return self.file.tell()

    @property
    def fd(self) -> int:
        """File Description"""
        return self.file.fileno()

    @property
    def mode(self) -> str:
        return self.file.mode

    @property
    def name(self) -> str:
        return self.file.name

    def flush(self) -> None:
        self.file.flush()

    def isatty(self) -> bool:
        return self.file.isatty()

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

    def get_filesize_with_path(self) -> int:
        if not os.path.isfile(self._path):
            raise FileNotFoundError(f"Not found regular file: '{self.pathname}'")
        if not os.access(self._path, os.R_OK):
            raise PermissionError(f"Not readable file: '{self.pathname}'")

        return os.path.getsize(self._path)

    def as_fstat(self):
        if self.closed:
            raise ValueError("The file is closed")

        assert self._file is not None
        return os.fstat(self._file.fileno())

    def get_filesize_with_fstat(self) -> int:
        return self.as_fstat().st_size

    @property
    def filesize(self) -> int:
        if self.closed:
            return self.get_filesize_with_path()
        else:
            return self.get_filesize_with_fstat()

    def update_safe(self) -> int:
        if self.closed:
            self.open()

        assert not self.closed

        filesize = self.filesize
        cursor = self.cursor

        if filesize == cursor:
            return 0
        elif filesize < cursor:
            self.seek_set(filesize)
            return (cursor - filesize) * -1
        else:
            assert cursor < filesize
            return self.update_to_offset(filesize)

    def update(self) -> int:
        return self.update_to_offset(self.filesize)

    def update_to_offset(self, offset: int) -> int:
        if self.closed:
            raise ValueError("The file is closed")

        cursor = self.cursor
        if offset < cursor:
            raise ValueError("'offset' must be greater than 'cursor'")

        if offset == cursor:
            return 0

        size = offset - cursor
        assert 0 < size
        assert self._file is not None
        data = self._file.read(size)
        self.write(str(data, encoding=self._encoding, errors=self._errors))
        return len(data)

    def seek_set(self, offset: int) -> None:
        self.file.seek(offset, os.SEEK_SET)

    def seek_current(self, offset: int) -> None:
        self.file.seek(offset, os.SEEK_CUR)

    def seek_end(self, offset: int) -> None:
        self.file.seek(offset, os.SEEK_END)

    def seek_begin(self) -> None:
        self.seek_set(0)

    def seek_eof(self) -> None:
        self.seek_end(0)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
