# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType

from cvp.assets.fonts import mdi


def create_alpha_box_outlines():
    return {
        "": mdi.HELP_BOX_OUTLINE,
        # Underscore
        "_": mdi.MINUS_BOX_OUTLINE,
        # Numeric
        "0": mdi.NUMERIC_0_BOX_OUTLINE,
        "1": mdi.NUMERIC_1_BOX_OUTLINE,
        "2": mdi.NUMERIC_2_BOX_OUTLINE,
        "3": mdi.NUMERIC_3_BOX_OUTLINE,
        "4": mdi.NUMERIC_4_BOX_OUTLINE,
        "5": mdi.NUMERIC_5_BOX_OUTLINE,
        "6": mdi.NUMERIC_6_BOX_OUTLINE,
        "7": mdi.NUMERIC_7_BOX_OUTLINE,
        "8": mdi.NUMERIC_8_BOX_OUTLINE,
        "9": mdi.NUMERIC_9_BOX_OUTLINE,
        # Alpha Uppercase
        "A": mdi.ALPHA_A_BOX_OUTLINE,
        "B": mdi.ALPHA_B_BOX_OUTLINE,
        "C": mdi.ALPHA_C_BOX_OUTLINE,
        "D": mdi.ALPHA_D_BOX_OUTLINE,
        "E": mdi.ALPHA_E_BOX_OUTLINE,
        "F": mdi.ALPHA_F_BOX_OUTLINE,
        "G": mdi.ALPHA_G_BOX_OUTLINE,
        "H": mdi.ALPHA_H_BOX_OUTLINE,
        "I": mdi.ALPHA_I_BOX_OUTLINE,
        "J": mdi.ALPHA_J_BOX_OUTLINE,
        "K": mdi.ALPHA_K_BOX_OUTLINE,
        "L": mdi.ALPHA_L_BOX_OUTLINE,
        "M": mdi.ALPHA_M_BOX_OUTLINE,
        "N": mdi.ALPHA_N_BOX_OUTLINE,
        "O": mdi.ALPHA_O_BOX_OUTLINE,
        "P": mdi.ALPHA_P_BOX_OUTLINE,
        "Q": mdi.ALPHA_Q_BOX_OUTLINE,
        "R": mdi.ALPHA_R_BOX_OUTLINE,
        "S": mdi.ALPHA_S_BOX_OUTLINE,
        "T": mdi.ALPHA_T_BOX_OUTLINE,
        "U": mdi.ALPHA_U_BOX_OUTLINE,
        "V": mdi.ALPHA_V_BOX_OUTLINE,
        "W": mdi.ALPHA_W_BOX_OUTLINE,
        "X": mdi.ALPHA_X_BOX_OUTLINE,
        "Y": mdi.ALPHA_Y_BOX_OUTLINE,
        "Z": mdi.ALPHA_Z_BOX_OUTLINE,
        # Alpha Lowercase
        "a": mdi.ALPHA_A_BOX_OUTLINE,
        "b": mdi.ALPHA_B_BOX_OUTLINE,
        "c": mdi.ALPHA_C_BOX_OUTLINE,
        "d": mdi.ALPHA_D_BOX_OUTLINE,
        "e": mdi.ALPHA_E_BOX_OUTLINE,
        "f": mdi.ALPHA_F_BOX_OUTLINE,
        "g": mdi.ALPHA_G_BOX_OUTLINE,
        "h": mdi.ALPHA_H_BOX_OUTLINE,
        "i": mdi.ALPHA_I_BOX_OUTLINE,
        "j": mdi.ALPHA_J_BOX_OUTLINE,
        "k": mdi.ALPHA_K_BOX_OUTLINE,
        "l": mdi.ALPHA_L_BOX_OUTLINE,
        "m": mdi.ALPHA_M_BOX_OUTLINE,
        "n": mdi.ALPHA_N_BOX_OUTLINE,
        "o": mdi.ALPHA_O_BOX_OUTLINE,
        "p": mdi.ALPHA_P_BOX_OUTLINE,
        "q": mdi.ALPHA_Q_BOX_OUTLINE,
        "r": mdi.ALPHA_R_BOX_OUTLINE,
        "s": mdi.ALPHA_S_BOX_OUTLINE,
        "t": mdi.ALPHA_T_BOX_OUTLINE,
        "u": mdi.ALPHA_U_BOX_OUTLINE,
        "v": mdi.ALPHA_V_BOX_OUTLINE,
        "w": mdi.ALPHA_W_BOX_OUTLINE,
        "x": mdi.ALPHA_X_BOX_OUTLINE,
        "y": mdi.ALPHA_Y_BOX_OUTLINE,
        "z": mdi.ALPHA_Z_BOX_OUTLINE,
    }


@lru_cache
def alpha_box_outlines() -> MappingProxyType[str, str]:
    return MappingProxyType({k: v for k, v in create_alpha_box_outlines().items()})
