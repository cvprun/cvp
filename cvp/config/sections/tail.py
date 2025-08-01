# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from cvp.encoding.config import EncodingConfig
from cvp.units.byte import BYTES_1KB
from cvp.variables import DEFAULT_STRING_NEWLINE, INFINITE


@dataclass
class TailConfig(EncodingConfig):
    newline: str = DEFAULT_STRING_NEWLINE
    autoscroll: bool = True

    max_buffer_lines: int = INFINITE
    """
    Maximum number of lines to keep in the buffer.
    """

    initial_read_bytes: int = 4 * BYTES_1KB
    """
    Number of bytes to read from the end of the file when opening for the first time.
    """

    @property
    def maxlen(self) -> Optional[int]:
        """
        Property for `collections.deque` constructor argument (for maxlen)
        """
        if self.max_buffer_lines == INFINITE:
            return None
        else:
            return self.max_buffer_lines
