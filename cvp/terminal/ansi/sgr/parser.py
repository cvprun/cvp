# -*- coding: utf-8 -*-

from typing import List, Sequence, Tuple, Union

from wcwidth import wcwidth

from cvp.encoding.ascii import HT
from cvp.terminal.ansi.sgr.lexer import SgrLine
from cvp.terminal.glyph import TerminalGlyph


def parse_terminal_glyphs_with_line(
    sgr_line: SgrLine,
    default_foreground: Union[None, int, Tuple[int, int, int]] = None,
    default_background: Union[None, int, Tuple[int, int, int]] = None,
    tab_size=4,
) -> List[TerminalGlyph]:
    result = list()
    column = 0

    for sgr_text in sgr_line:
        if sgr_text.style.background is None:
            bg_color = default_background
        else:
            bg_color = sgr_text.style.background

        if sgr_text.style.foreground is None:
            fg_color = default_foreground
        else:
            fg_color = sgr_text.style.foreground

        for c in sgr_text.text:
            column_size = tab_size if ord(c) == HT else wcwidth(c)
            if column_size <= 0:
                continue

            glyph = TerminalGlyph(
                row=sgr_line.lineno,
                col=column,
                char=c,
                foreground=fg_color,
                background=bg_color,
                error=sgr_text.error,
            )
            result.append(glyph)
            column += 1

            if column_size <= 1:
                continue

            for _ in range(column_size - 1):
                glyph = TerminalGlyph(
                    row=sgr_line.lineno,
                    col=column,
                    char=None,
                    foreground=fg_color,
                    background=bg_color,
                    error=sgr_text.error,
                )
                result.append(glyph)
                column += 1

    return result


def parse_terminal_glyphs_with_lines(
    sgr_lines: Sequence[SgrLine],
    default_foreground: Union[None, int, Tuple[int, int, int]] = None,
    default_background: Union[None, int, Tuple[int, int, int]] = None,
    tab_size=4,
) -> List[TerminalGlyph]:
    result = list()
    for sgr_line in sgr_lines:
        items = parse_terminal_glyphs_with_line(
            sgr_line=sgr_line,
            default_foreground=default_foreground,
            default_background=default_background,
            tab_size=tab_size,
        )
        result.extend(items)
    return result
