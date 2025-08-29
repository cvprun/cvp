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
    def selected_raw_text(self) -> str:
        items = [block.raw_text for block in self if block.selected]
        return reduce(lambda x, y: f"{x}{y}", items, str())

    @property
    def display_text(self) -> str:
        items = [block.display_text for block in self]
        return reduce(lambda x, y: f"{x}{y}", items, str())

    @property
    def selected_display_text(self) -> str:
        items = [block.display_text for block in self if block.selected]
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
        line: LineBlock,
        style: TerminalStyle,
    ):
        self.lineno = lineno
        self.text = text
        self.line = line
        self.style_before = style

    @property
    def col_begin(self) -> int:
        try:
            return self.line.col_begin
        except:  # noqa
            return 0

    @property
    def col_end(self) -> int:
        try:
            return self.line.col_end
        except:  # noqa
            return 0

    @property
    def cols(self) -> int:
        try:
            return self.line.cols
        except:  # noqa
            return 0

    def get_selected_col_begin(self) -> Optional[int]:
        return self.line.get_selected_col_begin()

    def get_selected_col_end(self) -> Optional[int]:
        return self.line.get_selected_col_end()

    @property
    def selected_col_begin(self) -> int:
        return self.line.selected_col_begin

    @property
    def selected_col_end(self) -> int:
        return self.line.selected_col_end

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

        line_selection = selection.clip_lineno(self.lineno)

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
