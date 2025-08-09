# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
#
# print a list of the 256-color red/green/blue values used by xterm.
# https://github.com/ThomasDickey/ncurses-snapshots/blob/master/test/xterm-16color.dat
# https://github.com/ThomasDickey/xterm-snapshots/blob/master/XTerm-col.ad
# https://github.com/ThomasDickey/xterm-snapshots/blob/master/256colres.pl

from functools import lru_cache
from types import MappingProxyType
from typing import Dict, Tuple


def create_256color_mapping() -> Dict[int, Tuple[int, int, int]]:
    result = dict()

    # colors 0-16 correspond to the ANSI and aixterm naming
    for code in range(0, 16):
        if code > 8:
            level = 255
        elif code == 7:
            level = 229
        else:
            level = 205

        r = 127 if code == 8 else level if (code & 1) != 0 else 92 if code == 12 else 0
        g = 127 if code == 8 else level if (code & 2) != 0 else 92 if code == 12 else 0
        b = 127 if code == 8 else 238 if code == 4 else level if (code & 4) != 0 else 0
        result[code] = r, g, b

    # colors 16-231 are a 6x6x6 color cube
    for red__ in range(0, 6):
        for green in range(0, 6):
            for blue_ in range(0, 6):
                code = 16 + (red__ * 36) + (green * 6) + blue_
                r = red__ * 40 + 55 if red__ != 0 else 0
                g = green * 40 + 55 if green != 0 else 0
                b = blue_ * 40 + 55 if blue_ != 0 else 0
                result[code] = r, g, b

    # colors 232-255 are a grayscale ramp, intentionally leaving out black and white
    for gray in range(0, 24):
        level = gray * 10 + 8
        code = 232 + gray
        result[code] = level, level, level

    return result


@lru_cache
def create_xterm_256color_mapping() -> MappingProxyType[int, Tuple[int, int, int]]:
    return MappingProxyType(create_256color_mapping())


XTERM_256COLOR_MAP = create_xterm_256color_mapping()
