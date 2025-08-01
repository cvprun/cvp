# -*- coding: utf-8 -*-

import os
from typing import BinaryIO, Optional

from cvp.paths.types import PathLike


def open_file_with_readonly_binary(path: PathLike) -> BinaryIO:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Not found regular file: '{path!r}'")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Not readable file: '{path!r}'")

    return open(path, "rb")


def close_binary_io(f: Optional[BinaryIO]) -> None:
    if f is not None:
        f.close()
