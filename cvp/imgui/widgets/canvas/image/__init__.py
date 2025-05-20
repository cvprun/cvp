# -*- coding: utf-8 -*-

from math import floor
from typing import Any, Optional

from imgui_bundle import imgui
from numpy import uint8
from numpy.typing import NDArray
from PIL.Image import Image

from cvp.canvas.canvas import CanvasProps
from cvp.gl.textures.numpy import FilePathLike, NumpyTexture
from cvp.imgui.set_window_font_scale import window_font_scale
from cvp.imgui.widgets.canvas.controllable import ControllableCanvas
from cvp.imgui.draw_list.draw_centered_text import draw_centered_text


class ImageCanvas(ControllableCanvas):
    def __init__(self, props: Optional[CanvasProps] = None):
        super().__init__()
        self._texture = NumpyTexture()
        self._props = props if props else CanvasProps()

    @property
    def opened(self) -> bool:
        return self._texture.opened

    def open_with_empty(self, width: int, height: int, channels: int) -> None:
        if self._texture.opened:
            self._texture.close()
        assert not self._texture.opened
        self._texture.open_with_empty(width, height, channels)

    def open_with_filled(
        self,
        width: int,
        height: int,
        channels: int,
        color: Any,
    ) -> None:
        if self._texture.opened:
            self._texture.close()
        assert not self._texture.opened
        self._texture.open_with_filled(width, height, channels, color)

    def open_with_file(self, file: FilePathLike) -> None:
        if self._texture.opened:
            self._texture.close()
        assert not self._texture.opened
        self._texture.open_with_file(file)

    def open_with_pillow(self, image: Image) -> None:
        if self._texture.opened:
            self._texture.close()
        assert not self._texture.opened
        self._texture.open_with_pillow(image)

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
            self.add_rect_filled()
            self.add_grid_x()
            self.add_grid_y()
            self.add_axis_x()
            self.add_axis_y()
            self.add_image()
            self.add_grid_pixels()

        self.add_pixel_infos()

    def add_rect_filled(self) -> None:
        color = imgui.get_color_u32(self._props.background_color)
        x1, y1, x2, y2 = self.canvas_roi
        p1 = x1, y1
        p2 = x2, y2
        self._draw_list.add_rect_filled(p1, p2, color)

    def add_grid_x(self) -> None:
        grid_x = self._props.grid_x
        if not grid_x.visible:
            return

        color = imgui.get_color_u32(grid_x.color)
        for line in self.vertical_grid_lines(grid_x.step):
            p1 = line[0], line[1]
            p2 = line[2], line[3]
            self._draw_list.add_line(p1, p2, color, grid_x.thickness)

    def add_grid_y(self) -> None:
        grid_y = self._props.grid_y
        if not grid_y.visible:
            return

        color = imgui.get_color_u32(grid_y.color)
        for line in self.horizontal_grid_lines(grid_y.step):
            p1 = line[0], line[1]
            p2 = line[2], line[3]
            self._draw_list.add_line(p1, p2, color, grid_y.thickness)

    def add_axis_x(self) -> None:
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

    def add_axis_y(self) -> None:
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

    def add_image(self):
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

    def add_grid_pixels(self) -> None:
        pixel = self._props.pixel
        if not pixel.visible:
            return

        if self.zoom < pixel.zoom_threshold:
            return

        color = imgui.get_color_u32(pixel.color)

        h_lines = self.horizontal_grid_lines(1.0)
        v_lines = self.vertical_grid_lines(1.0)

        for line in h_lines + v_lines:
            p1 = line[0], line[1]
            p2 = line[2], line[3]
            self._draw_list.add_line(p1, p2, color, pixel.thickness)

    def add_pixel_infos(self) -> None:
        if not self._texture.opened:
            return

        pixel = self._props.pixel
        if not pixel.visible:
            return

        if self.zoom < pixel.zoom_threshold:
            return

        color = imgui.get_color_u32(pixel.color)
        red = imgui.get_color_u32(pixel.red_color)
        green = imgui.get_color_u32(pixel.green_color)
        blue = imgui.get_color_u32(pixel.blue_color)

        h_lines = self.horizontal_grid_lines(1.0)
        v_lines = self.vertical_grid_lines(1.0)

        for yi in range(1, len(h_lines)):
            y1 = h_lines[yi - 1][1]
            y2 = h_lines[yi - 0][1]

            for vi in range(1, len(v_lines)):
                x1 = v_lines[vi - 1][0]
                x2 = v_lines[vi - 0][0]

                image_point = self.screen_to_canvas_coords((x1, y1))
                image_x = floor(image_point[0])
                image_y = floor(image_point[1])

                if not (0 <= image_x < self._texture.width):
                    continue
                if not (0 <= image_y < self._texture.height):
                    continue

                r, g, b, a = self._texture.array[image_y, image_x]
                color_text = f"{r:02X}{g:02X}{b:02X}{a:02X}"

                r_text = str(int(r))
                g_text = str(int(g))
                b_text = str(int(b))
                a_text = str(int(a))

                r_size = imgui.calc_text_size(r_text)
                g_size = imgui.calc_text_size(g_text)
                b_size = imgui.calc_text_size(b_text)
                a_size = imgui.calc_text_size(a_text)

                draw_centered_text(self._draw_list, x1, y1, x2, y2, color, color_text)
