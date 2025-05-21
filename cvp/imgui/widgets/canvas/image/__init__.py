# -*- coding: utf-8 -*-

from typing import Any, Optional, Sequence

from imgui_bundle import imgui
from numpy import uint8
from numpy.typing import NDArray
from PIL.Image import Image

from cvp.canvas.canvas import CanvasProps
from cvp.gl.textures.numpy import FilePathLike, NumpyTexture
from cvp.imgui.set_window_font_scale import window_font_scale
from cvp.imgui.widgets.canvas.controllable import ControllableCanvas


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

    def get_pixel_info(self, x: int, y: int) -> Sequence[str]:
        if not (0 <= x < self._texture.width):
            return ()
        if not (0 <= y < self._texture.height):
            return ()

        pixel = self._texture.array[y, x]
        match self._texture.channels:
            case 1:
                r = str()
                g = str()
                b = str()
                a = f"{int(pixel):03}"
            case 3:
                r = f"{int(pixel[0]):03}"
                g = f"{int(pixel[1]):03}"
                b = f"{int(pixel[2]):03}"
                a = str()
            case 4:
                r = f"{int(pixel[0]):03}"
                g = f"{int(pixel[1]):03}"
                b = f"{int(pixel[2]):03}"
                a = f"{int(pixel[3]):03}"
            case c:
                raise ValueError(f"Unsupported channels: {c}")
        return r, g, b, a

    def add_pixel_infos(self) -> None:
        if not self._texture.opened:
            return

        pixel = self._props.pixel
        if not pixel.visible:
            return

        if self.zoom < pixel.zoom_threshold:
            return

        cell_size = self.zoom  # size per pixel
        line_height = imgui.get_font_size()
        line_count = 1 + self._texture.channels
        text_box_height = line_height * line_count
        if cell_size < text_box_height:
            return

        padding_h = cell_size - text_box_height
        assert 0.0 <= padding_h

        bg_color = imgui.get_color_u32(pixel.background_color)
        xy_color = imgui.get_color_u32(pixel.offset_color)

        red_color = imgui.get_color_u32(pixel.red_color)
        green_color = imgui.get_color_u32(pixel.green_color)
        blue_color = imgui.get_color_u32(pixel.blue_color)
        alpha_color = imgui.get_color_u32(pixel.alpha_color)
        colors = red_color, green_color, blue_color, alpha_color

        x = self.cx + self.grid_begin_x(1.0)
        y = self.cy + self.grid_begin_y(1.0)
        left = x

        while y < self.ch:
            while x < self.cw:
                image_xy = self.screen_to_canvas_coords((x, y))
                image_x = round(image_xy[0])
                image_y = round(image_xy[1])

                xy_text = f"{image_x},{image_y}"
                xy_size = imgui.calc_text_size(xy_text)
                xy_p1 = x + pixel.thickness, y + pixel.thickness
                xy_p2 = xy_p1[0] + xy_size.x, xy_p1[1] + xy_size.y
                self._draw_list.add_rect_filled(xy_p1, xy_p2, bg_color)
                self._draw_list.add_text(xy_p1, xy_color, xy_text)

                if texts := self.get_pixel_info(image_x, image_y):
                    sizes = [imgui.calc_text_size(t) for t in texts]
                    cursor_y = xy_p2[1]
                    for text, size, color in zip(texts, sizes, colors):
                        if not text:
                            continue
                        p1 = xy_p1[0], cursor_y
                        p2 = p1[0] + size.x, p1[1] + size.y
                        self._draw_list.add_rect_filled(p1, p2, bg_color)
                        self._draw_list.add_text(p1, color, text)
                        cursor_y += line_height
                x += cell_size
            y += cell_size
            x = left
