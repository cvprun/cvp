# -*- coding: utf-8 -*-

import os
from os import PathLike
from typing import Union

from cvp.context.context import Context
from cvp.inspect.member import get_attribute_keys


class RendererContext(Context):
    def __init__(self, home: Union[str, PathLike[str]], *, with_init=False):
        super().__init__(home)
        if with_init:
            self._initialize()

    @classmethod
    def from_context(cls, context: Context, *, with_init=False):
        result = cls.__new__(cls)
        for key in get_attribute_keys(context):
            setattr(result, key, getattr(context, key))
        if with_init:
            result._initialize()
        return result

    def _initialize(self):
        # [IMPORTANT] Avoid 'circular import' issues
        from cvp.imgui.fonts.mapper import FontMapper
        from cvp.renderer.window.mapper import WindowMapper

        self.windows = WindowMapper()
        self.fonts = FontMapper()

    def add_default_fonts(self):
        """
        Must be called after Pygame and Imgui have been initialized.
        """

        normal_text_size_pixels = self.config.font.normal_text_size_pixels
        medium_text_size_pixels = self.config.font.medium_text_size_pixels
        large_text_size_pixels = self.config.font.large_text_size_pixels
        user_font = self.config.font.user_font

        if os.path.isfile(user_font):
            self.fonts.add_normal_ttf(user_font, normal_text_size_pixels)
            self.fonts.add_medium_ttf(user_font, medium_text_size_pixels)
            self.fonts.add_large_ttf(user_font, large_text_size_pixels)
        else:
            self.fonts.add_mixed_normal_text_font(normal_text_size_pixels)
            self.fonts.add_mixed_medium_text_font(medium_text_size_pixels)
            self.fonts.add_mixed_large_text_font(large_text_size_pixels)

        normal_icon_size_pixels = self.config.font.normal_icon_size_pixels
        medium_icon_size_pixels = self.config.font.medium_icon_size_pixels
        large_icon_size_pixels = self.config.font.large_icon_size_pixels

        self.fonts.add_mdi_normal_icon_font(normal_icon_size_pixels)
        self.fonts.add_mdi_medium_icon_font(medium_icon_size_pixels)
        self.fonts.add_mdi_large_icon_font(large_icon_size_pixels)

    def delete_fonts(self):
        self.fonts.close()
