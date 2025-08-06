# -*- coding: utf-8 -*-

from math import floor
from typing import Optional, Sequence, Tuple, Union

from imgui_bundle import imgui

from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.draw_list.create import create_draw_list_with_shared_data
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags import color_var
from cvp.imgui.flags.button import ALL_BUTTON_FLAGS
from cvp.imgui.flags.child import BORDERS, ChildFlags
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.flags.window import WindowFlags
from cvp.types.colors import RED_RGB
from cvp.values.delta import DeltaValue


class InputTerminal:
    def __init__(
        self,
        label: str,
        size: Optional[imgui.ImVec2Like] = None,
        child_flags: Union[ChildFlags, int] = BORDERS,
        window_flags: Union[WindowFlags, int] = 0,
        *,
        lineno_begin=0,
        readonly=False,
        autoscroll=False,
        show_lineno=False,
        show_whitespace=False,
    ):
        self._label = label
        self._size = size
        self._child_flags = child_flags
        self._window_flags = window_flags

        self.lineno_begin = lineno_begin
        self.readonly = readonly
        self.autoscroll = autoscroll
        self.show_lineno = show_lineno
        self.show_whitespace = show_whitespace

        self._mouse_wheel = DeltaValue.from_single_value(0.0)
        self._activating = DeltaValue.from_single_value(False)
        self._hovering = DeltaValue.from_single_value(False)
        self._focusing = DeltaValue.from_single_value(False)

        self._draw_list = create_draw_list_with_shared_data()
        self._cursor_pos = 0.0, 0.0
        self._mouse_pos = 0.0, 0.0
        self._canvas_pos = 0.0, 0.0
        self._canvas_size = 0.0, 0.0

        self._control_identifier = type(self).__name__
        self._control_flags = int(ALL_BUTTON_FLAGS)
        self._mouse_dragging_threshold = -1.0
        self._use_only_alt_and_left_dragging = False

        self._terminal_cursor = 0, 0
        self._terminal_size = 0, 0

    @property
    def terminal_cursor(self) -> Tuple[int, int]:
        return self._terminal_cursor

    @property
    def terminal_size(self) -> Tuple[int, int]:
        return self._terminal_size

    def do_process(self, lines: Sequence[str], *, debug=False) -> None:
        with begin_child_context(
            self._label,
            self._size,
            self._child_flags,
            self._window_flags,
        ):
            if imgui.is_window_hovered(ROOT_AND_CHILD_WINDOWS):
                if self._mouse_wheel.update(imgui.get_io().mouse_wheel):
                    if 0 < self._mouse_wheel.value:
                        # Drag Up
                        if imgui.get_scroll_y() < imgui.get_scroll_max_y():
                            self.autoscroll = False
                    elif self._mouse_wheel.value < 0:
                        # Drag Down
                        if imgui.get_scroll_max_y() <= imgui.get_scroll_y():
                            self.autoscroll = True
                    else:
                        assert 0 == self._mouse_wheel.value

            self.do_child_process(lines, debug=debug)

            if self.autoscroll:
                imgui.set_scroll_here_y(1.0)

    def do_child_process(self, lines: Sequence[str], *, debug=False) -> None:
        cursor_pos = imgui.get_cursor_pos()
        mouse_pos = imgui.get_mouse_pos()
        screen_pos = imgui.get_cursor_screen_pos()
        region_size = imgui.get_content_region_avail()

        cx, cy = cursor_pos.x, cursor_pos.y
        mx, my = mouse_pos.x, mouse_pos.y
        sx, sy = screen_pos.x, screen_pos.y
        rw, rh = region_size.x, region_size.y

        if rw == 0 or rh == 0:
            raise ValueError("Invalid region size")

        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(mx, float)
        assert isinstance(my, float)
        assert isinstance(sx, float)
        assert isinstance(sy, float)
        assert isinstance(rw, float)
        assert isinstance(rh, float)
        self._draw_list = get_window_draw_list()
        self._cursor_pos = cx, cy
        self._mouse_pos = mx, my
        self._canvas_pos = sx, sy
        self._canvas_size = rw, rh

        window_padding = imgui.get_style().window_padding
        assert window_padding.x == cx
        assert window_padding.y == cy

        # Using `imgui.invisible_button()` as a convenience
        # 1) it will advance the layout cursor and
        # 2) allows us to use `is_item_hovered()`/`is_item_active()`
        imgui.invisible_button(self._control_identifier, (rw, rh), self._control_flags)
        self._activating.update(imgui.is_item_active())
        self._hovering.update(imgui.is_item_hovered())
        self._focusing.update(imgui.is_item_focused())

        border_color = imgui.get_style_color_vec4(color_var.BORDER)
        text_color = imgui.get_style_color_vec4(color_var.TEXT)
        text_disabled_color = imgui.get_style_color_vec4(color_var.TEXT_DISABLED)

        border_color_u32 = imgui.get_color_u32(border_color)
        text_color_u32 = imgui.get_color_u32(text_color)
        text_disabled_color_u32 = imgui.get_color_u32(text_disabled_color)
        error_color_u32 = imgui.get_color_u32((*RED_RGB, 0.8))

        border_width = imgui.get_style().child_border_size

        item_spacing = imgui.get_style().item_spacing
        item_spacing_x_half = item_spacing.x / 2
        item_spacing_y_half = item_spacing.y / 2

        lineno_width = max(1, len(str(len(lines))))
        lineno_width_dummy_text = "0" * lineno_width
        lineno_text_size = imgui.calc_text_size(lineno_width_dummy_text)

        line_begin_x = lineno_text_size.x + item_spacing.x if self.show_lineno else 0
        line_height = imgui.get_text_line_height() + item_spacing_y_half
        full_text_height = line_height * len(lines)
        screen_width = floor(self._canvas_size[0] / imgui.calc_text_size("0").x)
        screen_height = floor(self._canvas_size[1] / line_height)
        self._terminal_size = screen_width, screen_height

        if self.show_lineno:
            # Draw a vertical line matching the width of the line number area.
            p1 = sx + lineno_text_size.x + item_spacing_x_half, 0.0
            p2 = p1[0], max(sy + rh, full_text_height)
            self._draw_list.add_line(p1, p2, border_color_u32, border_width)

        imgui.set_cursor_pos(cursor_pos)

        clipper = imgui.ListClipper()
        clipper.begin(len(lines))
        while clipper.step():
            for i in range(clipper.display_start, clipper.display_end):
                line_cursor_pos = imgui.get_cursor_pos()
                line_screen_pos = imgui.get_cursor_screen_pos()

                line_cx, line_cy = line_cursor_pos.x, line_cursor_pos.y
                line_sx, line_sy = line_screen_pos.x, line_screen_pos.y

                if self.show_lineno:
                    lineno = self.lineno_begin + i + 1
                    lineno_text = str(lineno).zfill(lineno_width)
                    lineno_pos = line_sx, line_sy
                    self._draw_list.add_text(
                        lineno_pos,
                        text_disabled_color_u32,
                        lineno_text,
                    )

                line_text = lines[i]
                line_text_size = imgui.calc_text_size(line_text)
                line_text_pos = line_sx + line_begin_x, line_sy
                self._draw_list.add_text(line_text_pos, text_color_u32, line_text)

                if debug:
                    x1 = line_screen_pos.x + line_begin_x
                    y1 = line_screen_pos.y
                    x2 = x1 + line_text_size.x
                    y2 = y1 + line_text_size.y
                    p1 = x1, y1
                    p2 = x2, y2
                    self._draw_list.add_rect(p1, p2, error_color_u32)

                # Advance the cursor position manually for the next line.
                next_pos_x = line_cx
                next_pos_y = line_cy + line_text_size.y + item_spacing_y_half
                next_pos = next_pos_x, next_pos_y
                imgui.set_cursor_pos(next_pos)
