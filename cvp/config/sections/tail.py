# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from cvp.encoding.config import EncodingConfig
from cvp.variables import (
    DEFAULT_STRING_ENCODING,
    DEFAULT_STRING_ERRORS,
    DEFAULT_STRING_NEWLINE,
    INFINITE,
)


@dataclass
class TailConfig(EncodingConfig):
    show_tabs_always: bool = False

    newline: str = DEFAULT_STRING_NEWLINE
    autoscroll: bool = True

    show_lineno: bool = False
    show_whitespace: bool = False
    show_eol: bool = False
    show_block_roi: bool = False
    show_line_roi: bool = False
    show_error: bool = False

    max_buffer_lines: int = INFINITE
    """
    Maximum number of lines to keep in the buffer.
    """

    manually_update_interval: float = 0.0

    @property
    def maxlen(self) -> Optional[int]:
        """
        Property for `collections.deque` constructor argument (for maxlen)
        """
        if self.max_buffer_lines == INFINITE:
            return None
        else:
            return self.max_buffer_lines

    def update_infinite_lines(self) -> None:
        self.max_buffer_lines = INFINITE

    def update_defaults(self) -> None:
        self.encoding = DEFAULT_STRING_ENCODING
        self.errors = DEFAULT_STRING_ERRORS
        self.show_tabs_always = False
        self.newline = DEFAULT_STRING_NEWLINE
        self.autoscroll = True
        self.max_buffer_lines = INFINITE
        self.manually_update_interval = 0.0
