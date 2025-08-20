# -*- coding: utf-8 -*-
# Select Graphic Rendition

from typing import Final

RESET: Final[int] = 0
NORMAL: Final[int] = RESET

BOLD: Final[int] = 1
INCREASED_INTENSITY: Final[int] = BOLD

FAINT: Final[int] = 2
DIM: Final[int] = FAINT
DECREASED_INTENSITY: Final[int] = FAINT

ITALIC: Final[int] = 3
UNDERLINE: Final[int] = 4
SLOW_BLINK: Final[int] = 5
RAPID_BLINK: Final[int] = 6

REVERSE_VIDEO: Final[int] = 7
INVERT: Final[int] = REVERSE_VIDEO

CONCEAL: Final[int] = 8
HIDE: Final[int] = CONCEAL

CROSSED_OUT: Final[int] = 9
STRIKETHROUGH: Final[int] = CROSSED_OUT

PRIMARY_FONT: Final[int] = 10
DEFAULT_FONT: Final[int] = PRIMARY_FONT

ALTERNATIVE_FONT_START: Final[int] = 11
ALTERNATIVE_FONT_END: Final[int] = 19


def is_alternative_font(char: int) -> bool:
    return ALTERNATIVE_FONT_START <= char <= ALTERNATIVE_FONT_END


ALTERNATIVE_FONT_1: Final[int] = 11
ALTERNATIVE_FONT_2: Final[int] = 12
ALTERNATIVE_FONT_3: Final[int] = 13
ALTERNATIVE_FONT_4: Final[int] = 14
ALTERNATIVE_FONT_5: Final[int] = 15
ALTERNATIVE_FONT_6: Final[int] = 16
ALTERNATIVE_FONT_7: Final[int] = 17
ALTERNATIVE_FONT_8: Final[int] = 18
ALTERNATIVE_FONT_9: Final[int] = 19

FRAKTUR: Final[int] = 20  # Rarely supported
GOTHIC: Final[int] = FRAKTUR

DOUBLY_UNDERLINED: Final[int] = 21  # Replaced by NOT_BOLD.
NOT_BOLD: Final[int] = DOUBLY_UNDERLINED

NORMAL_INTENSITY: Final[int] = 22

NEITHER_ITALIC_NOR_BLACKLETTER: Final[int] = 23
NOT_ITALIC: Final[int] = NEITHER_ITALIC_NOR_BLACKLETTER

NEITHER_SINGLY_NOR_DOUBLY_UNDERLINED: Final[int] = 24
NOT_UNDERLINED: Final[int] = NEITHER_SINGLY_NOR_DOUBLY_UNDERLINED

NOT_BLINKING: Final[int] = 25
PROPORTIONAL_SPACING: Final[int] = 26
NOT_REVERSED: Final[int] = 27

REVEAL: Final[int] = 28
NOT_CONCEALED: Final[int] = REVEAL

NOT_CROSSED_OUT: Final[int] = 29
NOT_STRIKETHROUGH: Final[int] = NOT_CROSSED_OUT

FG_COLOR_START: Final[int] = 30
FG_COLOR_END: Final[int] = 37


def is_fg_color(char: int) -> bool:
    return FG_COLOR_START <= char <= FG_COLOR_END


FG_COLOR_BLACK: Final[int] = 30
FG_COLOR_RED: Final[int] = 31
FG_COLOR_GREEN: Final[int] = 32
FG_COLOR_YELLOW: Final[int] = 33
FG_COLOR_BLUE: Final[int] = 34
FG_COLOR_MAGENTA: Final[int] = 35
FG_COLOR_CYAN: Final[int] = 36
FG_COLOR_WHITE: Final[int] = 37

FG_COLOR_EXTENDED: Final[int] = 38
"""Next arguments are `5;n` or `2;r;g;b`"""

FG_COLOR_DEFAULT: Final[int] = 39

BG_COLOR_START: Final[int] = 40
BG_COLOR_END: Final[int] = 47


def is_bg_color(char: int) -> bool:
    return BG_COLOR_START <= char <= BG_COLOR_END


BG_COLOR_BLACK: Final[int] = 40
BG_COLOR_RED: Final[int] = 41
BG_COLOR_GREEN: Final[int] = 42
BG_COLOR_YELLOW: Final[int] = 43
BG_COLOR_BLUE: Final[int] = 44
BG_COLOR_MAGENTA: Final[int] = 45
BG_COLOR_CYAN: Final[int] = 46
BG_COLOR_WHITE: Final[int] = 47

BG_COLOR_EXTENDED: Final[int] = 48
"""Next arguments are `5;n` or `2;r;g;b`"""

BG_COLOR_DEFAULT: Final[int] = 49

DISABLE_PROPORTIONAL_SPACING: Final[int] = 50
FRAMED: Final[int] = 51
ENCIRCLED: Final[int] = 52
OVERLINED: Final[int] = 53
NEITHER_FRAMED_NOR_ENCIRCLED: Final[int] = 54
NOT_OVERLINED: Final[int] = 55

UNDERLINE_COLOR: Final[int] = 58
"""
Not in standard; implemented in Kitty, VTE, mintty, and iTerm2.
Next arguments are `5;n` or `2;r;g;b`.
"""

UNDERLINE_COLOR_DEFAULT: Final[int] = 59
"""
Not in standard; implemented in Kitty, VTE, mintty, and iTerm2.
"""

IDEOGRAM_UNDERLINE: Final[int] = 60
IDEOGRAM_DOUBLE_UNDERLINE: Final[int] = 61
IDEOGRAM_OVERLINE: Final[int] = 62
IDEOGRAM_DOUBLE_OVERLINE: Final[int] = 63
IDEOGRAM_STRESS: Final[int] = 64

RIGHT_SIDE_LINE: Final[int] = IDEOGRAM_UNDERLINE
DOUBLE_LINE_ON_THE_RIGHT_SIDE: Final[int] = IDEOGRAM_DOUBLE_UNDERLINE
LEFT_SIDE_LINE: Final[int] = IDEOGRAM_OVERLINE
DOUBLE_LINE_ON_THE_LEFT_SIDE: Final[int] = IDEOGRAM_DOUBLE_OVERLINE
IDEOGRAM_STRESS_MARKING: Final[int] = IDEOGRAM_STRESS

NO_IDEOGRAM_ATTRIBUTES: Final[int] = 65
"""Reset the effects of all of 60-64"""

SUPERSCRIPT: Final[int] = 73
SUBSCRIPT: Final[int] = 74
NEITHER_SUPERSCRIPT_NOR_SUBSCRIPT: Final[int] = 75

BRIGHT_FG_COLOR_START: Final[int] = 90
BRIGHT_FG_COLOR_END: Final[int] = 97


def is_bright_fg_color(char: int) -> bool:
    return BRIGHT_FG_COLOR_START <= char <= BRIGHT_FG_COLOR_END


BRIGHT_FG_COLOR_BLACK: Final[int] = 90
BRIGHT_FG_COLOR_RED: Final[int] = 91
BRIGHT_FG_COLOR_GREEN: Final[int] = 92
BRIGHT_FG_COLOR_YELLOW: Final[int] = 93
BRIGHT_FG_COLOR_BLUE: Final[int] = 94
BRIGHT_FG_COLOR_MAGENTA: Final[int] = 95
BRIGHT_FG_COLOR_CYAN: Final[int] = 96
BRIGHT_FG_COLOR_WHITE: Final[int] = 97

BRIGHT_BG_COLOR_START: Final[int] = 100
BRIGHT_BG_COLOR_END: Final[int] = 107


def is_bright_bg_color(char: int) -> bool:
    return BRIGHT_BG_COLOR_START <= char <= BRIGHT_BG_COLOR_END


BRIGHT_BG_COLOR_BLACK: Final[int] = 100
BRIGHT_BG_COLOR_RED: Final[int] = 101
BRIGHT_BG_COLOR_GREEN: Final[int] = 102
BRIGHT_BG_COLOR_YELLOW: Final[int] = 103
BRIGHT_BG_COLOR_BLUE: Final[int] = 104
BRIGHT_BG_COLOR_MAGENTA: Final[int] = 105
BRIGHT_BG_COLOR_CYAN: Final[int] = 106
BRIGHT_BG_COLOR_WHITE: Final[int] = 107
