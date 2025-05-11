# -*- coding: utf-8 -*-

from cvp.canvas.canvas import CanvasKey
from cvp.context.mixins._base import BaseContextMixin


class CanvasMixin(BaseContextMixin):
    @property
    def selected_canvas_key(self) -> CanvasKey:
        return CanvasKey(self._config.canvas.selected_uuid)

    @selected_canvas_key.setter
    def selected_canvas_key(self, value: CanvasKey) -> None:
        self._config.canvas.selected_uuid = str(value)

    @property
    def selected_canvas(self):
        return self._canvases.get(self.selected_canvas_key)
