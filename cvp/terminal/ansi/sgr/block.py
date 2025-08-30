# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
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

    def as_unformatted_text(self) -> str:
        return (
            f"Raw Text: {self.raw_text}\n"
            f"Display Text: {self.display_text}\n"
            f"Lineno: {self.lineno}\n"
            f"Column Begin: {self.col_begin}\n"
            f"Column End: {self.col_end}\n"
            f"Foreground: {self.foreground}\n"
            f"Background: {self.background}\n"
            f"Error: {self.error}\n"
            f"Selected: {self.selected}\n"
        )

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
    def selection(self) -> TerminalSelection:
        begin_column = self.get_selected_col_begin()
        end_column = self.get_selected_col_end()

        if begin_column is None or end_column is None:
            return TerminalSelection()

        assert isinstance(begin_column, int)
        assert isinstance(end_column, int)
        return TerminalSelection.from_raw(
            self.lineno,
            begin_column,
            self.lineno,
            end_column,
        )

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
        update_at: Optional[datetime] = None,
    ):
        self.lineno = lineno
        self.text = text
        self.line = line
        self.style_before = style
        self.selection = line.selection
        self.update_at = update_at if update_at else datetime.now().astimezone()

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
        if self.selection.begin is not None:
            return self.selection.begin.column
        else:
            return None

    def get_selected_col_end(self) -> Optional[int]:
        if self.selection.end is not None:
            return self.selection.end.column
        else:
            return None

    def clip_selection(self, selection: TerminalSelection):
        return selection.clip_lineno(self.lineno, column_end=self.col_end)

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

        clipped_selection = self.clip_selection(selection)
        if not self.selection.has_area and not clipped_selection.has_area:
            return True

        return self.selection == clipped_selection
