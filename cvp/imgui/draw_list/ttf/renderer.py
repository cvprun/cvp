# -*- coding: utf-8 -*-

from typing import Optional

from fontTools.ttLib import TTFont

# noinspection PyProtectedMember
from fontTools.ttLib.ttGlyphSet import _TTGlyphGlyf, _TTGlyphSetGlyf

from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.ttf.pen import ImguiPen
from cvp.imgui.draw_list.types import DrawList
from cvp.types.shapes import Point


def draw_ttf_text(
    ttf: TTFont,
    size: int,
    text: str,
    point: Point,
    color=0xFFFFFFFF,
    draw_list: Optional[DrawList] = None,
) -> None:
    if draw_list is None:
        draw_list = get_window_draw_list()
    assert draw_list is not None

    glyph_set = ttf.getGlyphSet()
    assert isinstance(glyph_set, _TTGlyphSetGlyf)

    units_per_em = ttf["head"].unitsPerEm
    assert isinstance(units_per_em, int)

    scale = size / units_per_em

    x = point[0]
    y = point[1] + size

    for char in text:
        glyph_name = ttf.getBestCmap().get(ord(char))
        if glyph_name is None:
            continue

        glyph = glyph_set[glyph_name]
        assert isinstance(glyph, _TTGlyphGlyf)

        width = glyph.width * scale

        pen = ImguiPen(glyph_set, draw_list, scale, x, y, color)
        glyph.draw(pen)
        x += width
