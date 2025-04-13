# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from os import PathLike
from typing import Optional, Union

from imgui_bundle import imgui

from cvp.imgui.fonts.builder import FontBuilder
from cvp.imgui.fonts.defaults import add_mixed_font
from cvp.imgui.fonts.font import Font


class FontMapper(OrderedDict[str, Font]):
    def close(self):
        fonts = list(self.values())
        self.clear()
        for font in fonts:
            font.close()

    def add_mixed_font(self, name: str, size: int, *, use_texture=False):
        if self.__contains__(name):
            raise KeyError(f"Already exists font key: {name}")

        font = add_mixed_font(name, size, use_texture=use_texture)
        self.__setitem__(name, font)
        return font

    def add_ttf_file(
        self,
        filepath: Union[str, PathLike[str]],
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
        font = builder.done(use_texture=use_texture)

        self.__setitem__(name, font)
        return font

    @staticmethod
    def get_font_global_scale() -> float:
        return imgui.get_io().font_global_scale

    @staticmethod
    def set_font_global_scale(scale: float) -> None:
        imgui.get_io().font_global_scale = scale

    @property
    def font_global_scale(self) -> float:
        return self.get_font_global_scale()

    @font_global_scale.setter
    def font_global_scale(self, scale: float) -> None:
        self.set_font_global_scale(scale)
