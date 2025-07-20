# -*- coding: utf-8 -*-

import os
from typing import Final, Optional

from psutil import virtual_memory

from cvp.filesystem.types import PathLike
from cvp.units import byte

SMALL_FILE_SIZE_THRESHOLD: Final[int] = byte.BYTES_1MB
MEDIUM_FILE_SIZE_THRESHOLD: Final[int] = byte.BYTES_100MB
LARGE_FILE_SIZE_THRESHOLD: Final[int] = byte.BYTES_1GB


def get_adaptive_chunk_size(path: PathLike) -> int:
    size = os.path.getsize(path)

    if size < SMALL_FILE_SIZE_THRESHOLD:
        return byte.BYTES_8KB
    elif size < MEDIUM_FILE_SIZE_THRESHOLD:
        return byte.BYTES_64KB
    elif size < LARGE_FILE_SIZE_THRESHOLD:
        return byte.BYTES_256KB
    else:
        return byte.BYTES_1MB


def get_block_size(path: PathLike) -> int:
    """
    'Preferred' blocksize for efficient file system I/O.
    Writing to a file in smaller chunks may cause an inefficient read-modify-rewrite.
    """
    return os.stat(path).st_blksize


def get_memory_based_chunk_size() -> int:
    """Get chunk size based on available memory"""

    # Use a certain percentage of available memory
    available_memory_bytes = virtual_memory().available

    # 1% of available memory or maximum 10MB
    chunk_size = min(available_memory_bytes // 100, byte.BYTES_10MB)

    # Ensure minimum 8KB
    return max(chunk_size, byte.BYTES_8KB)


def get_optimal_read_size(path: Optional[PathLike] = None) -> int:
    if path is not None and os.path.exists(path):
        try:
            return get_block_size(path)
        except:  # noqa
            pass

        try:
            return get_adaptive_chunk_size(path)
        except:  # noqa
            pass

    return get_memory_based_chunk_size()


def get_pipe_buf(path: PathLike) -> int:
    """Maximum number of bytes guaranteed to be atomic when written to a pipe."""
    return os.pathconf(path, "PC_PIPE_BUF")  # Availability: Unix.
