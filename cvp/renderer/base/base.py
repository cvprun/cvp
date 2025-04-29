# -*- coding: utf-8 -*-

from typing import Dict

from imgui_bundle import imgui

from cvp.renderer.base.interface import RendererInterface
from cvp.types.override import override


class BaseRenderer(RendererInterface):
    _keymap: Dict[imgui.Key, int]

    def __init__(self):
        if not imgui.get_current_context():
            raise RuntimeError(
                "No valid ImGui context. Use imgui.create_context() first and/or "
                "imgui.set_current_context()"
            )

        self.io = imgui.get_io()
        self.io.delta_time = 1.0 / 60.0

        self._font_texture = 0
        self._keymap = dict()

        self._create_device_objects()
        self.refresh_font_texture()

    @override
    def _create_device_objects(self) -> None:
        pass

    @override
    def _invalidate_device_objects(self) -> None:
        pass

    @override
    def refresh_font_texture(self) -> None:
        pass

    @override
    def render(self, draw_data: imgui.ImDrawData) -> None:
        pass

    def shutdown(self) -> None:
        self._invalidate_device_objects()
