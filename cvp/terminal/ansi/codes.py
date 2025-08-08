# -*- coding: utf-8 -*-

from typing import Final

ESC: Final[str] = "\x1b"
CSI: Final[str] = "["  # Control Sequence Introducer
SGR: Final[str] = "m"  # Select Graphic Rendition

BLACK_FG: Final[int] = 30
RED_FG: Final[int] = 31
GREEN_FG: Final[int] = 32
YELLOW_FG: Final[int] = 33
BLUE_FG: Final[int] = 34
MAGENTA_FG: Final[int] = 35
CYAN_FG: Final[int] = 36
WHITE_FG: Final[int] = 37
DEFAULT_FG: Final[int] = 39

BLACK_BG: Final[int] = 40
RED_BG: Final[int] = 41
GREEN_BG: Final[int] = 42
YELLOW_BG: Final[int] = 43
BLUE_BG: Final[int] = 44
MAGENTA_BG: Final[int] = 45
CYAN_BG: Final[int] = 46
WHITE_BG: Final[int] = 47
DEFAULT_BG: Final[int] = 49

BRIGHT_BLACK_FG: Final[int] = 90
BRIGHT_RED_FG: Final[int] = 91
BRIGHT_GREEN_FG: Final[int] = 92
BRIGHT_YELLOW_FG: Final[int] = 93
BRIGHT_BLUE_FG: Final[int] = 94
BRIGHT_MAGENTA_FG: Final[int] = 95
BRIGHT_CYAN_FG: Final[int] = 96
BRIGHT_WHITE_FG: Final[int] = 97

BRIGHT_BLACK_BG: Final[int] = 100
BRIGHT_RED_BG: Final[int] = 101
BRIGHT_GREEN_BG: Final[int] = 102
BRIGHT_YELLOW_BG: Final[int] = 103
BRIGHT_BLUE_BG: Final[int] = 104
BRIGHT_MAGENTA_BG: Final[int] = 105
BRIGHT_CYAN_BG: Final[int] = 106
BRIGHT_WHITE_BG: Final[int] = 107
