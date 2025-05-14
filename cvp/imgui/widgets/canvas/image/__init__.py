# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui
from numpy import uint8
from numpy.typing import NDArray

from cvp.canvas.canvas import CanvasProps
from cvp.gl.textures.numpy import FilePathLike, NumpyTexture
from cvp.imgui.set_window_font_scale import window_font_scale
from cvp.imgui.widgets.canvas.controllable import ControllableCanvas


class ImageCanvas(ControllableCanvas):
    def __init__(self, props: Optional[CanvasProps] = None):
        super().__init__()
        self._texture = NumpyTexture()
        self._props = props if props else CanvasProps()

    def open_with_empty(self, width: int, height: int, channels: int) -> None:
        if self._texture.opened:
            self._texture.close()
        assert not self._texture.opened
        self._texture.open_with_empty(width, height, channels)

    def open_with_file(self, file: FilePathLike) -> None:
        if self._texture.opened:
            self._texture.close()
        assert not self._texture.opened
        self._texture.open_with_file(file)

    def open_with_numpy(self, array: NDArray[uint8], *, use_deepcopy=False) -> None:
        if self._texture.opened:
            self._texture.close()
        assert not self._texture.opened
        self._texture.open_with_numpy(array, use_deepcopy=use_deepcopy)

    def close(self) -> None:
        if self._texture.opened:
            self._texture.close()
        assert not self._texture.opened

    def reset_controllers(self):
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0

        self._props.control.pan_x = 0.0
        self._props.control.pan_y = 0.0
        self._props.control.zoom = 1.0

    def do_process_controllers(self, debugging=False) -> None:
        if result := self.render_controllers(debugging=debugging):
            self._props.control.pan_x = result.pan_x
            self._props.control.pan_y = result.pan_y
            self._props.control.zoom = result.zoom

    def do_process(self):
        if result := self.update_state():
            self._props.control.pan_x = result.pan_x
            self._props.control.pan_y = result.pan_y
            self._props.control.zoom = result.zoom

        with window_font_scale(self.zoom):
            self.fill()
            self.draw_grid_x()
            self.draw_grid_y()
            self.draw_axis_x()
            self.draw_axis_y()
            self.draw_texture()

    def fill(self) -> None:
        color = imgui.get_color_u32(self._props.background_color)
        x1, y1, x2, y2 = self.canvas_roi
        p1 = x1, y1
        p2 = x2, y2
        self._draw_list.add_rect_filled(p1, p2, color)

    def draw_grid_x(self) -> None:
        grid_x = self._props.grid_x
        if not grid_x.visible:
            return

        color = imgui.get_color_u32(grid_x.color)
        for line in self.vertical_grid_lines(grid_x.step):
            p1 = line[0], line[1]
            p2 = line[2], line[3]
            self._draw_list.add_line(p1, p2, color, grid_x.thickness)

    def draw_grid_y(self) -> None:
        grid_y = self._props.grid_y
        if not grid_y.visible:
            return

        color = imgui.get_color_u32(grid_y.color)
        for line in self.horizontal_grid_lines(grid_y.step):
            p1 = line[0], line[1]
            p2 = line[2], line[3]
            self._draw_list.add_line(p1, p2, color, grid_y.thickness)

    def draw_axis_x(self) -> None:
        axis_x = self._props.axis_x
        if not axis_x.visible:
            return

        origin_y = self.local_origin_to_screen_coords()[1]
        color = imgui.get_color_u32(axis_x.color)

        x1 = self.cx
        y1 = origin_y
        x2 = self.cx + self.cw
        y2 = origin_y

        p1 = x1, y1
        p2 = x2, y2
        self._draw_list.add_line(p1, p2, color, axis_x.thickness)

    def draw_axis_y(self) -> None:
        axis_y = self._props.axis_y
        if not axis_y.visible:
            return

        origin_x = self.local_origin_to_screen_coords()[0]
        color = imgui.get_color_u32(axis_y.color)

        x1 = origin_x
        y1 = self.cy
        x2 = origin_x
        y2 = self.cy + self.ch

        p1 = x1, y1
        p2 = x2, y2
        self._draw_list.add_line(p1, p2, color, axis_y.thickness)

    def draw_texture(self):
        if not self._texture.opened:
            return

        texture_id = self._texture.texture_id
        assert texture_id != 0

        origin = self.local_origin_to_screen_coords()
        width = float(self._texture.width)
        height = float(self._texture.height)
        size = self.canvas_to_screen_coords((width, height))

        self._draw_list.add_image(
            texture_id,
            origin,
            size,
            uv_min=(0, 0),
            uv_max=(1, 1),
        )
