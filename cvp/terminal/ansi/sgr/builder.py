# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Dict, List, Optional

from cvp.encoding.ascii import (
    HT,
    LF,
    MIDDLE_DOT,
    RIGHT_POINTING_DOUBLE_ANGLE_QUOTATION_MARK,
    SPACE,
)
from cvp.terminal.ansi.sgr.block import CachedLineBlock, LineBlock, TextBlock
from cvp.terminal.ansi.sgr.glyph import SgrGlyph
from cvp.terminal.ansi.sgr.lexer import lex_sgr_lines
from cvp.terminal.ansi.sgr.parser import parse_terminal_glyphs_with_line
from cvp.terminal.ansi.tokenizer import tokenize_ansi_escape_text
from cvp.terminal.palette import TerminalPalette
from cvp.terminal.selection import TerminalSelection
from cvp.terminal.style import TerminalStyle


class SgrBuilder:
    def __init__(
        self,
        show_whitespace=False,
        text_disabled_color=0xFF7E7E7E,
        text_selected_bg_color=0x594296FA,
        tabsize=4,
        linefeed=LF,
        space=SPACE,
        tab=HT,
        empty_char=chr(SPACE),
        tab_char=chr(RIGHT_POINTING_DOUBLE_ANGLE_QUOTATION_MARK),
        whitespace_char=chr(MIDDLE_DOT),
        *,
        cache_lines: Optional[Dict[int, CachedLineBlock]] = None,
    ):
        self.show_whitespace = show_whitespace
        self.text_disabled_color = text_disabled_color
        self.text_selected_bg_color = text_selected_bg_color
        self.tabsize = tabsize
        self.linefeed = linefeed
        self.space = space
        self.tab = tab
        self.empty_char = empty_char
        self.tab_char = tab_char
        self.whitespace_char = whitespace_char
        self._cache_lines = dict(cache_lines or {})

    def convert_glyph_to_block(
        self,
        glyph: SgrGlyph,
        selection: TerminalSelection,
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

        if selected := selection.contain_with(row, col):
            bg = self.text_selected_bg_color
        else:
            bg = glyph.background_u32

        return TextBlock(
            raw_text=raw_text,
            display_text=display_text,
            lineno=row,
            col_begin=col,
            col_end=col + 1,
            foreground=fg,
            background=bg,
            error=glyph.error,
            selected=selected,
        )

    def build_with_text(
        self,
        lineno: int,
        text: str,
        style: Optional[TerminalStyle] = None,
        palette: Optional[TerminalPalette] = None,
        selection: Optional[TerminalSelection] = None,
        *,
        same_line=False,
    ) -> List[LineBlock]:
        if not text:
            return list()

        if style is None:
            style = TerminalStyle()
        assert isinstance(style, TerminalStyle)

        if palette is None:
            palette = TerminalPalette()
        assert isinstance(palette, TerminalPalette)

        if selection is None:
            selection = TerminalSelection()
        assert isinstance(selection, TerminalSelection)

        tokens = tokenize_ansi_escape_text(text, linefeed=self.linefeed)
        assert 1 <= len(tokens)

        sgr_lines = lex_sgr_lines(
            tokens,
            style,
            palette,
            lineno=lineno,
            same_line=same_line,
        )
        assert 1 <= len(sgr_lines)

        result = list()
        for sgr_line in sgr_lines:
            glyphs = parse_terminal_glyphs_with_line(sgr_line, tabsize=self.tabsize)
            assert 1 <= len(glyphs)

            last_block = self.convert_glyph_to_block(glyphs[0], selection)
            assert last_block.lineno == sgr_line.lineno

            text_blocks = [last_block]

            for glyph in glyphs[1:]:
                block = self.convert_glyph_to_block(glyph, selection)
                assert block.lineno == sgr_line.lineno

                if last_block.mergeable_with(block):
                    last_block.merge(block)
                else:
                    text_blocks.append(block)
                    last_block = block

            result.append(LineBlock(sgr_line.lineno, text_blocks))

        return result

    def build_with_caching(
        self,
        lineno: int,
        text: str,
        style: Optional[TerminalStyle] = None,
        palette: Optional[TerminalPalette] = None,
        selection: Optional[TerminalSelection] = None,
        *,
        same_line=False,
    ) -> CachedLineBlock:
        if style is None:
            style = TerminalStyle()
        assert isinstance(style, TerminalStyle)

        if palette is None:
            palette = TerminalPalette()
        assert isinstance(palette, TerminalPalette)

        if selection is None:
            selection = TerminalSelection()
        assert isinstance(selection, TerminalSelection)

        cache_line = self._cache_lines.get(lineno)
        if not cache_line or not cache_line.equal(text, style, selection):
            initial_style = deepcopy(style)
            line_blocks = self.build_with_text(
                lineno=lineno,
                text=text,
                style=style,
                palette=palette,
                selection=selection,
                same_line=same_line,
            )

            if line_blocks:
                assert 1 == len(line_blocks)
                line_block = line_blocks[0]
            else:
                line_block = LineBlock(lineno=lineno)

            cache_line = CachedLineBlock(lineno, text, line_block, initial_style)
            self._cache_lines[lineno] = cache_line

        return cache_line
