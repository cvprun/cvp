# -*- coding: utf-8 -*-

from dataclasses import dataclass
from functools import reduce
from typing import Iterable, List, Optional

from cvp.encoding.ascii import (
    HT,
    LF,
    MIDDLE_DOT,
    RIGHT_POINTING_DOUBLE_ANGLE_QUOTATION_MARK,
    SPACE,
)
from cvp.terminal.ansi.sgr.glyph import SgrGlyph
from cvp.terminal.ansi.sgr.lexer import lex_sgr_lines
from cvp.terminal.ansi.sgr.parser import parse_terminal_glyphs_with_line
from cvp.terminal.ansi.tokenizer import tokenize_ansi_escape_text
from cvp.terminal.coord import TerminalCoord, TerminalSelectedArea
from cvp.terminal.palette import TerminalPalette
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


class SgrBuilder:
    def __init__(
        self,
        show_whitespace=False,
        text_disabled_color=0xFF7E7E7E,
        text_selected_bg_color=0x594296FA,
        tab_size=4,
        linefeed=LF,
        space=SPACE,
        tab=HT,
        empty_char=chr(SPACE),
        tab_char=chr(RIGHT_POINTING_DOUBLE_ANGLE_QUOTATION_MARK),
        whitespace_char=chr(MIDDLE_DOT),
    ):
        self.show_whitespace = show_whitespace
        self.text_disabled_color = text_disabled_color
        self.text_selected_bg_color = text_selected_bg_color
        self.tabsize = tab_size
        self.linefeed = linefeed
        self.space = space
        self.tab = tab
        self.empty_char = empty_char
        self.tab_char = tab_char
        self.whitespace_char = whitespace_char

    def convert_glyph_to_block(
        self,
        glyph: SgrGlyph,
        selected: TerminalSelectedArea,
    ) -> TextBlock:
        row = glyph.row
        col = glyph.col
        raw_text = glyph.char if glyph.char else str()

        if self.show_whitespace:
            if not raw_text:
                display_text = self.empty_char
                fg = self.text_disabled_color
            elif raw_text == chr(self.tab):
                display_text = self.tab_char
                fg = self.text_disabled_color
            elif raw_text == chr(self.space):
                display_text = self.whitespace_char
                fg = self.text_disabled_color
            else:
                display_text = raw_text
                fg = glyph.foreground_u32
        else:
            display_text = raw_text
            fg = glyph.foreground_u32

        coord = TerminalCoord(row, col)
        if selected.contain_with_coord(coord):
            bg = self.text_selected_bg_color
        else:
            bg = glyph.background_u32

        e = glyph.error

        return TextBlock(
            raw_text=raw_text,
            display_text=display_text,
            lineno=row,
            col_begin=col,
            col_end=col + 1,
            foreground=fg,
            background=bg,
            error=e,
        )

    def build(
        self,
        text: str,
        *,
        lineno=1,
        style: Optional[TerminalStyle] = None,
        palette: Optional[TerminalPalette] = None,
        selected: Optional[TerminalSelectedArea] = None,
    ) -> List[LineBlock]:
        if not text:
            return list()

        if style is None:
            style = TerminalStyle()
        assert isinstance(style, TerminalStyle)

        if palette is None:
            palette = TerminalPalette()
        assert isinstance(palette, TerminalPalette)

        if selected is None:
            selected = TerminalSelectedArea()
        assert isinstance(selected, TerminalSelectedArea)

        tokens = tokenize_ansi_escape_text(text, linefeed=self.linefeed)
        assert 1 <= len(tokens)

        sgr_lines = lex_sgr_lines(tokens, style, palette, lineno=lineno)
        assert 1 <= len(sgr_lines)

        result = list()
        for sgr_line in sgr_lines:
            glyphs = parse_terminal_glyphs_with_line(sgr_line, tabsize=self.tabsize)
            assert 1 <= len(glyphs)

            last_block = self.convert_glyph_to_block(glyphs[0], selected)
            assert last_block.lineno == sgr_line.lineno

            text_blocks = [last_block]

            for glyph in glyphs[1:]:
                block = self.convert_glyph_to_block(glyph, selected)
                assert block.lineno == sgr_line.lineno

                if last_block.mergeable_with(block):
                    last_block.merge(block)
                else:
                    text_blocks.append(block)
                    last_block = block

            result.append(LineBlock(sgr_line.lineno, text_blocks))
        return result
