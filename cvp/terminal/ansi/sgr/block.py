# -*- coding: utf-8 -*-

from dataclasses import dataclass
from functools import reduce
from typing import Iterable, List, Optional


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

    @property
    def cols(self) -> int:
        return self.col_end - self.col_begin

    def merge(self, item: "TextBlock") -> None:
        assert self.lineno == item.lineno
        assert self.col_end == item.col_begin
        assert self.foreground == item.foreground
        assert self.background == item.background
        assert self.error == item.error

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
