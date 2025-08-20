# -*- coding: utf-8 -*-

from typing import Optional

from cvp.colors.convert.imgui import argb8888_to_uint32
from cvp.colors.xterm import XTERM_256COLOR_MAP
from cvp.terminal.ansi.sgr.codes import BG_COLOR_EXTENDED, FG_COLOR_EXTENDED


def get_extended_color_with_parameters(*args: int) -> Optional[int]:
    try:
        if args[0] not in (FG_COLOR_EXTENDED, BG_COLOR_EXTENDED):
            return None

        match args[1]:
            case 2:
                r, g, b = args[2], args[3], args[4]
                return argb8888_to_uint32(0xFF, r, g, b)
            case 5:
                r, g, b = XTERM_256COLOR_MAP[args[2]]
                return argb8888_to_uint32(0xFF, r, g, b)
    except:  # noqa
        pass

    return None
