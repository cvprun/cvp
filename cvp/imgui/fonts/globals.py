# -*- coding: utf-8 -*-

from functools import lru_cache

from cvp.imgui.fonts.mapper import FontMapper
from cvp.patterns.singleton import singleton


@singleton
class GlobalFontMapper(FontMapper):
    pass


@lru_cache
def global_font_mapper() -> GlobalFontMapper:
    return GlobalFontMapper()
