# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from cvp.terminal.coord import TerminalCoord


@dataclass
class TerminalSelection:
    begin: Optional[TerminalCoord] = None
    end: Optional[TerminalCoord] = None

    @property
    def normalize(self):
        if self.begin is None or self.end is None:
            raise ValueError("Selection is not set")

        if self.begin <= self.end:
            return TerminalSelection(self.begin, self.end)
        else:
            return TerminalSelection(self.end, self.begin)

    @property
    def exists(self) -> bool:
        return self.begin is not None and self.end is not None

    def contain_with_coord(self, coord: TerminalCoord) -> bool:
        try:
            begin, end = self.normalize
            return begin <= coord < end
        except ValueError:
            return False

    def contain_with_lineno(self, lineno: int) -> bool:
        try:
            begin, end = self.normalize
            return begin.lineno <= lineno < end.lineno
        except ValueError:
            return False
