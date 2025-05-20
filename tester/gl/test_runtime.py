# -*- coding: utf-8 -*-

from ctypes import CDLL
from unittest import TestCase, main

from OpenGL import GL, platform

from cvp.gl.runtime import get_opengl_dll, get_opengl_process_address


class RuntimeTestCase(TestCase):
    def test_platform_dll(self):
        # noinspection PyUnresolvedReferences
        self.assertEqual(GL.glGetString.DLL, platform.PLATFORM.OpenGL)

    def test_get_opengl_dll(self):
        self.assertIsInstance(get_opengl_dll(), CDLL)

    def test_get_opengl_process_address(self):
        self.assertNotEqual(0, get_opengl_process_address("glGetString"))


if __name__ == "__main__":
    main()
