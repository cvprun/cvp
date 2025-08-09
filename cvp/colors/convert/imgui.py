# -*- coding: utf-8 -*-

from cvp.types.colors import RGB, RGBA

"""
// Helpers macros to generate 32-bit encoded colors
// - User can declare their own format by #defining the 5 _SHIFT/_MASK macros in their
//   imconfig file.
// - Any setting other than the default will need custom backend support.
//   The only standard backend that supports anything else than the default is DirectX9.
#ifndef IM_COL32_R_SHIFT
# ifdef IMGUI_USE_BGRA_PACKED_COLOR
#  define IM_COL32_R_SHIFT    16
#  define IM_COL32_G_SHIFT    8
#  define IM_COL32_B_SHIFT    0
#  define IM_COL32_A_SHIFT    24
#  define IM_COL32_A_MASK     0xFF000000
# else
#  define IM_COL32_R_SHIFT    0
#  define IM_COL32_G_SHIFT    8
#  define IM_COL32_B_SHIFT    16
#  define IM_COL32_A_SHIFT    24
#  define IM_COL32_A_MASK     0xFF000000
# endif
#endif
"""


def rgba_to_uint32(rgba: RGBA) -> int:
    """
    Convert an RGBA tuple (float, float, float, float) in [0.0, 1.0] to a 32-bit integer
    """
    r, g, b, a = rgba

    if not (0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1 and 0 <= a <= 1):
        raise ValueError("RGBA values must be in [0.0, 1.0]")

    ai = int(round(a * 255))
    ri = int(round(r * 255))
    gi = int(round(g * 255))
    bi = int(round(b * 255))

    return (ai << 24) | (ri << 16) | (gi << 8) | bi


def rgb_to_uint32(rgb: RGB, a=1.0) -> int:
    """
    Convert an RGB tuple (float, float, float) in [0.0, 1.0] to a 32-bit integer.
    """

    r, g, b = rgb

    if not (0.0 <= r <= 1.0 and 0.0 <= g <= 1.0 and 0.0 <= b <= 1.0):
        raise ValueError("RGB values must be in [0.0, 1.0]")

    if not (0.0 <= a <= 1.0):
        raise ValueError("Alpha values must be in [0.0, 1.0]")

    ai = int(round(a * 255))
    ri = int(round(r * 255))
    gi = int(round(g * 255))
    bi = int(round(b * 255))

    return (ai << 24) | (ri << 16) | (gi << 8) | bi


def uint32_to_rgba(value: int) -> RGBA:
    """
    Convert a 32-bit integer to an RGBA tuple (float, float, float, float) in [0.0, 1.0]
    """

    if not (0 <= value <= 0xFFFFFFFF):
        raise ValueError("Value must be a 32-bit integer")

    a = ((value >> 24) & 0xFF) / 255.0
    r = ((value >> 16) & 0xFF) / 255.0
    g = ((value >> 8) & 0xFF) / 255.0
    b = (value & 0xFF) / 255.0

    return r, g, b, a


def uint32_to_rgb(value: int) -> RGB:
    """
    Convert a 32-bit integer to an RGB tuple (float, float, float) in [0.0, 1.0].
    """

    if not (0 <= value <= 0xFFFFFFFF):
        raise ValueError("Value must be a 32-bit integer")

    r = ((value >> 16) & 0xFF) / 255.0
    g = ((value >> 8) & 0xFF) / 255.0
    b = (value & 0xFF) / 255.0

    return r, g, b
