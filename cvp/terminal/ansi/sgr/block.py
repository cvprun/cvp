# -*- coding: utf-8 -*-

from dataclasses import dataclass
from functools import reduce
from typing import Iterable, List, Optional

from cvp.terminal.selection import TerminalSelection
from cvp.terminal.style import TerminalStyle


@dataclass
class TextBlock:
    raw_text: str
    display_text: str
    lineno: int
    col_begin: int
    col_end: int
    foreground: Optional[int] = None
    background: Optional[int] = None
    error: Optional[str] = None
    selected: bool = False

    @property
    def cols(self) -> int:
        return self.col_end - self.col_begin

    def merge(self, item: "TextBlock") -> None:
        assert self.lineno == item.lineno
        assert self.col_end == item.col_begin
        assert self.foreground == item.foreground
        assert self.background == item.background
        assert self.error == item.error
        assert self.selected == item.selected

        self.raw_text += item.raw_text
        self.display_text += item.display_text
        self.col_end = item.col_end

    def mergeable_with(self, item: "TextBlock") -> bool:
        if self.lineno != item.lineno:
            return False
        if self.col_end != item.col_begin:
            return False
        if self.foreground != item.foreground:
            return False
        if self.background != item.background:
            return False
        if self.error != item.error:
            return False
        if self.selected != item.selected:
            return False
        return True


class LineBlock(List[TextBlock]):
    def __init__(self, lineno: int, __iterable: Optional[Iterable[TextBlock]] = None):
        super().__init__(__iterable or ())
        self.lineno = lineno

    @property
    def raw_text(self) -> str:
        items = [block.raw_text for block in self]
        return reduce(lambda x, y: f"{x}{y}", items, str())

    @property
    def display_text(self) -> str:
        items = [block.display_text for block in self]
        return reduce(lambda x, y: f"{x}{y}", items, str())

    @property
    def col_begin(self) -> int:
        return self[0].col_begin

    @property
    def col_end(self) -> int:
        return self[-1].col_end

    @property
    def cols(self) -> int:
        return self.col_end - self.col_begin

    def get_selected_col_begin(self) -> Optional[int]:
        for block in self:
            if block.selected:
                return block.col_begin
        return None

    def get_selected_col_end(self) -> Optional[int]:
        for block in reversed(self):
            if block.selected:
                return block.col_end
        return None

    @property
    def selected_col_begin(self) -> int:
        column = self.get_selected_col_begin()
        if column is not None:
            return column
        raise ValueError("Cannot find selected block")

    @property
    def selected_col_end(self) -> int:
        column = self.get_selected_col_end()
        if column is not None:
            return column
        raise ValueError("Cannot find selected block")


class CachedLineBlock:
    def __init__(
        self,
        lineno: int,
        text: str,
        lines: List[LineBlock],
        style: TerminalStyle,
    ):
        self.lineno = lineno
        self.text = text
        self.lines = lines
        self.style_before = style
        self.selection_col_begin = self._find_selected_col_begin(lines)
        self.selection_col_end = self._find_selected_col_end(lines)

    @staticmethod
    def _find_selected_col_begin(lines: List[LineBlock]) -> Optional[int]:
        if not lines:
            return None

        line0 = lines[0]
        begin = line0.get_selected_col_begin()
        if begin is not None:
            return begin

        for line_n in lines[1:]:
            begin = line_n.get_selected_col_begin()
            if begin is not None:
                return begin

        return None

    @staticmethod
    def _find_selected_col_end(lines: List[LineBlock]) -> Optional[int]:
        if not lines:
            return None

        line_last = lines[-1]
        end = line_last.get_selected_col_end()
        if end is not None:
            return end

        for line_n in reversed(lines[:-1]):
            end = line_n.get_selected_col_end()
            if end is not None:
                return end

        return None

    @property
    def rows(self) -> int:
        return len(self.lines)

    @property
    def cols(self) -> int:
        return max(line.cols for line in self.lines) if self.lines else 0

    def equal(
        self,
        text: str,
        style: TerminalStyle,
        selection: TerminalSelection,
    ) -> bool:
        if self.text != text:
            return False

        if self.style_before != style:
            return False

        # if self.selected != selection:
        #     if selection.exists:
        #         begin, end = selection.normalize
        #         assert isinstance(begin, TerminalCoord)
        #         assert isinstance(end, TerminalCoord)
        #         begin.lineno < self.lineno < end.lineno
        #     begin, end = self.selection.contain_with_lineno(self.lineno)
        #     return False

        # begin_lineno = selection.begin.lineno
        # begin_column = selection.begin.column
        # end_lineno = selection.end.lineno
        # end_column = selection.end.column
        # for line in self.lines:
        #     current_lineno = line.lineno
        #     for text in line:
        #         text_col_begin = text.col_begin
        #         text_col_end = text.col_end

        return True
