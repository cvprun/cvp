# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from cvp.encoding.config import EncodingConfig
from cvp.variables import DEFAULT_STRING_NEWLINE, INFINITE


@dataclass
class TailConfig(EncodingConfig):
    newline: str = DEFAULT_STRING_NEWLINE
    autoscroll: bool = True

    max_buffer_lines: int = INFINITE
    """
    Maximum number of lines to keep in the buffer.
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

    def set_infinite_lines(self) -> None:
        self.max_buffer_lines = INFINITE
