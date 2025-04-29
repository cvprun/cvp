# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from imgui_bundle import imgui


class RendererInterface(ABC):
    @abstractmethod
    def _create_device_objects(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _invalidate_device_objects(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self, draw_data: imgui.ImDrawData) -> None:
        raise NotImplementedError

    @abstractmethod
    def refresh_font_texture(self) -> None:
        raise NotImplementedError
