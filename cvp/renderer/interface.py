# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class RendererInterface(ABC):
    @abstractmethod
    def render(self, draw_data):
        raise NotImplementedError

    @abstractmethod
    def refresh_font_texture(self):
        raise NotImplementedError

    @abstractmethod
    def shutdown(self):
        self._invalidate_device_objects()

    @abstractmethod
    def _create_device_objects(self):
        raise NotImplementedError

    @abstractmethod
    def _invalidate_device_objects(self):
        raise NotImplementedError
