# -*- coding: utf-8 -*-

from typing import Dict

from imgui_bundle import imgui

from cvp.renderer.interface import RendererInterface
from cvp.types.override import override


class BaseOpenGLRenderer(RendererInterface):
    def __init__(self):
        if not imgui.get_current_context():
            raise RuntimeError(
                "No valid ImGui context. Use imgui.create_context() first and/or "
                "imgui.set_current_context()."
            )
        self.io = imgui.get_io()
        self.io.delta_time = 1.0 / 60.0
        self._font_texture = None
        self._create_device_objects()
        self.refresh_font_texture()
        self._keymap = dict()

    @property
    def keymap(self) -> Dict[int, int]:
        if hasattr(self.io, "key_map"):
            return self.io.key_map
        else:
            return self._keymap

    @override
    def render(self, draw_data):
        pass

    @override
    def refresh_font_texture(self):
        pass

    @override
    def shutdown(self):
        self._invalidate_device_objects()

    @override
    def _create_device_objects(self):
        raise NotImplementedError

    @override
    def _invalidate_device_objects(self):
        raise NotImplementedError
