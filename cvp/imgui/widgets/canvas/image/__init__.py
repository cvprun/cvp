# -*- coding: utf-8 -*-

from cvp.gl.textures.numpy import NumpyTexture
from cvp.imgui.widgets.canvas.controllable import ControllableCanvas


class ImageCanvas(ControllableCanvas):
    def __init__(self):
        super().__init__()
        self._texture = NumpyTexture()

    def do_process(self):
        texture_id = self._texture.texture_id
        p1 = self.p1
        p2 = self.p2
        self._draw_list.add_image(texture_id, p1, p2, uv_min=(0, 0), uv_max=(1, 1))
