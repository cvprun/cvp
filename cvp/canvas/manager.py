# -*- coding: utf-8 -*-

from typing import Optional

from cvp.canvas.canvas import Canvas, CanvasKey
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.canvases import CanvasesPath


class CanvasManager(ResourceManager[CanvasKey, Canvas]):
    _focused_key: Optional[CanvasKey]

    def __init__(self, path: CanvasesPath, *, reload=False, raise_errors=False):
        super().__init__(
            key_type=CanvasKey,
            config_type=Canvas,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._focused_key = None

    @property
    def focused_canvas_key(self):
        return self._focused_key

    @focused_canvas_key.setter
    def focused_canvas_key(self, value: CanvasKey) -> None:
        self._focused_key = value

    @property
    def focused_canvas(self) -> Optional[Canvas]:
        if self._focused_key is None:
            return None
        return self.get(self._focused_key)
