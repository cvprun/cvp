# -*- coding: utf-8 -*-

from typing import NamedTuple


class TerminalCoord(NamedTuple):
    lineno: int
    column: int

    @property
    def is_invalid_column(self) -> bool:
        return self.column <= 0

    def __repr__(self):
        return f"<{type(self).__name__} lineno={self.lineno}, column={self.column}>"

    def __str__(self):
        return f"{self.lineno}:{self.column}"
