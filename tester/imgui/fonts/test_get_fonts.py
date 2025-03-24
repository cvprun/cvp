# -*- coding: utf-8 -*-

from unittest import TestCase, main

from imgui_bundle import imgui
from numpy import ndarray, uint8

from cvp.imgui.fonts.get_fonts import (
    get_fonts,
    get_tex_data_as_raw_rgba32,
    get_tex_data_as_rgba32,
)


class GetFontsTestCase(TestCase):
    def setUp(self):
        imgui.create_context()

    def test_get_fonts(self):
        fonts = get_fonts()
        self.assertIsNotNone(fonts)
        self.assertIsInstance(fonts, imgui.ImFontAtlas)

    def test_get_tex_data_as_rgba32(self):
        tex = get_tex_data_as_rgba32()
        self.assertIsInstance(tex, ndarray)
        self.assertEqual(tex.dtype, uint8)
        self.assertEqual(3, len(tex.shape))

        height, width, channels = tex.shape
        self.assertLess(0, height)
        self.assertLess(0, width)
        self.assertEqual(4, channels)  # RGBA32 == 4bytes

        data = tex.tobytes()
        self.assertIsInstance(data, bytes)
        self.assertEqual(height * width * channels, len(data))

        tex2_info = get_tex_data_as_raw_rgba32()
        self.assertEqual(width, tex2_info[0])
        self.assertEqual(height, tex2_info[1])
        self.assertEqual(data, tex2_info[2])


if __name__ == "__main__":
    main()
