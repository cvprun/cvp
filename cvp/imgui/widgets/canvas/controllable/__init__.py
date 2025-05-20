# -*- coding: utf-8 -*-

from math import fmod
from typing import Tuple, Union

from imgui_bundle import imgui

from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.draw_list.create import create_draw_list_with_shared_data
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags.button import ALL_BUTTON_FLAGS
from cvp.imgui.flags.input_text import READ_ONLY
from cvp.imgui.flags.mouse_button import (
    MOUSE_LEFT,
    MOUSE_MIDDLE,
    MOUSE_RIGHT,
    MouseButton,
)
from cvp.imgui.input_float2 import input_float2
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.slider_float import slider_float
from cvp.imgui.widgets.canvas.controllable.props import ControllableProps
from cvp.imgui.widgets.canvas.controllable.result import ControllableResult
from cvp.types.shapes import Point, Rect
from cvp.variables import (
    CANVAS_ZOOM_FACTOR,
    CANVAS_ZOOM_MAX_SCALE,
    CANVAS_ZOOM_MIN_SCALE,
)


class ControllableCanvas(ControllableProps):
    def __init__(self):
        super().__init__()

        self._draw_list = create_draw_list_with_shared_data()

        self._pan_label = "Pan"
        self._pan_speed = 0.1
        self._pan_min = 0.0
        self._pan_max = 0.0
        self._pan_fmt = "%.1f"
        self._pan_flags = 0

        self._zoom_label = "Zoom"
        self._zoom_factor = CANVAS_ZOOM_FACTOR
        self._zoom_min = CANVAS_ZOOM_MIN_SCALE
        self._zoom_max = CANVAS_ZOOM_MAX_SCALE
        self._zoom_fmt = "%.2f"
        self._zoom_flags = 0

        self._local_pos_label = "Local"
        self._local_pos_x = 0.0
        self._local_pos_y = 0.0
        self._local_pos_fmt = "%.3f"
        self._local_pos_flags = READ_ONLY

        self._canvas_pos_label = "Canvas"
        self._canvas_pos_x = 0.0
        self._canvas_pos_y = 0.0
        self._canvas_pos_fmt = "%.3f"
        self._canvas_pos_flags = READ_ONLY

        self._control_identifier = type(self).__name__
        self._control_flags = int(ALL_BUTTON_FLAGS)
        self._mouse_dragging_threshold = -1.0
        self._use_only_alt_and_left_dragging = False

    @property
    def frame_padding(self) -> Tuple[int, int]:
        padding = imgui.get_style().frame_padding
        return int(padding.x), int(padding.y)

    @property
    def window_padding(self) -> Tuple[int, int]:
        padding = imgui.get_style().window_padding
        return int(padding.x), int(padding.y)

    @property
    def item_spacing(self) -> Tuple[int, int]:
        spacing = imgui.get_style().item_spacing
        return int(spacing.x), int(spacing.y)

    @property
    def item_inner_spacing(self) -> Tuple[int, int]:
        spacing = imgui.get_style().item_inner_spacing
        return int(spacing.x), int(spacing.y)

    def drag_pan(self, dryrun=False):
        retval = drag_float2(
            self._pan_label,
            self.pan_x,
            self.pan_y,
            self._pan_speed,
            self._pan_min,
            self._pan_max,
            self._pan_fmt,
            self._pan_flags,
        )
        if not dryrun and retval:
            self.pan_x = retval.value0
            self.pan_y = retval.value1
        return retval

    def slider_zoom(self, dryrun=False):
        retval = slider_float(
            self._zoom_label,
            self.zoom,
            self._zoom_min,
            self._zoom_max,
            self._zoom_fmt,
            self._zoom_flags,
        )
        if not dryrun and retval:
            self.zoom = retval.value
        return retval

    def input_local_pos(self):
        return input_float2(
            self._local_pos_label,
            self._local_pos_x,
            self._local_pos_y,
            self._local_pos_fmt,
            self._local_pos_flags,
        )

    def input_canvas_pos(self):
        return input_float2(
            self._canvas_pos_label,
            self._canvas_pos_x,
            self._canvas_pos_y,
            self._canvas_pos_fmt,
            self._canvas_pos_flags,
        )

    def tree_debugging(self) -> None:
        if imgui.tree_node("Debugging"):
            try:
                message = self.as_unformatted_text()
                imgui.text_unformatted(message.strip())
            finally:
                imgui.tree_pop()

    def render_controllers(self, dryrun=False, debugging=False) -> ControllableResult:
        pan = self.drag_pan(dryrun=dryrun)
        zoom = self.slider_zoom(dryrun=dryrun)

        with style_disable_input_context():
            self.input_local_pos()
            self.input_canvas_pos()

        if debugging:
            self.tree_debugging()

        changed = pan.clicked or zoom.changed
        return ControllableResult(changed, pan.value0, pan.value1, zoom.value)

    def point_in_canvas_rect(self, point: Point) -> bool:
        x, y = point
        cx, cy = self._canvas_pos
        cw, ch = self._canvas_size
        return cx <= x <= cx + cw and cy <= y <= cy + ch

    def canvas_to_screen_coords(self, point: Point) -> Point:
        x = self.cx + (point[0] + self.pan_x) * self.zoom
        y = self.cy + (point[1] + self.pan_y) * self.zoom
        return x, y

    def local_origin_to_screen_coords(self) -> Point:
        return self.canvas_to_screen_coords((0.0, 0.0))

    def canvas_to_screen_roi(self, roi: Rect) -> Rect:
        p1 = self.canvas_to_screen_coords((roi[0], roi[1]))
        p2 = self.canvas_to_screen_coords((roi[2], roi[3]))
        return p1[0], p1[1], p2[0], p2[1]

    def screen_to_canvas_coords(self, point: Point) -> Point:
        x = (point[0] - self.cx) / self.zoom - self.pan_x
        y = (point[1] - self.cy) / self.zoom - self.pan_y
        return x, y

    def screen_to_canvas_roi(self, roi: Rect) -> Rect:
        p1 = self.screen_to_canvas_coords((roi[0], roi[1]))
        p2 = self.screen_to_canvas_coords((roi[2], roi[3]))
        return p1[0], p1[1], p2[0], p2[1]

    def mouse_to_canvas_coords(self) -> Point:
        return self.screen_to_canvas_coords(self._mouse_pos)

    def is_mouse_dragging(self, button: Union[MouseButton, int]) -> bool:
        if isinstance(button, MouseButton):
            button = int(button)
        assert isinstance(button, int)
        assert self._mouse_dragging_threshold != 0.0
        return imgui.is_mouse_dragging(button, self._mouse_dragging_threshold)

    def vertical_grid_lines(self, step: float):
        if step <= 0:
            raise ValueError("The 'step' value must be greater than 0")
        if self.zoom <= 0:
            raise ValueError("The 'zoom' value must be greater than 0")

        retval = list()
        x = fmod(self.pan_x * self.zoom, step * self.zoom)
        while x < self.cw:
            x1 = self.cx + x
            y1 = self.cy
            x2 = self.cx + x
            y2 = self.cy + self.ch
            retval.append((x1, y1, x2, y2))
            x += step * self.zoom
        return retval

    def horizontal_grid_lines(self, step: float):
        if step <= 0:
            raise ValueError("The 'step' value must be greater than 0")
        if self.zoom <= 0:
            raise ValueError("The 'zoom' value must be greater than 0")

        retval = list()
        y = fmod(self.pan_y * self.zoom, step * self.zoom)
        while y < self.ch:
            x1 = self.cx
            y1 = self.cy + y
            x2 = self.cx + self.cw
            y2 = self.cy + y
            retval.append((x1, y1, x2, y2))
            y += step * self.zoom
        return retval

    def update_state(self) -> ControllableResult:
        mouse_pos = imgui.get_mouse_pos()
        screen_pos = imgui.get_cursor_screen_pos()
        region_size = imgui.get_content_region_avail()

        mx, my = mouse_pos.x, mouse_pos.y
        cx, cy = screen_pos.x, screen_pos.y
        cw, ch = region_size.x, region_size.y

        if cw == 0 or ch == 0:
            raise ValueError("Invalid region size")

        assert isinstance(mx, float)
        assert isinstance(my, float)
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)
        self._draw_list = get_window_draw_list()
        self._mouse_pos = mx, my
        self._canvas_pos = cx, cy
        self._canvas_size = cw, ch

        # Using `imgui.invisible_button()` as a convenience
        # 1) it will advance the layout cursor and
        # 2) allows us to use `is_item_hovered()`/`is_item_active()`
        imgui.invisible_button(self._control_identifier, (cw, ch), self._control_flags)
        self._activating.update(imgui.is_item_active())
        self._hovering.update(imgui.is_item_hovered())
        self._focusing.update(imgui.is_item_focused())

        io = imgui.get_io()

        if self._focusing.value:
            left_down = bool(io.mouse_down[MOUSE_LEFT])
            right_down = bool(io.mouse_down[MOUSE_RIGHT])
            middle_down = bool(io.mouse_down[MOUSE_MIDDLE])

            self._left_button.update(left_down, self._mouse_pos)
            self._middle_button.update(middle_down, self._mouse_pos)
            self._right_button.update(right_down, self._mouse_pos)

            self._shift_down.update(io.key_shift)
            self._ctrl_down.update(io.key_ctrl)
            self._alt_down.update(io.key_alt)

        zoom = self.zoom
        pan_x = self.pan_x
        pan_y = self.pan_y
        try:
            if self.activating:
                if self.middle_dragging:
                    pan_x += io.mouse_delta.x / zoom
                    pan_y += io.mouse_delta.y / zoom
                elif self._use_only_alt_and_left_dragging:
                    if self.only_alt_down and self.left_dragging:
                        pan_x += io.mouse_delta.x / zoom
                        pan_y += io.mouse_delta.y / zoom

            if self.hovering and io.mouse_wheel != 0:
                if io.mouse_wheel > 0:
                    zoom *= self._zoom_factor ** abs(io.mouse_wheel)
                elif io.mouse_wheel < 0:
                    zoom /= self._zoom_factor ** abs(io.mouse_wheel)

            if zoom > self._zoom_max:
                zoom = self._zoom_max
            elif zoom < self._zoom_min:
                zoom = self._zoom_min

            if zoom != self.zoom:
                # Apply zoom centered on the mouse position.
                dx1 = (mx - cx) / self.zoom
                dy1 = (my - cy) / self.zoom
                dx2 = (mx - cx) / zoom
                dy2 = (my - cy) / zoom
                pan_x += dx2 - dx1
                pan_y += dy2 - dy1
        finally:
            self.zoom = zoom
            self.pan_x = pan_x
            self.pan_y = pan_y

        if self._hovering.value:
            self._local_pos_x = mx - cx
            self._local_pos_y = my - cy

            scx, scy = self.screen_to_canvas_coords((mx, my))
            self._canvas_pos_x = scx
            self._canvas_pos_y = scy

        changed = self._pan_x.changed or self._pan_y.changed or self._zoom.changed
        return ControllableResult(changed, self.pan_x, self.pan_y, self.zoom)
