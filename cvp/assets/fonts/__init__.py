# -*- coding: utf-8 -*-

import os
from functools import lru_cache
from typing import Final

from cvp.assets import get_assets_dir
from cvp.variables import CODEPOINT_GLYPHS_EXTENSION, CODEPOINT_RANGES_EXTENSION


@lru_cache
def get_fonts_dir() -> str:
    return os.path.join(get_assets_dir(), "fonts")


JBM_DIR: Final[str] = "JetBrainsMono"
MDI_DIR: Final[str] = "MaterialDesignIcons"
NGC_DIR: Final[str] = "NanumGothicCoding"

FONT_FILENAME_JBM: Final[str] = "JetBrainsMono[wght]"
FONT_FILENAME_JBM_I: Final[str] = "JetBrainsMono-Italic[wght]"
FONT_FILENAME_MDI: Final[str] = "materialdesignicons-webfont"
FONT_FILENAME_NGC: Final[str] = "NanumGothicCoding"
FONT_FILENAME_NGC_B: Final[str] = "NanumGothicCoding-Bold"

_TTF: Final[str] = ".ttf"
FONT_TTF_FILENAME_JBM: Final[str] = FONT_FILENAME_JBM + _TTF
FONT_TTF_FILENAME_JBM_I: Final[str] = FONT_FILENAME_JBM_I + _TTF
FONT_TTF_FILENAME_MDI: Final[str] = FONT_FILENAME_MDI + _TTF
FONT_TTF_FILENAME_NGC: Final[str] = FONT_FILENAME_NGC + _TTF
FONT_TTF_FILENAME_NGC_B: Final[str] = FONT_FILENAME_NGC_B + _TTF


@lru_cache
def get_jbm_font_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_TTF_FILENAME_JBM)


@lru_cache
def get_jbm_i_font_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_TTF_FILENAME_JBM_I)


@lru_cache
def get_mdi_font_path() -> str:
    return os.path.join(get_fonts_dir(), MDI_DIR, FONT_TTF_FILENAME_MDI)


@lru_cache
def get_ngc_font_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_TTF_FILENAME_NGC)


@lru_cache
def get_ngc_b_font_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_TTF_FILENAME_NGC_B)


_RANGES: Final[str] = CODEPOINT_RANGES_EXTENSION
FONT_RANGES_FILENAME_JBM: Final[str] = FONT_FILENAME_JBM + _RANGES
FONT_RANGES_FILENAME_JBM_I: Final[str] = FONT_FILENAME_JBM_I + _RANGES
FONT_RANGES_FILENAME_MDI: Final[str] = FONT_FILENAME_MDI + _RANGES
FONT_RANGES_FILENAME_NGC: Final[str] = FONT_FILENAME_NGC + _RANGES
FONT_RANGES_FILENAME_NGC_B: Final[str] = FONT_FILENAME_NGC_B + _RANGES


@lru_cache
def get_jbm_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_RANGES_FILENAME_JBM)


@lru_cache
def get_jbm_i_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_RANGES_FILENAME_JBM_I)


@lru_cache
def get_mdi_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), MDI_DIR, FONT_RANGES_FILENAME_MDI)


@lru_cache
def get_ngc_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_RANGES_FILENAME_NGC)


@lru_cache
def get_ngc_b_font_ranges_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_RANGES_FILENAME_NGC_B)


_GLYPHS: Final[str] = CODEPOINT_GLYPHS_EXTENSION
FONT_GLYPHS_FILENAME_JBM: Final[str] = FONT_FILENAME_JBM + _GLYPHS
FONT_GLYPHS_FILENAME_JBM_I: Final[str] = FONT_FILENAME_JBM_I + _GLYPHS
FONT_GLYPHS_FILENAME_MDI: Final[str] = FONT_FILENAME_MDI + _GLYPHS
FONT_GLYPHS_FILENAME_NGC: Final[str] = FONT_FILENAME_NGC + _GLYPHS
FONT_GLYPHS_FILENAME_NGC_B: Final[str] = FONT_FILENAME_NGC_B + _GLYPHS


@lru_cache
def get_jbm_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_GLYPHS_FILENAME_JBM)


@lru_cache
def get_jbm_i_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), JBM_DIR, FONT_GLYPHS_FILENAME_JBM_I)


@lru_cache
def get_mdi_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), MDI_DIR, FONT_GLYPHS_FILENAME_MDI)


@lru_cache
def get_ngc_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_GLYPHS_FILENAME_NGC)


@lru_cache
def get_ngc_b_font_glyphs_path() -> str:
    return os.path.join(get_fonts_dir(), NGC_DIR, FONT_GLYPHS_FILENAME_NGC_B)


@lru_cache
def get_mdi_font_glyphs_python_path() -> str:
    return os.path.join(get_fonts_dir(), "mdi.py")
