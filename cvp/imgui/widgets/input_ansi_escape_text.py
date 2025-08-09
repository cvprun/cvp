# -*- coding: utf-8 -*-

from math import floor
from typing import Optional, Sequence, Tuple, Union

from imgui_bundle import imgui

from cvp.encoding.ascii import LF
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.draw_list.create import create_draw_list_with_shared_data
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags import color_var
from cvp.imgui.flags.button import ALL_BUTTON_FLAGS
from cvp.imgui.flags.child import BORDERS, ChildFlags
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.flags.window import WindowFlags
from cvp.terminal.ansi import sgr
from cvp.terminal.ansi.csi import CsiCommand
from cvp.terminal.ansi.palette import TerminalPalette
from cvp.terminal.ansi.parser import (
    AnsiCsiEscape,
    AnsiError,
    AnsiToken,
    parse_ansi_escape_text,
)
from cvp.terminal.ansi.style import TerminalStyle
from cvp.types.colors import RED_RGB
from cvp.types.shapes import Point, Size
from cvp.values.delta import DeltaValue


class InputAnsiEscapeText:
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

        self._palette = TerminalPalette()
        self._style = TerminalStyle()

    @property
    def terminal_cursor(self) -> Tuple[int, int]:
        return self._terminal_cursor

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
    def error_color(self) -> int:
        r, g, b = RED_RGB
        return imgui.get_color_u32((r, g, b, 0.8))

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

        lineno_width = max(1, len(str(len(lines))))
        lineno_width_dummy_text = "0" * lineno_width
        lineno_text_size = imgui.calc_text_size(lineno_width_dummy_text)

        item_spacing_x = self.item_spacing.x
        line_begin_x = lineno_text_size.x + item_spacing_x if self.show_lineno else 0.0
        line_height = self.line_height
        full_line_height = line_height * len(lines)

        screen_width = floor(self._canvas_size[0] / imgui.calc_text_size("0").x)
        screen_height = floor(self._canvas_size[1] / line_height)
        self._terminal_size = screen_width, screen_height

        if self.show_lineno:
            # Draw a vertical line matching the width of the line number area.
            p1 = sx + lineno_text_size.x + self.item_spacing_x_half, 0.0
            p2 = p1[0], max(sy + rh, full_line_height)
            self._draw_list.add_line(p1, p2, self.border_color, self.border_width)

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
                        self.text_disabled_color,
                        lineno_text,
                    )

                line_text = lines[i]
                line_text_pos = line_sx + line_begin_x, line_sy

                line_text_size = self.do_line_process(
                    line_text,
                    line_text_pos,
                    debug=debug,
                )

                # Advance the cursor position manually for the next line.
                next_pos_x = line_cx
                next_pos_y = line_cy + line_text_size[1]
                imgui.set_cursor_pos((next_pos_x, next_pos_y))

    def do_line_process(self, text: str, pos: Point, *, debug=False) -> Size:
        line_cx, line_cy = pos
        max_width = 0.0

        for line in text.split(chr(LF)):
            cx = line_cx
            cy = line_cy
            max_height_by_line = self.text_line_height
            try:
                for token in parse_ansi_escape_text(line):
                    assert isinstance(token, AnsiToken)
                    if isinstance(token, AnsiCsiEscape):
                        self.do_csi_process(token.command)
                        continue

                    if isinstance(token, AnsiError):
                        tw, th = self.do_error_text_process(token.token, (cx, cy))
                        if debug:
                            pass
                    else:
                        tw, th = self.do_text_process(token.token, (cx, cy))

                    cx += tw
                    max_height_by_line = max(max_height_by_line, th)
            finally:
                max_width = max(max_width, cx - line_cx)
                line_cy += max_height_by_line + self.item_spacing_y_half

        size_x = max_width
        size_y = max(self.text_line_height, pos[1] - line_cy - self.item_spacing_y_half)

        if debug:
            rect_x2 = pos[0] + size_x
            rect_y2 = pos[1] + size_y
            self._draw_list.add_rect(pos, (rect_x2, rect_y2), self.error_color)

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

    def do_sgr_process(self, *args: int) -> None:
        """
        Select Graphic Rendition
        """
        assert 1 <= len(args)
        match args[0]:
            # --------------------------------------------------------------------------
            case sgr.RESET:
                self._style.reset()
            case sgr.FG_COLOR_BLACK:
                self._style.foreground = self._palette.black
            case sgr.FG_COLOR_RED:
                self._style.foreground = self._palette.red
            case sgr.FG_COLOR_GREEN:
                self._style.foreground = self._palette.green
            case sgr.FG_COLOR_YELLOW:
                self._style.foreground = self._palette.yellow
            case sgr.FG_COLOR_BLUE:
                self._style.foreground = self._palette.blue
            case sgr.FG_COLOR_MAGENTA:
                self._style.foreground = self._palette.magenta
            case sgr.FG_COLOR_CYAN:
                self._style.foreground = self._palette.cyan
            case sgr.FG_COLOR_WHITE:
                self._style.foreground = self._palette.white
            case sgr.FG_COLOR_EXTENDED:
                self._style.foreground = sgr.get_extended_color_with_parameters(*args)
            case sgr.FG_COLOR_DEFAULT:
                self._style.foreground = None
            # --------------------------------------------------------------------------
            case sgr.BG_COLOR_BLACK:
                self._style.background = self._palette.black
            case sgr.BG_COLOR_RED:
                self._style.background = self._palette.red
            case sgr.BG_COLOR_GREEN:
                self._style.background = self._palette.green
            case sgr.BG_COLOR_YELLOW:
                self._style.background = self._palette.yellow
            case sgr.BG_COLOR_BLUE:
                self._style.background = self._palette.blue
            case sgr.BG_COLOR_MAGENTA:
                self._style.background = self._palette.magenta
            case sgr.BG_COLOR_CYAN:
                self._style.background = self._palette.cyan
            case sgr.BG_COLOR_WHITE:
                self._style.background = self._palette.white
            case sgr.BG_COLOR_EXTENDED:
                self._style.background = sgr.get_extended_color_with_parameters(*args)
            case sgr.BG_COLOR_DEFAULT:
                self._style.background = None
            # --------------------------------------------------------------------------
            case sgr.BRIGHT_FG_COLOR_BLACK:
                self._style.foreground = self._palette.bright_black
            case sgr.BRIGHT_FG_COLOR_RED:
                self._style.foreground = self._palette.bright_red
            case sgr.BRIGHT_FG_COLOR_GREEN:
                self._style.foreground = self._palette.bright_green
            case sgr.BRIGHT_FG_COLOR_YELLOW:
                self._style.foreground = self._palette.bright_yellow
            case sgr.BRIGHT_FG_COLOR_BLUE:
                self._style.foreground = self._palette.bright_blue
            case sgr.BRIGHT_FG_COLOR_MAGENTA:
                self._style.foreground = self._palette.bright_magenta
            case sgr.BRIGHT_FG_COLOR_CYAN:
                self._style.foreground = self._palette.bright_cyan
            case sgr.BRIGHT_FG_COLOR_WHITE:
                self._style.foreground = self._palette.bright_white
            # --------------------------------------------------------------------------
            case sgr.BRIGHT_BG_COLOR_BLACK:
                self._style.background = self._palette.bright_black
            case sgr.BRIGHT_BG_COLOR_RED:
                self._style.background = self._palette.bright_red
            case sgr.BRIGHT_BG_COLOR_GREEN:
                self._style.background = self._palette.bright_green
            case sgr.BRIGHT_BG_COLOR_YELLOW:
                self._style.background = self._palette.bright_yellow
            case sgr.BRIGHT_BG_COLOR_BLUE:
                self._style.background = self._palette.bright_blue
            case sgr.BRIGHT_BG_COLOR_MAGENTA:
                self._style.background = self._palette.bright_magenta
            case sgr.BRIGHT_BG_COLOR_CYAN:
                self._style.background = self._palette.bright_cyan
            case sgr.BRIGHT_BG_COLOR_WHITE:
                self._style.background = self._palette.bright_white
            # --------------------------------------------------------------------------

    def do_error_text_process(self, text: str, pos: Point) -> Size:
        if not text:
            return 0.0, 0.0

        cx, cy = pos
        text_size = imgui.calc_text_size(text)
        pos2 = cx + text_size.x, cy + text_size.y

        self._draw_list.add_text(pos, self.error_color, text)
        self._draw_list.add_rect(pos, pos2, self.error_color)

        return text_size.x, text_size.y

    @property
    def background_color(self) -> Optional[int]:
        if self._style.background is not None:
            if isinstance(self._style.background, int):
                return self._style.background
            if isinstance(self._style.background, tuple):
                assert 3 == len(self._style.background)
                r, g, b = self._style.background
                return imgui.get_color_u32((r, g, b, 1.0))
        return None

    @property
    def foreground_color(self) -> int:
        if self._style.foreground is not None:
            if isinstance(self._style.foreground, int):
                return self._style.foreground
            if isinstance(self._style.foreground, tuple):
                assert 3 == len(self._style.foreground)
                r, g, b = self._style.foreground
                return imgui.get_color_u32((r, g, b, 1.0))
        return self.text_color

    def do_text_process(self, text: str, pos: Point) -> Size:
        if not text:
            return 0.0, 0.0

        cx, cy = pos
        text_size = imgui.calc_text_size(text)
        pos2 = cx + text_size.x, cy + text_size.y

        background_color = self.background_color
        if background_color is not None:
            self._draw_list.add_rect_filled(pos, pos2, background_color)

        self._draw_list.add_text(pos, self.foreground_color, text)

        return text_size.x, text_size.y
