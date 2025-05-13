# -*- coding: utf-8 -*-

from unittest import TestCase, main

from OpenGL import GL

from cvp.gl.textures.filter import TextureFilter, create_texture_filter_mapping


class FilterTestCase(TestCase):
    def test_keys(self):
        mapping_keys = set(create_texture_filter_mapping().keys())
        filters = set(TextureFilter)
        self.assertSetEqual(filters, mapping_keys)

    def test_values(self):
        mapping_values = set(create_texture_filter_mapping().values())
        values = {
            GL.GL_NEAREST,
            GL.GL_LINEAR,
            GL.GL_NEAREST_MIPMAP_NEAREST,
            GL.GL_LINEAR_MIPMAP_NEAREST,
            GL.GL_NEAREST_MIPMAP_LINEAR,
            GL.GL_LINEAR_MIPMAP_LINEAR,
        }
        self.assertSetEqual(values, mapping_values)

    def test_integers(self):
        mapping_values = set(create_texture_filter_mapping().values())
        numbers = set(map(lambda x: int(x), mapping_values))
        self.assertSetEqual(mapping_values, numbers)


if __name__ == "__main__":
    main()
