# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Iterable, List, NamedTuple, Optional, Sequence

from cvp.terminal.ansi import sgr
from cvp.terminal.ansi.palette import TerminalPalette
from cvp.terminal.ansi.style import TerminalStyle
from cvp.terminal.ansi.tokenizer import (
    AnsiCsiEscape,
    AnsiError,
    AnsiEscape,
    AnsiFeEscape,
    AnsiLineFeed,
    AnsiRegularText,
    AnsiToken,
)


class SgrText(NamedTuple):
    text: str
    style: TerminalStyle
    error: Optional[str] = None


class SgrLine(List[SgrText]):
    def __init__(self, lineno: int, __iterable: Optional[Iterable[SgrText]] = None):
        super().__init__(__iterable or ())
        self.lineno = lineno


def apply_sgr_style(
    style: TerminalStyle,
    palette: TerminalPalette,
    *params: int,
    use_deepcopy=False,
) -> TerminalStyle:
    assert 1 <= len(params)
    result = deepcopy(style) if use_deepcopy else style
    try:
        match params[0]:
            # --------------------------------------------------------------------------
            case sgr.RESET:
                result.reset()
            # --------------------------------------------------------------------------
            case sgr.BOLD:
                result.bold = True
            case sgr.FAINT:
                result.faint = True
            case sgr.ITALIC:
                result.italic = True
            case sgr.UNDERLINE:
                result.underline = True
            case sgr.SLOW_BLINK:
                result.blink_speed = 1
            case sgr.RAPID_BLINK:
                result.blink_speed = 2
            case sgr.REVERSE_VIDEO:
                result.inverse = True
            case sgr.CONCEAL:
                result.hide = True
            case sgr.CROSSED_OUT:
                result.strike = True
            # --------------------------------------------------------------------------
            case sgr.PRIMARY_FONT:
                result.font = None
            case sgr.ALTERNATIVE_FONT_1:
                result.font = 1
            case sgr.ALTERNATIVE_FONT_2:
                result.font = 2
            case sgr.ALTERNATIVE_FONT_3:
                result.font = 3
            case sgr.ALTERNATIVE_FONT_4:
                result.font = 4
            case sgr.ALTERNATIVE_FONT_5:
                result.font = 5
            case sgr.ALTERNATIVE_FONT_6:
                result.font = 6
            case sgr.ALTERNATIVE_FONT_7:
                result.font = 7
            case sgr.ALTERNATIVE_FONT_8:
                result.font = 8
            case sgr.ALTERNATIVE_FONT_9:
                result.font = 9
            case sgr.FRAKTUR:
                pass  # Rarely supported
            # --------------------------------------------------------------------------
            case sgr.NOT_BOLD:
                result.bold = False
            case sgr.NORMAL_INTENSITY:
                result.faint = False
            case sgr.NOT_ITALIC:
                result.italic = False
            case sgr.NOT_UNDERLINED:
                result.underline = False
            case sgr.NOT_BLINKING:
                result.blink_speed = 0
            case sgr.PROPORTIONAL_SPACING:
                pass  # ITU T.61 and T.416, not known to be used on terminals.
            case sgr.NOT_REVERSED:
                result.inverse = False
            case sgr.NOT_CONCEALED:
                result.hide = False
            case sgr.NOT_CROSSED_OUT:
                result.strike = False
            # --------------------------------------------------------------------------
            case sgr.FG_COLOR_BLACK:
                result.foreground = palette.black
            case sgr.FG_COLOR_RED:
                result.foreground = palette.red
            case sgr.FG_COLOR_GREEN:
                result.foreground = palette.green
            case sgr.FG_COLOR_YELLOW:
                result.foreground = palette.yellow
            case sgr.FG_COLOR_BLUE:
                result.foreground = palette.blue
            case sgr.FG_COLOR_MAGENTA:
                result.foreground = palette.magenta
            case sgr.FG_COLOR_CYAN:
                result.foreground = palette.cyan
            case sgr.FG_COLOR_WHITE:
                result.foreground = palette.white
            case sgr.FG_COLOR_EXTENDED:
                result.foreground = sgr.get_extended_color_with_parameters(*params)
            case sgr.FG_COLOR_DEFAULT:
                result.foreground = None
            # --------------------------------------------------------------------------
            case sgr.BG_COLOR_BLACK:
                result.background = palette.black
            case sgr.BG_COLOR_RED:
                result.background = palette.red
            case sgr.BG_COLOR_GREEN:
                result.background = palette.green
            case sgr.BG_COLOR_YELLOW:
                result.background = palette.yellow
            case sgr.BG_COLOR_BLUE:
                result.background = palette.blue
            case sgr.BG_COLOR_MAGENTA:
                result.background = palette.magenta
            case sgr.BG_COLOR_CYAN:
                result.background = palette.cyan
            case sgr.BG_COLOR_WHITE:
                result.background = palette.white
            case sgr.BG_COLOR_EXTENDED:
                result.background = sgr.get_extended_color_with_parameters(*params)
            case sgr.BG_COLOR_DEFAULT:
                result.background = None
            # --------------------------------------------------------------------------
            case sgr.DISABLE_PROPORTIONAL_SPACING:
                pass
            case sgr.FRAMED:
                pass
            case sgr.ENCIRCLED:
                pass
            case sgr.OVERLINED:
                pass
            case sgr.NEITHER_FRAMED_NOR_ENCIRCLED:
                pass
            case sgr.NOT_OVERLINED:
                pass
            # --------------------------------------------------------------------------
            case sgr.UNDERLINE_COLOR:
                result.underline_color = sgr.get_extended_color_with_parameters(*params)
            case sgr.UNDERLINE_COLOR_DEFAULT:
                result.underline_color = None
            # --------------------------------------------------------------------------
            case sgr.IDEOGRAM_UNDERLINE:
                pass
            case sgr.IDEOGRAM_DOUBLE_UNDERLINE:
                pass
            case sgr.IDEOGRAM_OVERLINE:
                pass
            case sgr.IDEOGRAM_DOUBLE_OVERLINE:
                pass
            case sgr.IDEOGRAM_STRESS:
                pass
            case sgr.NO_IDEOGRAM_ATTRIBUTES:
                pass
            # --------------------------------------------------------------------------
            case sgr.SUPERSCRIPT:
                pass
            case sgr.SUBSCRIPT:
                pass
            case sgr.NEITHER_SUPERSCRIPT_NOR_SUBSCRIPT:
                pass
            # --------------------------------------------------------------------------
            case sgr.BRIGHT_FG_COLOR_BLACK:
                result.foreground = palette.bright_black
            case sgr.BRIGHT_FG_COLOR_RED:
                result.foreground = palette.bright_red
            case sgr.BRIGHT_FG_COLOR_GREEN:
                result.foreground = palette.bright_green
            case sgr.BRIGHT_FG_COLOR_YELLOW:
                result.foreground = palette.bright_yellow
            case sgr.BRIGHT_FG_COLOR_BLUE:
                result.foreground = palette.bright_blue
            case sgr.BRIGHT_FG_COLOR_MAGENTA:
                result.foreground = palette.bright_magenta
            case sgr.BRIGHT_FG_COLOR_CYAN:
                result.foreground = palette.bright_cyan
            case sgr.BRIGHT_FG_COLOR_WHITE:
                result.foreground = palette.bright_white
            # --------------------------------------------------------------------------
            case sgr.BRIGHT_BG_COLOR_BLACK:
                result.background = palette.bright_black
            case sgr.BRIGHT_BG_COLOR_RED:
                result.background = palette.bright_red
            case sgr.BRIGHT_BG_COLOR_GREEN:
                result.background = palette.bright_green
            case sgr.BRIGHT_BG_COLOR_YELLOW:
                result.background = palette.bright_yellow
            case sgr.BRIGHT_BG_COLOR_BLUE:
                result.background = palette.bright_blue
            case sgr.BRIGHT_BG_COLOR_MAGENTA:
                result.background = palette.bright_magenta
            case sgr.BRIGHT_BG_COLOR_CYAN:
                result.background = palette.bright_cyan
            case sgr.BRIGHT_BG_COLOR_WHITE:
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
