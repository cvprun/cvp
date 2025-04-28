# -*- coding: utf-8 -*-

import os
from os import PathLike
from typing import Optional, Union

from cvp.assets.fonts import (
    get_jbm_font_path,
    get_mdi_font_path,
    get_ngc_b_font_path,
    get_ngc_font_path,
)
from cvp.imgui.fonts.builder import FontBuilder
from cvp.imgui.fonts.font import Font


def add_mixed_font(
    name: str,
    size: int,
    ngc_delta=0,
    mdi_delta=0,
    *,
    use_texture=False,
) -> Font:
    jbm = get_jbm_font_path()
    ngc = get_ngc_font_path()
    mdi = get_mdi_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(jbm)
    builder.add_ttf(ngc, size=size + ngc_delta)
    builder.add_ttf(mdi, size=size + mdi_delta)
    return builder.done(use_texture=use_texture)


def add_jbm_font(name: str, size: int, *, use_texture=False) -> Font:
    jbm = get_jbm_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(jbm)
    return builder.done(use_texture=use_texture)


def add_mdi_font(name: str, size: int, *, use_texture=False) -> Font:
    mdi = get_mdi_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(mdi)
    return builder.done(use_texture=use_texture)


def add_ngc_font(name: str, size: int, *, use_texture=False) -> Font:
    ngc = get_ngc_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(ngc)
    return builder.done(use_texture=use_texture)


def add_ngc_b_font(name: str, size: int, *, use_texture=False) -> Font:
    ngc = get_ngc_b_font_path()
    builder = FontBuilder(name, size)
    builder.add_ttf(ngc)
    return builder.done(use_texture=use_texture)


def add_ttf_file(
    filepath: Union[PathLike[str], str],
    size: int,
    *,
    name: Optional[str] = None,
    use_texture=False,
):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: '{str(filepath)}'")

    if not name:
        name = os.path.basename(filepath)
    assert isinstance(name, str)

    builder = FontBuilder(name, size)
    builder.add_ttf(filepath)
    return builder.done(use_texture=use_texture)
