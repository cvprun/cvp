# -*- coding: utf-8 -*-

from io import StringIO
from math import floor
from typing import Optional, Sequence, Union

from imgui_bundle import imgui

from cvp.encoding.ascii import (
    DIGIT_ZERO,
    HT,
    LF,
    MIDDLE_DOT,
    PILCROW_SIGN,
    RIGHT_POINTING_DOUBLE_ANGLE_QUOTATION_MARK,
    SPACE,
)
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.draw_list.create import create_draw_list_with_shared_data
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags.child import BORDERS, ChildFlags
from cvp.imgui.flags.mouse_button import MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT
from cvp.imgui.flags.window import WindowFlags
from cvp.imgui.get_style import (
    get_border_u32,
    get_border_width,
    get_char_width,
    get_item_spacing_x,
    get_item_spacing_x_half,
    get_line_height,
    get_text_disabled_u32,
    get_text_line_height,
    get_text_selected_bg_u32,
    get_text_u32,
)
from cvp.imgui.tooltip import tooltip_text_wrapped
from cvp.terminal.ansi.sgr.builder import SgrBuilder
from cvp.terminal.palette import TerminalPalette
from cvp.terminal.selection import TerminalSelection
from cvp.terminal.style import TerminalStyle
from cvp.types.shapes import Point, Size
from cvp.types.shapes_i import SizeI
from cvp.values.delta import DeltaValue
from cvp.values.drag_button import DragButton


class AnsiEscapeEditor:
    """
    https://en.wikipedia.org/wiki/ANSI_escape_code
    """

    def __init__(
        self,
        label: str,
        size: Optional[imgui.ImVec2Like] = None,
        child_flags: Union[ChildFlags, int] = BORDERS,
        window_flags: Union[WindowFlags, int] = 0,
        *,
        autoscroll=False,
        tabsize=4,
        show_lineno=False,
        show_whitespace=False,
        show_eol=False,
        show_block_roi=False,
        show_text_roi=False,
        show_error=False,
        palette: Optional[TerminalPalette] = None,
    ):
        self._builder = SgrBuilder(
            show_whitespace=show_whitespace,
            text_disabled_color=get_text_disabled_u32(),
            tabsize=tabsize,
            linefeed=LF,
            space=SPACE,
            tab=HT,
            empty_char=chr(SPACE),
            tab_char=chr(RIGHT_POINTING_DOUBLE_ANGLE_QUOTATION_MARK),
            whitespace_char=chr(MIDDLE_DOT),
        )
        self._border_color = get_border_u32()
        self._text_color = get_text_u32()
        self._text_selected_bg_color = get_text_selected_bg_u32()
        self._eol_char = chr(PILCROW_SIGN)

        self._autoscroll = autoscroll
        self._show_lineno = show_lineno
        self._show_eol = show_eol
        self._show_block_roi = show_block_roi
        self._show_line_roi = show_text_roi
        self._show_error = show_error

        self._label = label
        self._size = size
        self._child_flags = child_flags
        self._window_flags = window_flags

        self._left_button = DragButton()
        self._middle_button = DragButton()
        self._right_button = DragButton()

        self._shift_down = DeltaValue.from_single_value(False)
        self._ctrl_down = DeltaValue.from_single_value(False)
        self._alt_down = DeltaValue.from_single_value(False)

        self._draw_list = create_draw_list_with_shared_data()
        self._mouse_wheel = DeltaValue.from_single_value(0.0)
        self._mouse_pos = 0.0, 0.0
        self._cursor_pos = 0.0, 0.0
        self._cursor_screen_pos = 0.0, 0.0
        self._content_region_size = 0.0, 0.0

        self._cursor_lineno = 0
        self._cursor_column = 0
        self._terminal_size = 0, 0

        self._palette = palette if palette is not None else TerminalPalette()

    @property
    def autoscroll(self) -> bool:
        return self._autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self._autoscroll = value

    @property
    def show_lineno(self) -> bool:
        return self._show_lineno

    @show_lineno.setter
    def show_lineno(self, value: bool) -> None:
        self._show_lineno = value

    @property
    def show_eol(self) -> bool:
        return self._show_eol

    @show_eol.setter
    def show_eol(self, value: bool) -> None:
        self._show_eol = value

    @property
    def show_whitespace(self) -> bool:
        return self._builder.show_whitespace

    @show_whitespace.setter
    def show_whitespace(self, value: bool) -> None:
        self._builder.show_whitespace = value

    @property
    def show_block_roi(self) -> bool:
        return self._show_block_roi

    @show_block_roi.setter
    def show_block_roi(self, value: bool) -> None:
        self._show_block_roi = value

    @property
    def show_line_roi(self) -> bool:
        return self._show_line_roi

    @show_line_roi.setter
    def show_line_roi(self, value: bool) -> None:
        self._show_line_roi = value

    @property
    def show_error(self) -> bool:
        return self._show_error

    @show_error.setter
    def show_error(self, value: bool) -> None:
        self._show_error = value

    @property
    def text_disabled_color(self) -> int:
        return self._builder.text_disabled_color

    @property
    def text_selected_bg_color(self) -> int:
        return self._text_selected_bg_color

    @property
    def border_color(self) -> int:
        return self._border_color

    @property
    def text_color(self) -> int:
        return self._text_color

    @property
    def mouse_pos(self) -> Size:
        return self._mouse_pos

    @property
    def cursor_pos(self) -> Size:
        return self._cursor_pos

    @property
    def cursor_screen_pos(self) -> Size:
        return self._cursor_screen_pos

    @property
    def content_region_size(self) -> Size:
        return self._content_region_size

    @property
    def cursor_lineno(self) -> int:
        return self._cursor_lineno

    @property
    def cursor_column(self) -> int:
        return self._cursor_column

    @property
    def terminal_size(self) -> SizeI:
        return self._terminal_size

    def get_selected_text(self, selection: Optional[TerminalSelection] = None) -> str:
        return str()

    def render(
        self,
        lines: Sequence[str],
        style: Optional[TerminalStyle] = None,
        selection: Optional[TerminalSelection] = None,
        *,
        lineno=1,
    ) -> None:
        with begin_child_context(
            self._label,
            self._size,
            self._child_flags,
            self._window_flags,
        ):
            if imgui.is_window_hovered():
                if self._mouse_wheel.update(imgui.get_io().mouse_wheel):
                    if 0 < self._mouse_wheel.value:
                        # Drag Up
                        if imgui.get_scroll_y() < imgui.get_scroll_max_y():
                            self._autoscroll = False
                    elif self._mouse_wheel.value < 0:
                        # Drag Down
                        if imgui.get_scroll_max_y() <= imgui.get_scroll_y():
                            self._autoscroll = True
                    else:
                        assert 0 == self._mouse_wheel.value

            self.render_editor_canvas(lines, style, selection, lineno=lineno)

            if self._autoscroll:
                imgui.set_scroll_here_y(1.0)

    def render_editor_canvas(
        self,
        lines: Sequence[str],
        style: Optional[TerminalStyle] = None,
        selection: Optional[TerminalSelection] = None,
        *,
        lineno=1,
    ) -> None:
        if style is None:
            style = TerminalStyle()
        assert isinstance(style, TerminalStyle)

        if selection is None:
            selection = TerminalSelection()
        assert isinstance(selection, TerminalSelection)

        mouse_pos = imgui.get_mouse_pos()
        cursor_pos = imgui.get_cursor_pos()
        cursor_screen_pos = imgui.get_cursor_screen_pos()
        content_region_size = imgui.get_content_region_avail()

        mx, my = mouse_pos.x, mouse_pos.y
        cx, cy = cursor_pos.x, cursor_pos.y
        csx, csy = cursor_screen_pos.x, cursor_screen_pos.y
        crw, crh = content_region_size.x, content_region_size.y

        if crw == 0 or crh == 0:
            raise ValueError("Invalid region size")

        assert isinstance(mx, float)
        assert isinstance(my, float)
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(csx, float)
        assert isinstance(csy, float)
        assert isinstance(crw, float)
        assert isinstance(crh, float)
        self._draw_list = get_window_draw_list()
        self._mouse_pos = mx, my
        self._cursor_pos = cx, cy
        self._cursor_screen_pos = csx, csy
        self._content_region_size = crw, crh

        io = imgui.get_io()

        left_down = bool(io.mouse_down[MOUSE_LEFT])
        right_down = bool(io.mouse_down[MOUSE_RIGHT])
        middle_down = bool(io.mouse_down[MOUSE_MIDDLE])

        self._left_button.update(left_down, self._mouse_pos)
        self._middle_button.update(middle_down, self._mouse_pos)
        self._right_button.update(right_down, self._mouse_pos)

        self._shift_down.update(io.key_shift)
        self._ctrl_down.update(io.key_ctrl)
        self._alt_down.update(io.key_alt)

        lineno_max_length = max(1, len(str(lineno + len(lines))))
        lineno_max_width_dummy_text = chr(DIGIT_ZERO) * lineno_max_length
        lineno_max_width = imgui.calc_text_size(lineno_max_width_dummy_text).x

        item_spacing_x = get_item_spacing_x()
        line_begin_x = lineno_max_width + item_spacing_x if self._show_lineno else 0.0
        line_height = get_line_height()
        full_line_height = line_height * len(lines)

        if self._show_lineno:
            # Draw a vertical line matching the width of the line number area.
            p1 = csx + lineno_max_width + get_item_spacing_x_half(), 0.0
            p2 = p1[0], max(csy + crh, full_line_height)
            self._draw_list.add_line(p1, p2, self.border_color, get_border_width())

        single_char_width = get_char_width()
        screen_width = floor(crw / single_char_width)
        screen_height = floor(crh / line_height)
        self._terminal_size = screen_width, screen_height

        mouse_x = mx - csx - line_begin_x
        mouse_y = my - csy
        self._cursor_column = floor(mouse_x / single_char_width) + 1
        self._cursor_lineno = lineno + floor(mouse_y / line_height)

        if self._left_button.changed_down:
            selection.set_begin(self._cursor_lineno, self._cursor_column)
        if self._left_button.is_down:
            selection.set_end(self._cursor_lineno, self._cursor_column)
        if self._left_button.changed_up:
            selection.set_end(self._cursor_lineno, self._cursor_column)
            if selection.begin == selection.end:
                selection.begin = None
                selection.end = None

        clipper = imgui.ListClipper()
        clipper.begin(len(lines))
        while clipper.step():
            for i in range(clipper.display_start, clipper.display_end):
                line_cursor_pos = imgui.get_cursor_pos()
                line_screen_pos = imgui.get_cursor_screen_pos()

                line_cx, line_cy = line_cursor_pos.x, line_cursor_pos.y
                line_sx, line_sy = line_screen_pos.x, line_screen_pos.y
                line_lineno = lineno + i

                if self._show_lineno:
                    lineno_pos = line_sx, line_sy
                    lineno_color = self.text_disabled_color
                    lineno_text = str(line_lineno).zfill(lineno_max_length)
                    self._draw_list.add_text(lineno_pos, lineno_color, lineno_text)

                line_pos = line_sx + line_begin_x, line_sy
                line_size = self.render_line(
                    lineno=line_lineno,
                    text=lines[i],
                    pos=line_pos,
                    style=style,
                    selection=selection,
                )

                # Advance the cursor position manually for the next line.
                next_pos_x = line_cx
                next_pos_y = line_cy + line_size[1]
                next_pos = next_pos_x, next_pos_y
                imgui.set_cursor_pos(next_pos)

    def render_line(
        self,
        lineno: int,
        text: str,
        pos: Point,
        style: TerminalStyle,
        selection: TerminalSelection,
    ) -> Size:
        block = self._builder.build_with_caching(
            lineno=lineno,
            text=text,
            style=style,
            palette=self._palette,
            selection=selection,
            same_line=True,
        )

        line_pivot_x, line_pivot_y = pos
        char_width = get_char_width()
        char_height = get_text_line_height()
        line_height = get_line_height()

        lines = [block.line]
        assert 1 <= len(lines)

        for line_block in lines:
            cx = line_pivot_x
            cy = line_pivot_y

            try:
                for text_block in line_block:
                    x1 = cx + char_width * (text_block.col_begin - 1)
                    x2 = cx + char_width * (text_block.col_end - 1)
                    y1 = cy
                    y2 = cy + char_height
                    p1 = x1, y1
                    p2 = x2, y2

                    if text_block.background is not None:
                        self._draw_list.add_rect_filled(p1, p2, text_block.background)

                    if text_block.foreground is not None:
                        text_color = text_block.foreground
                    else:
                        text_color = self.text_color

                    self._draw_list.add_text(p1, text_color, text_block.display_text)

                    if self._show_block_roi:
                        self._draw_list.add_rect(p1, p2, self._palette.debug)
                        if imgui.is_mouse_hovering_rect(p1, p2):
                            text_info = StringIO()
                            text_info.write(text_block.as_unformatted_text())
                            text_info.write(f"Selection: {selection}\n")
                            text_info.write(f"Block Selection: {block.selection}\n")
                            clip_selection = block.clip_selection(selection)
                            text_info.write(f"Clip Selection: {clip_selection}\n")
                            text_info.write(f"Block Update At: {block.update_at}\n")
                            tooltip_text_wrapped(text_info.getvalue())

                    elif self._show_error and text_block.error:
                        self._draw_list.add_rect(p1, p2, self._palette.error)
                        if imgui.is_mouse_hovering_rect(p1, p2):
                            tooltip_text_wrapped(text_block.error)

                if self._show_eol:
                    col_end = line_block.col_end if line_block else 1
                    eol_pos = cx + char_width * (col_end - 1), cy
                    eol_color = self.text_disabled_color
                    eol_char = self._eol_char
                    self._draw_list.add_text(eol_pos, eol_color, eol_char)
            finally:
                line_pivot_y += line_height

        size_x = char_width * block.cols
        size_y = line_height * len(lines)

        if self._show_line_roi:
            rect_x2 = pos[0] + size_x
            rect_y2 = pos[1] + size_y
            self._draw_list.add_rect(pos, (rect_x2, rect_y2), self._palette.debug)

        return size_x, size_y
