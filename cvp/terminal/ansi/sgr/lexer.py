# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import List, Optional, Sequence

from cvp.memory.copy import copy_flexible
from cvp.terminal.ansi.sgr import codes as sgr_codes
from cvp.terminal.ansi.sgr.colors import get_extended_color_with_parameters
from cvp.terminal.ansi.sgr.line import SgrLine
from cvp.terminal.ansi.sgr.text import SgrText
from cvp.terminal.ansi.tokenizer import (
    AnsiCsiEscape,
    AnsiError,
    AnsiEscape,
    AnsiFeEscape,
    AnsiLineFeed,
    AnsiRegularText,
    AnsiToken,
)
from cvp.terminal.palette import TerminalPalette
from cvp.terminal.style import TerminalStyle


def apply_sgr_style(
    style: TerminalStyle,
    palette: TerminalPalette,
    *params: int,
    use_copy=False,
    use_deepcopy=False,
) -> TerminalStyle:
    assert 1 <= len(params)
    result = copy_flexible(style, use_copy=use_copy, use_deepcopy=use_deepcopy)
    try:
        match params[0]:
            # --------------------------------------------------------------------------
            case sgr_codes.RESET:
                result.reset()
            # --------------------------------------------------------------------------
            case sgr_codes.BOLD:
                result.bold = True
            case sgr_codes.FAINT:
                result.faint = True
            case sgr_codes.ITALIC:
                result.italic = True
            case sgr_codes.UNDERLINE:
                result.underline = True
            case sgr_codes.SLOW_BLINK:
                result.blink_speed = 1
            case sgr_codes.RAPID_BLINK:
                result.blink_speed = 2
            case sgr_codes.REVERSE_VIDEO:
                result.inverse = True
            case sgr_codes.CONCEAL:
                result.hide = True
            case sgr_codes.CROSSED_OUT:
                result.strike = True
            # --------------------------------------------------------------------------
            case sgr_codes.PRIMARY_FONT:
                result.font = None
            case sgr_codes.ALTERNATIVE_FONT_1:
                result.font = 1
            case sgr_codes.ALTERNATIVE_FONT_2:
                result.font = 2
            case sgr_codes.ALTERNATIVE_FONT_3:
                result.font = 3
            case sgr_codes.ALTERNATIVE_FONT_4:
                result.font = 4
            case sgr_codes.ALTERNATIVE_FONT_5:
                result.font = 5
            case sgr_codes.ALTERNATIVE_FONT_6:
                result.font = 6
            case sgr_codes.ALTERNATIVE_FONT_7:
                result.font = 7
            case sgr_codes.ALTERNATIVE_FONT_8:
                result.font = 8
            case sgr_codes.ALTERNATIVE_FONT_9:
                result.font = 9
            case sgr_codes.FRAKTUR:
                pass  # Rarely supported
            # --------------------------------------------------------------------------
            case sgr_codes.NOT_BOLD:
                result.bold = False
            case sgr_codes.NORMAL_INTENSITY:
                result.faint = False
            case sgr_codes.NOT_ITALIC:
                result.italic = False
            case sgr_codes.NOT_UNDERLINED:
                result.underline = False
            case sgr_codes.NOT_BLINKING:
                result.blink_speed = 0
            case sgr_codes.PROPORTIONAL_SPACING:
                pass  # ITU T.61 and T.416, not known to be used on terminals.
            case sgr_codes.NOT_REVERSED:
                result.inverse = False
            case sgr_codes.NOT_CONCEALED:
                result.hide = False
            case sgr_codes.NOT_CROSSED_OUT:
                result.strike = False
            # --------------------------------------------------------------------------
            case sgr_codes.FG_COLOR_BLACK:
                result.foreground = palette.black
            case sgr_codes.FG_COLOR_RED:
                result.foreground = palette.red
            case sgr_codes.FG_COLOR_GREEN:
                result.foreground = palette.green
            case sgr_codes.FG_COLOR_YELLOW:
                result.foreground = palette.yellow
            case sgr_codes.FG_COLOR_BLUE:
                result.foreground = palette.blue
            case sgr_codes.FG_COLOR_MAGENTA:
                result.foreground = palette.magenta
            case sgr_codes.FG_COLOR_CYAN:
                result.foreground = palette.cyan
            case sgr_codes.FG_COLOR_WHITE:
                result.foreground = palette.white
            case sgr_codes.FG_COLOR_EXTENDED:
                result.foreground = get_extended_color_with_parameters(*params)
            case sgr_codes.FG_COLOR_DEFAULT:
                result.foreground = None
            # --------------------------------------------------------------------------
            case sgr_codes.BG_COLOR_BLACK:
                result.background = palette.black
            case sgr_codes.BG_COLOR_RED:
                result.background = palette.red
            case sgr_codes.BG_COLOR_GREEN:
                result.background = palette.green
            case sgr_codes.BG_COLOR_YELLOW:
                result.background = palette.yellow
            case sgr_codes.BG_COLOR_BLUE:
                result.background = palette.blue
            case sgr_codes.BG_COLOR_MAGENTA:
                result.background = palette.magenta
            case sgr_codes.BG_COLOR_CYAN:
                result.background = palette.cyan
            case sgr_codes.BG_COLOR_WHITE:
                result.background = palette.white
            case sgr_codes.BG_COLOR_EXTENDED:
                result.background = get_extended_color_with_parameters(*params)
            case sgr_codes.BG_COLOR_DEFAULT:
                result.background = None
            # --------------------------------------------------------------------------
            case sgr_codes.DISABLE_PROPORTIONAL_SPACING:
                pass
            case sgr_codes.FRAMED:
                pass
            case sgr_codes.ENCIRCLED:
                pass
            case sgr_codes.OVERLINED:
                pass
            case sgr_codes.NEITHER_FRAMED_NOR_ENCIRCLED:
                pass
            case sgr_codes.NOT_OVERLINED:
                pass
            # --------------------------------------------------------------------------
            case sgr_codes.UNDERLINE_COLOR:
                result.underline_color = get_extended_color_with_parameters(*params)
            case sgr_codes.UNDERLINE_COLOR_DEFAULT:
                result.underline_color = None
            # --------------------------------------------------------------------------
            case sgr_codes.IDEOGRAM_UNDERLINE:
                pass
            case sgr_codes.IDEOGRAM_DOUBLE_UNDERLINE:
                pass
            case sgr_codes.IDEOGRAM_OVERLINE:
                pass
            case sgr_codes.IDEOGRAM_DOUBLE_OVERLINE:
                pass
            case sgr_codes.IDEOGRAM_STRESS:
                pass
            case sgr_codes.NO_IDEOGRAM_ATTRIBUTES:
                pass
            # --------------------------------------------------------------------------
            case sgr_codes.SUPERSCRIPT:
                pass
            case sgr_codes.SUBSCRIPT:
                pass
            case sgr_codes.NEITHER_SUPERSCRIPT_NOR_SUBSCRIPT:
                pass
            # --------------------------------------------------------------------------
            case sgr_codes.BRIGHT_FG_COLOR_BLACK:
                result.foreground = palette.bright_black
            case sgr_codes.BRIGHT_FG_COLOR_RED:
                result.foreground = palette.bright_red
            case sgr_codes.BRIGHT_FG_COLOR_GREEN:
                result.foreground = palette.bright_green
            case sgr_codes.BRIGHT_FG_COLOR_YELLOW:
                result.foreground = palette.bright_yellow
            case sgr_codes.BRIGHT_FG_COLOR_BLUE:
                result.foreground = palette.bright_blue
            case sgr_codes.BRIGHT_FG_COLOR_MAGENTA:
                result.foreground = palette.bright_magenta
            case sgr_codes.BRIGHT_FG_COLOR_CYAN:
                result.foreground = palette.bright_cyan
            case sgr_codes.BRIGHT_FG_COLOR_WHITE:
                result.foreground = palette.bright_white
            # --------------------------------------------------------------------------
            case sgr_codes.BRIGHT_BG_COLOR_BLACK:
                result.background = palette.bright_black
            case sgr_codes.BRIGHT_BG_COLOR_RED:
                result.background = palette.bright_red
            case sgr_codes.BRIGHT_BG_COLOR_GREEN:
                result.background = palette.bright_green
            case sgr_codes.BRIGHT_BG_COLOR_YELLOW:
                result.background = palette.bright_yellow
            case sgr_codes.BRIGHT_BG_COLOR_BLUE:
                result.background = palette.bright_blue
            case sgr_codes.BRIGHT_BG_COLOR_MAGENTA:
                result.background = palette.bright_magenta
            case sgr_codes.BRIGHT_BG_COLOR_CYAN:
                result.background = palette.bright_cyan
            case sgr_codes.BRIGHT_BG_COLOR_WHITE:
                result.background = palette.bright_white
            # --------------------------------------------------------------------------
    finally:
        return result


def lex_sgr_lines(
    tokens: Sequence[AnsiToken],
    style: Optional[TerminalStyle] = None,
    palette: Optional[TerminalPalette] = None,
    *,
    lineno=1,
) -> List[SgrLine]:
    """
    Lexical analyzer for SGR (Select Graphic Rendition) sequences.
    """
    if not tokens:
        return list()

    if style is None:
        style = TerminalStyle()
    assert isinstance(style, TerminalStyle)

    if palette is None:
        palette = TerminalPalette()
    assert isinstance(palette, TerminalPalette)

    result: List[SgrLine] = list()
    current_line = SgrLine(lineno)

    for token in tokens:
        if isinstance(token, AnsiError):
            current_line.append(SgrText(token.text, deepcopy(style), token.error))
        elif isinstance(token, AnsiLineFeed):
            result.append(current_line)
            current_line = SgrLine(current_line.lineno + 1)
        elif isinstance(token, AnsiRegularText):
            current_line.append(SgrText(token.text, deepcopy(style)))
        elif isinstance(token, AnsiCsiEscape):
            if token.command.is_sgr:
                try:
                    params = token.command.as_integer_parameters()
                    assert 1 <= len(params)
                    apply_sgr_style(style, palette, *params, use_deepcopy=False)
                except BaseException as e:
                    current_line.append(SgrText(token.text, deepcopy(style), str(e)))
            else:
                pass  # Non-SGR CSI sequences are not used.
        elif isinstance(token, AnsiFeEscape):
            pass  # "Fe Escape sequences" are not used.
        elif isinstance(token, AnsiEscape):
            pass  # "Escape sequences" are not used.
        else:
            assert False, "Inaccessible section"

    if current_line:
        result.append(current_line)

    return result
