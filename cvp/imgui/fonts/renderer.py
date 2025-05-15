# -*- coding: utf-8 -*-

from typing import Final

from fontTools.ttLib import TTFont

from cvp.imgui.fonts.pen import ImguiPen

SPACE_CHAR: Final[str] = chr(0x32)
assert SPACE_CHAR == " "


class ImguiFontRenderer:
    def __init__(self, font_path, size=12):
        self.font = TTFont(font_path)
        self.size = size
        self.units_per_em = self.font["head"].unitsPerEm
        self.scale = size / self.units_per_em

    def render_text(self, draw_list, text, x, y, color=0xFFFFFFFF):
        glyph_set = self.font.getGlyphSet()
        current_x = x

        for char in text:
            if char == SPACE_CHAR:
                current_x += self.size * 0.5
                continue

            try:
                glyph_name = self.font.getBestCmap().get(ord(char))
                if glyph_name is None:
                    current_x += self.size * 0.5
                    continue

                glyph = glyph_set[glyph_name]
                width = glyph.width * self.scale

                pen = ImguiPen(glyph_set, draw_list, self.scale, current_x, y, color)
                glyph.draw(pen)

                current_x += width

            except Exception as e:
                print(f"Error rendering character '{char}': {e}")
                current_x += self.size * 0.5
