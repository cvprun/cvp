# -*- coding: utf-8 -*-

from cvp.types.colors import RGB, RGBA


def rgba_to_uint32(rgba: RGBA) -> int:
    """
    Convert an RGBA tuple (float, float, float, float) in [0.0, 1.0] to a 32-bit integer
    """
    r, g, b, a = rgba

    if not (0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1 and 0 <= a <= 1):
        raise ValueError("RGBA values must be in [0.0, 1.0]")

    ri = int(round(r * 255))
    gi = int(round(g * 255))
    bi = int(round(b * 255))
    ai = int(round(a * 255))

    return (ri << 24) | (gi << 16) | (bi << 8) | ai


def rgb_to_uint32(rgb: RGB, a=1.0) -> int:
    """
    Convert an RGB tuple (float, float, float) in [0.0, 1.0] to a 32-bit integer.
    """

    r, g, b = rgb

    if not (0.0 <= r <= 1.0 and 0.0 <= g <= 1.0 and 0.0 <= b <= 1.0):
        raise ValueError("RGB values must be in [0.0, 1.0]")

    if not (0.0 <= a <= 1.0):
        raise ValueError("Alpha values must be in [0.0, 1.0]")

    ri = int(round(r * 255))
    gi = int(round(g * 255))
    bi = int(round(b * 255))
    ai = int(round(a * 255))

    return (ri << 24) | (gi << 16) | (bi << 8) | ai


def uint32_to_rgba(value: int) -> RGBA:
    """
    Convert a 32-bit integer to an RGBA tuple (float, float, float, float) in [0.0, 1.0]
    """

    if not (0 <= value <= 0xFFFFFFFF):
        raise ValueError("Value must be a 32-bit integer")

    r = ((value >> 24) & 0xFF) / 255.0
    g = ((value >> 16) & 0xFF) / 255.0
    b = ((value >> 8) & 0xFF) / 255.0
    a = (value & 0xFF) / 255.0

    return r, g, b, a


def uint32_to_rgb(value: int) -> RGB:
    """
    Convert a 32-bit integer to an RGB tuple (float, float, float) in [0.0, 1.0].
    """

    if not (0 <= value <= 0xFFFFFFFF):
        raise ValueError("Value must be a 32-bit integer")

    r = ((value >> 24) & 0xFF) / 255.0
    g = ((value >> 16) & 0xFF) / 255.0
    b = ((value >> 8) & 0xFF) / 255.0

    return r, g, b
