# -*- coding: utf-8 -*-

from typing import Final, Optional

from cvp.colors.convert.imgui import argb8888_to_uint32
from cvp.colors.xterm import XTERM_256COLOR_MAP
from cvp.terminal.ansi.sgr.codes import BG_COLOR_EXTENDED, FG_COLOR_EXTENDED

SGR_EXT_COLOR_8BIT: Final[int] = 5
"""
ESC[38;5;⟨n⟩m Select foreground color
ESC[48;5;⟨n⟩m Select background color

https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
"""

SGR_EXT_COLOR_24BIT: Final[int] = 2
"""
ESC[38;2;⟨r⟩;⟨g⟩;⟨b⟩m Select RGB foreground color
ESC[48;2;⟨r⟩;⟨g⟩;⟨b⟩m Select RGB background color

https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
"""


def get_extended_color_with_parameters(*args: int) -> Optional[int]:
    try:
        if args[0] not in (FG_COLOR_EXTENDED, BG_COLOR_EXTENDED):
            return None

        a2 = args[1]
        if a2 == SGR_EXT_COLOR_8BIT:
            r, g, b = XTERM_256COLOR_MAP[args[2]]
            return argb8888_to_uint32(0xFF, r, g, b)
        elif a2 == SGR_EXT_COLOR_24BIT:
            r, g, b = args[2], args[3], args[4]
            return argb8888_to_uint32(0xFF, r, g, b)
        else:
            raise ValueError(f"Unexpected 2nd argument value: {a2}")
    except:  # noqa
        pass

    return None
