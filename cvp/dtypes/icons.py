# -*- coding: utf-8 -*-

from types import MappingProxyType
from typing import Final

from cvp.fonts.glyphs import mdi
from cvp.fonts.types import IconCode

DTYPE_ICON_MAPPING: Final[MappingProxyType[str, IconCode]] = MappingProxyType(
    {
        "": mdi.HELP,
        # Underscore
        "_": mdi.MINUS,
        # Numeric
        "0": mdi.NUMERIC_0,
        "1": mdi.NUMERIC_1,
        "2": mdi.NUMERIC_2,
        "3": mdi.NUMERIC_3,
        "4": mdi.NUMERIC_4,
        "5": mdi.NUMERIC_5,
        "6": mdi.NUMERIC_6,
        "7": mdi.NUMERIC_7,
        "8": mdi.NUMERIC_8,
        "9": mdi.NUMERIC_9,
        # Alpha Uppercase
        "A": mdi.ALPHA_A,
        "B": mdi.ALPHA_B,
        "C": mdi.ALPHA_C,
        "D": mdi.ALPHA_D,
        "E": mdi.ALPHA_E,
        "F": mdi.ALPHA_F,
        "G": mdi.ALPHA_G,
        "H": mdi.ALPHA_H,
        "I": mdi.ALPHA_I,
        "J": mdi.ALPHA_J,
        "K": mdi.ALPHA_K,
        "L": mdi.ALPHA_L,
        "M": mdi.ALPHA_M,
        "N": mdi.ALPHA_N,
        "O": mdi.ALPHA_O,
        "P": mdi.ALPHA_P,
        "Q": mdi.ALPHA_Q,
        "R": mdi.ALPHA_R,
        "S": mdi.ALPHA_S,
        "T": mdi.ALPHA_T,
        "U": mdi.ALPHA_U,
        "V": mdi.ALPHA_V,
        "W": mdi.ALPHA_W,
        "X": mdi.ALPHA_X,
        "Y": mdi.ALPHA_Y,
        "Z": mdi.ALPHA_Z,
        # Alpha Lowercase
        "a": mdi.ALPHA_A,
        "b": mdi.ALPHA_B,
        "c": mdi.ALPHA_C,
        "d": mdi.ALPHA_D,
        "e": mdi.ALPHA_E,
        "f": mdi.ALPHA_F,
        "g": mdi.ALPHA_G,
        "h": mdi.ALPHA_H,
        "i": mdi.ALPHA_I,
        "j": mdi.ALPHA_J,
        "k": mdi.ALPHA_K,
        "l": mdi.ALPHA_L,
        "m": mdi.ALPHA_M,
        "n": mdi.ALPHA_N,
        "o": mdi.ALPHA_O,
        "p": mdi.ALPHA_P,
        "q": mdi.ALPHA_Q,
        "r": mdi.ALPHA_R,
        "s": mdi.ALPHA_S,
        "t": mdi.ALPHA_T,
        "u": mdi.ALPHA_U,
        "v": mdi.ALPHA_V,
        "w": mdi.ALPHA_W,
        "x": mdi.ALPHA_X,
        "y": mdi.ALPHA_Y,
        "z": mdi.ALPHA_Z,
    }
)
