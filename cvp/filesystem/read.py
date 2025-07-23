# -*- coding: utf-8 -*-

import os
from io import StringIO
from logging import Logger
from typing import Optional

from cvp.concurrency.threading.progress_value import ProgressValue
from cvp.filesystem.conf import get_optimal_read_size


def read_progressive(
    path: str,
    encoding="utf-8",
    errors="strict",
    *,
    logger: Optional[Logger] = None,
    progress: Optional[ProgressValue] = None,
    chunk_size: Optional[int] = None,
) -> str:
    if logger is not None:
        logger.info(f"Starting progressive read of file: '{path}'")

    if not os.path.isfile(path):
        if logger is not None:
            logger.debug(f"File does not exist: '{path}'")
        return str()

    total_size = os.path.getsize(path)

    if logger is not None:
        logger.debug(f"Total file size to read: {total_size} bytes")

    if total_size < 0:
        return str()

    if chunk_size is None:
        chunk_size = get_optimal_read_size(path)
    assert isinstance(chunk_size, int)
    assert 1 <= chunk_size

    if logger is not None:
        logger.debug(f"Using chunk size: {chunk_size} bytes for reading file: '{path}'")

    if progress is not None:
        progress.set(0, limit=total_size)

    buffer = StringIO()
    read_bytes = 0

    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                read_bytes += len(chunk)
                buffer.write(chunk.decode(encoding=encoding, errors=errors))

                if progress is not None:
                    progress.set(read_bytes)
    except BaseException as e:
        if logger is not None:
            logger.error(f"Failed to load text file '{path}': {e}")
        raise

    if logger is not None:
        logger.info(f"Successfully read file: '{path}' ({read_bytes} bytes)")

    return buffer.getvalue()
