# -*- coding: utf-8 -*-

from cvp.assets.fonts import (
    get_jbm_font_path,
    get_jbm_font_ranges_path,
    get_jbm_i_font_path,
    get_jbm_i_font_ranges_path,
    get_mdi_font_glyphs_path,
    get_mdi_font_glyphs_python_path,
    get_mdi_font_path,
    get_mdi_font_ranges_path,
    get_ngc_b_font_path,
    get_ngc_b_font_ranges_path,
    get_ngc_font_path,
    get_ngc_font_ranges_path,
)
from cvp.fonts.ttf import TTF


def create_jbm_ttf():
    return TTF.from_filepath(get_jbm_font_path())


def create_jbm_i_ttf():
    return TTF.from_filepath(get_jbm_i_font_path())


def create_mdi_ttf():
    return TTF.from_filepath(get_mdi_font_path())


def create_ngc_ttf():
    return TTF.from_filepath(get_ngc_font_path())


def create_ngc_b_ttf():
    return TTF.from_filepath(get_ngc_b_font_path())


def _write_default_font_ranges() -> None:
    create_jbm_ttf().write_ranges(get_jbm_font_ranges_path())
    create_jbm_i_ttf().write_ranges(get_jbm_i_font_ranges_path())
    create_mdi_ttf().write_ranges(get_mdi_font_ranges_path())
    create_ngc_ttf().write_ranges(get_ngc_font_ranges_path())
    create_ngc_b_ttf().write_ranges(get_ngc_b_font_ranges_path())


def write_default_font_ranges(*, printer=print, verbose=False) -> None:
    if verbose:
        printer("Writing ranges file...")
    _write_default_font_ranges()
    if verbose:
        printer("Completed writing the ranges file.")


def _write_default_font_glyphs() -> None:
    create_mdi_ttf().write_glyphs(get_mdi_font_glyphs_path())
    create_mdi_ttf().write_glyphs_python(get_mdi_font_glyphs_python_path())


def write_default_font_glyphs(*, printer=print, verbose=False) -> None:
    if verbose:
        printer("Writing glyphs file...")
    _write_default_font_glyphs()
    if verbose:
        printer("Completed writing the glyphs file.")


def write_default_cache_files(*, printer=print, verbose=False) -> None:
    write_default_font_ranges(printer=printer, verbose=verbose)
    write_default_font_glyphs(printer=printer, verbose=verbose)


if __name__ == "__main__":
    write_default_cache_files(verbose=True)
