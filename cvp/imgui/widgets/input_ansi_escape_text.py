# -*- coding: utf-8 -*-

from io import StringIO
from math import floor
from typing import NamedTuple, Optional, Sequence, Tuple, Union

from imgui_bundle import imgui

from cvp.encoding.ascii import HT, LF, PILCROW_SIGN, SPACE
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.draw_list.create import create_draw_list_with_shared_data
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags import color_var
from cvp.imgui.flags.button import ALL_BUTTON_FLAGS
from cvp.imgui.flags.child import BORDERS, ChildFlags
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.flags.mouse_button import MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT
from cvp.imgui.flags.window import WindowFlags
from cvp.imgui.tooltip import tooltip_text_wrapped
from cvp.terminal.ansi import sgr
from cvp.terminal.ansi.csi import CsiCommand
from cvp.terminal.ansi.palette import TerminalPalette
from cvp.terminal.ansi.parser import (
    AnsiCsiEscape,
    AnsiError,
    AnsiEscape,
    AnsiFeEscape,
    AnsiLineFeed,
    parse_ansi_escape_text,
)
from cvp.terminal.ansi.style import TerminalStyle
from cvp.types.shapes import Point, Size
from cvp.values.delta import DeltaValue
from cvp.values.drag_button import DragButton


class InputAnsiEscapeText:
    """
    https://en.wikipedia.org/wiki/ANSI_escape_code
    """

    class Coord(NamedTuple):
        lineno: int
        column: int

    class GlyphInfo(NamedTuple):
        char: str
        display_char: str
        display_size: Tuple[float, float]
        column_size: int

    def __init__(
        self,
        label: str,
        size: Optional[imgui.ImVec2Like] = None,
        child_flags: Union[ChildFlags, int] = BORDERS,
        window_flags: Union[WindowFlags, int] = 0,
        *,
        lineno_begin=1,
        readonly=False,
        autoscroll=False,
        tab_size=4,
        show_lineno=False,
        show_whitespace=False,
        show_eol=False,
        palette: Optional[TerminalPalette] = None,
        style: Optional[TerminalStyle] = None,
        selected_begin: Optional[Coord] = None,
        selected_end: Optional[Coord] = None,
    ):
        self._label = label
        self._size = size
        self._child_flags = child_flags
        self._window_flags = window_flags

        self.lineno_begin = lineno_begin
        self.readonly = readonly
        self.autoscroll = autoscroll
        self.tab_size = tab_size
        self.show_lineno = show_lineno
        self.show_whitespace = show_whitespace
        self.show_eol = show_eol
        self.palette = palette if palette else TerminalPalette()
        self.style = style if style else TerminalStyle()

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

        self._control_identifier = type(self).__name__
        self._control_flags = int(ALL_BUTTON_FLAGS)

        self._terminal_coord_lineno = 0
        self._terminal_coord_column = 0
        self._terminal_size = 0, 0

        self._selected_begin = selected_begin
        self._selected_end = selected_end
        self._selected_buffer = StringIO()
        self._selected_text = str()

    @property
    def mouse_pos(self):
        return self._mouse_pos

    @property
    def cursor_pos(self):
        return self._cursor_pos

    @property
    def cursor_screen_pos(self):
        return self._cursor_screen_pos

    @property
    def content_region_size(self):
        return self._content_region_size

    @property
    def selected_begin(self) -> Optional[Coord]:
        return self._selected_begin

    @property
    def selected_end(self) -> Optional[Coord]:
        return self._selected_end

    @property
    def terminal_coord(self) -> Coord:
        return self.Coord(self._terminal_coord_lineno, self._terminal_coord_column)

    @property
    def terminal_size(self) -> Tuple[int, int]:
        return self._terminal_size

    @property
    def border_color(self) -> int:
        color = imgui.get_style_color_vec4(color_var.BORDER)
        return imgui.get_color_u32(color)

    @property
    def text_color(self) -> int:
        color = imgui.get_style_color_vec4(color_var.TEXT)
        return imgui.get_color_u32(color)

    @property
    def text_disabled_color(self) -> int:
        color = imgui.get_style_color_vec4(color_var.TEXT_DISABLED)
        return imgui.get_color_u32(color)

    @property
    def text_link_color(self) -> int:
        color = imgui.get_style_color_vec4(color_var.TEXT_LINK)
        return imgui.get_color_u32(color)

    @property
    def text_selected_bg_color(self) -> int:
        color = imgui.get_style_color_vec4(color_var.TEXT_SELECTED_BG)
        return imgui.get_color_u32(color)

    @property
    def error_color(self) -> int:
        return self.palette.error

    @property
    def warning_color(self) -> int:
        return self.palette.warning

    @property
    def success_color(self) -> int:
        return self.palette.success

    @property
    def debug_color(self) -> int:
        return self.palette.debug

    @property
    def border_width(self) -> float:
        return imgui.get_style().child_border_size

    @property
    def item_spacing(self):
        return imgui.get_style().item_spacing

    @property
    def item_spacing_x_half(self) -> float:
        return self.item_spacing.x / 2.0

    @property
    def item_spacing_y_half(self) -> float:
        return self.item_spacing.y / 2.0

    @property
    def text_line_height(self) -> float:
        return imgui.get_text_line_height()

    @property
    def line_height(self) -> float:
        return self.text_line_height + self.item_spacing_y_half

    @property
    def char_width(self) -> float:
        return imgui.calc_text_size("0").x

    @property
    def background_color(self) -> Optional[int]:
        if self.style.background is not None:
            if isinstance(self.style.background, int):
                return self.style.background
            if isinstance(self.style.background, tuple):
                assert 3 == len(self.style.background)
                r, g, b = self.style.background
                return imgui.get_color_u32((r, g, b, 1.0))
        return None

    @property
    def foreground_color(self) -> int:
        if self.style.foreground is not None:
            if isinstance(self.style.foreground, int):
                return self.style.foreground
            if isinstance(self.style.foreground, tuple):
                assert 3 == len(self.style.foreground)
                r, g, b = self.style.foreground
                return imgui.get_color_u32((r, g, b, 1.0))
        return self.text_color

    @property
    def normalized_selected(self) -> Tuple[Coord, Coord]:
        if self._selected_begin is None or self._selected_end is None:
            raise ValueError("Selection is not set")

        if self._selected_begin <= self._selected_end:
            return self._selected_begin, self._selected_end
        else:
            return self._selected_end, self._selected_begin

    @property
    def has_selected_coords(self) -> bool:
        return self._selected_begin is not None and self._selected_end is not None

    def is_selected_with_coord(self, coord: Coord) -> bool:
        try:
            begin, end = self.normalized_selected
            return begin <= coord < end
        except ValueError:
            return False

    def is_selected_with_lineno(self, lineno: int) -> bool:
        try:
            begin, end = self.normalized_selected
            return begin.lineno <= lineno < end.lineno
        except ValueError:
            return False

    def get_glyph(self, c: str) -> GlyphInfo:
        if c == chr(HT):
            display_char = chr(SPACE) * self.tab_size
        else:
            display_char = c

        text_size = imgui.calc_text_size(display_char)
        display_size = text_size.x, text_size.y
        column_size = floor(text_size.x / self.char_width)
        return self.GlyphInfo(c, display_char, display_size, column_size)

    def get_selected_column(
        self,
        line: str,
        begin_column=0,
        end_column: Optional[int] = None,
        *,
        raw=False,
    ) -> str:
        if end_column is None:
            end_column = len(line)
        assert isinstance(end_column, int)

        column = 0
        buffer = StringIO()
        try:
            for token in parse_ansi_escape_text(line):
                line_text = token.token
                assert line_text.find(chr(LF)) == -1

                if isinstance(token, AnsiEscape):
                    assert isinstance(token, (AnsiCsiEscape, AnsiFeEscape, AnsiEscape))
                    assert len(line_text) == len(line_text.encode())
                    if raw and begin_column <= column < end_column:
                        buffer.write(token.token)
                    continue

                for c in line_text:
                    glyph = self.get_glyph(c)
                    if begin_column <= column < end_column:
                        if raw:
                            buffer.write(c)
                        else:
                            buffer.write(glyph.display_char)
                    column += glyph.column_size
        finally:
            return buffer.getvalue()

    def get_selected_text(self, lines: Sequence[str]) -> str:
        try:
            begin, end = self.normalized_selected
            if begin == end:
                return str()

            assert begin < end
            begin_line_index = begin.lineno - self.lineno_begin
            end_line_index = end.lineno - self.lineno_begin
            begin_column = begin.column
            end_column = end.column

            if begin_line_index == end_line_index:
                assert begin_column < end_column
                return self.get_selected_column(
                    lines[begin_line_index],
                    begin_column,
                    end_column,
                )

            assert begin_line_index < end_line_index
            begin_line = lines[begin_line_index]
            end_line = lines[end_line_index]

            buffer = StringIO()
            buffer.write(self.get_selected_column(begin_line, begin_column))
            buffer.write(chr(LF))

            for lineno in range(begin_line_index + 1, end_line_index):
                buffer.write(self.get_selected_column(lines[lineno]))
                buffer.write(chr(LF))

            buffer.write(self.get_selected_column(end_line, 0, end_column))

            return buffer.getvalue()
        except ValueError:
            return str()

    def select_all(self, lines: Sequence[str]) -> None:
        self._selected_begin = self.Coord(self.lineno_begin, 0)
        self._selected_end = self.Coord(self.lineno_begin + len(lines), 0)

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

        assert imgui.get_style().window_padding.x == cx
        assert imgui.get_style().window_padding.y == cy
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

        lineno_width = max(1, len(str(len(lines))))
        lineno_width_dummy_text = "0" * lineno_width
        lineno_text_size = imgui.calc_text_size(lineno_width_dummy_text)

        item_spacing_x = self.item_spacing.x
        line_begin_x = lineno_text_size.x + item_spacing_x if self.show_lineno else 0.0
        line_height = self.line_height
        full_line_height = line_height * len(lines)

        if self.show_lineno:
            # Draw a vertical line matching the width of the line number area.
            p1 = csx + lineno_text_size.x + self.item_spacing_x_half, 0.0
            p2 = p1[0], max(csy + crh, full_line_height)
            self._draw_list.add_line(p1, p2, self.border_color, self.border_width)

        screen_width = floor(crw / self.char_width)
        screen_height = floor(crh / line_height)
        self._terminal_size = screen_width, screen_height

        mouse_x = mx - csx - line_begin_x
        mouse_y = my - csy
        self._terminal_coord_column = floor(mouse_x / self.char_width)
        self._terminal_coord_lineno = self.lineno_begin + floor(mouse_y / line_height)

        if self._left_button.changed_down:
            self._selected_begin = self.terminal_coord
        if self._left_button.is_down:
            self._selected_end = self.terminal_coord
        if self._left_button.changed_up:
            self._selected_end = self.terminal_coord
            if self._selected_begin == self._selected_end:
                self._selected_begin = None
                self._selected_end = None

        clipper = imgui.ListClipper()
        clipper.begin(len(lines))
        while clipper.step():
            for i in range(clipper.display_start, clipper.display_end):
                line_cursor_pos = imgui.get_cursor_pos()
                line_screen_pos = imgui.get_cursor_screen_pos()

                line_cx, line_cy = line_cursor_pos.x, line_cursor_pos.y
                line_sx, line_sy = line_screen_pos.x, line_screen_pos.y
                lineno = self.lineno_begin + i

                if self.show_lineno:
                    self._draw_list.add_text(
                        (line_sx, line_sy),
                        self.text_disabled_color,
                        str(lineno).zfill(lineno_width),
                    )

                line_text_size = self.do_line_process(
                    lines[i],
                    (line_sx + line_begin_x, line_sy),
                    lineno,
                    debug=debug,
                )

                # Advance the cursor position manually for the next line.
                next_pos_x = line_cx
                next_pos_y = line_cy + line_text_size[1]
                imgui.set_cursor_pos((next_pos_x, next_pos_y))

    def do_line_process(
        self,
        text: str,
        pos: Point,
        lineno: int,
        *,
        debug=False,
    ) -> Size:
        line_cx, line_cy = pos
        max_width = 0.0
        column = 0

        for line in text.split(chr(LF)):
            cx = line_cx
            cy = line_cy
            max_height_by_line = self.text_line_height

            try:
                for token in parse_ansi_escape_text(line):
                    assert not isinstance(token, AnsiLineFeed)

                    if isinstance(token, AnsiCsiEscape):
                        self.do_csi_process(token.command)
                        continue
                    elif isinstance(token, AnsiFeEscape):
                        self.do_fe_process(token.control_code)
                        continue
                    elif isinstance(token, AnsiEscape):
                        self.do_fe_process(token.control_code)
                        continue

                    line_text = token.token
                    assert line_text.find(chr(LF)) == -1
                    line_text_size = imgui.calc_text_size(line_text)
                    max_height_by_line = max(max_height_by_line, line_text_size.y)

                    sel_color = self.text_selected_bg_color
                    bg_color = self.background_color
                    fg_color = self.foreground_color

                    line_text_rect_p1 = cx, cy
                    line_text_rect_p2 = cx + line_text_size.x, cy + line_text_size.y

                    for i, c in enumerate(line_text):
                        glyph = self.get_glyph(c)
                        display_char = glyph.display_char
                        display_width, display_height = glyph.display_size
                        column_offset = glyph.column_size

                        try:
                            p1 = cx, cy
                            p2 = cx + display_width, cy + display_height

                            if self.is_selected_with_coord(self.Coord(lineno, column)):
                                self._draw_list.add_rect_filled(p1, p2, sel_color)
                            elif bg_color is not None:
                                self._draw_list.add_rect_filled(p1, p2, bg_color)

                            self._draw_list.add_text(p1, fg_color, display_char)
                        finally:
                            cx += display_width
                            column += column_offset

                    if isinstance(token, AnsiError):
                        self._draw_list.add_rect(
                            line_text_rect_p1,
                            line_text_rect_p2,
                            self.error_color,
                        )
                        if imgui.is_mouse_hovering_rect(
                            line_text_rect_p1,
                            line_text_rect_p2,
                        ):
                            tooltip_text_wrapped(token.error_message)

                if self.show_eol:
                    self._draw_list.add_text(
                        (cx, cy),
                        self.text_disabled_color,
                        chr(PILCROW_SIGN),
                    )
            finally:
                max_width = max(max_width, cx - line_cx)
                line_cy += max_height_by_line + self.item_spacing_y_half

        height = line_cy - pos[1]
        size_x = max_width
        size_y = max(self.line_height, height)

        if debug:
            rect_x2 = pos[0] + size_x
            rect_y2 = pos[1] + size_y
            self._draw_list.add_rect(pos, (rect_x2, rect_y2), self.debug_color)

        return size_x, size_y

    def do_csi_process(self, command: CsiCommand) -> None:
        if not command.is_sgr:
            # Other Control Sequence Introducers are not supported.
            pass

        params = command.as_integer_parameters()
        if not params:
            # `CSI m` is treated as `CSI 0 m` (reset / normal).
            params.append(0)

        self.do_sgr_process(*params)

    def do_fe_process(self, control_code: str) -> None:
        pass

    def do_sgr_process(self, *args: int) -> None:
        """
        Select Graphic Rendition
        """
        assert 1 <= len(args)
        match args[0]:
            # --------------------------------------------------------------------------
            case sgr.RESET:
                self.style.reset()
            case sgr.FG_COLOR_BLACK:
                self.style.foreground = self.palette.black
            case sgr.FG_COLOR_RED:
                self.style.foreground = self.palette.red
            case sgr.FG_COLOR_GREEN:
                self.style.foreground = self.palette.green
            case sgr.FG_COLOR_YELLOW:
                self.style.foreground = self.palette.yellow
            case sgr.FG_COLOR_BLUE:
                self.style.foreground = self.palette.blue
            case sgr.FG_COLOR_MAGENTA:
                self.style.foreground = self.palette.magenta
            case sgr.FG_COLOR_CYAN:
                self.style.foreground = self.palette.cyan
            case sgr.FG_COLOR_WHITE:
                self.style.foreground = self.palette.white
            case sgr.FG_COLOR_EXTENDED:
                self.style.foreground = sgr.get_extended_color_with_parameters(*args)
            case sgr.FG_COLOR_DEFAULT:
                self.style.foreground = None
            # --------------------------------------------------------------------------
            case sgr.BG_COLOR_BLACK:
                self.style.background = self.palette.black
            case sgr.BG_COLOR_RED:
                self.style.background = self.palette.red
            case sgr.BG_COLOR_GREEN:
                self.style.background = self.palette.green
            case sgr.BG_COLOR_YELLOW:
                self.style.background = self.palette.yellow
            case sgr.BG_COLOR_BLUE:
                self.style.background = self.palette.blue
            case sgr.BG_COLOR_MAGENTA:
                self.style.background = self.palette.magenta
            case sgr.BG_COLOR_CYAN:
                self.style.background = self.palette.cyan
            case sgr.BG_COLOR_WHITE:
                self.style.background = self.palette.white
            case sgr.BG_COLOR_EXTENDED:
                self.style.background = sgr.get_extended_color_with_parameters(*args)
            case sgr.BG_COLOR_DEFAULT:
                self.style.background = None
            # --------------------------------------------------------------------------
            case sgr.BRIGHT_FG_COLOR_BLACK:
                self.style.foreground = self.palette.bright_black
            case sgr.BRIGHT_FG_COLOR_RED:
                self.style.foreground = self.palette.bright_red
            case sgr.BRIGHT_FG_COLOR_GREEN:
                self.style.foreground = self.palette.bright_green
            case sgr.BRIGHT_FG_COLOR_YELLOW:
                self.style.foreground = self.palette.bright_yellow
            case sgr.BRIGHT_FG_COLOR_BLUE:
                self.style.foreground = self.palette.bright_blue
            case sgr.BRIGHT_FG_COLOR_MAGENTA:
                self.style.foreground = self.palette.bright_magenta
            case sgr.BRIGHT_FG_COLOR_CYAN:
                self.style.foreground = self.palette.bright_cyan
            case sgr.BRIGHT_FG_COLOR_WHITE:
                self.style.foreground = self.palette.bright_white
            # --------------------------------------------------------------------------
            case sgr.BRIGHT_BG_COLOR_BLACK:
                self.style.background = self.palette.bright_black
            case sgr.BRIGHT_BG_COLOR_RED:
                self.style.background = self.palette.bright_red
            case sgr.BRIGHT_BG_COLOR_GREEN:
                self.style.background = self.palette.bright_green
            case sgr.BRIGHT_BG_COLOR_YELLOW:
                self.style.background = self.palette.bright_yellow
            case sgr.BRIGHT_BG_COLOR_BLUE:
                self.style.background = self.palette.bright_blue
            case sgr.BRIGHT_BG_COLOR_MAGENTA:
                self.style.background = self.palette.bright_magenta
            case sgr.BRIGHT_BG_COLOR_CYAN:
                self.style.background = self.palette.bright_cyan
            case sgr.BRIGHT_BG_COLOR_WHITE:
                self.style.background = self.palette.bright_white
            # --------------------------------------------------------------------------
