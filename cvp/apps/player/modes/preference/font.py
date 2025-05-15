# -*- coding: utf-8 -*-

from math import isqrt
from typing import Final, List, Tuple

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.clipboard import put_clipboard_text
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags import focused, hovered
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.mouse_button import MOUSE_LEFT
from cvp.imgui.fonts.font import Font
from cvp.imgui.fonts.globals import GlobalFontMapper
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.text_centered import text_centered
from cvp.types.colors import RGBA
from cvp.types.override import override


class FontPreference(BasePreference):
    __cvp_menu_name__ = "Font"

    _MENU_SPLIT_X: Final[int] = 150
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _PLANES_SPLIT_X: Final[int] = 150
    _PLANES_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

    @staticmethod
    def fonts() -> List[imgui.ImFont]:
        return [font for font in imgui.get_io().fonts.fonts]

    @property
    def config(self):
        return self.context.config.font

    @property
    def selected_block(self) -> Tuple[int, int]:
        return self.config.selected_block

    @selected_block.setter
    def selected_block(self, value: Tuple[int, int]) -> None:
        self.config.selected_block = value

    @property
    def selected_begin(self) -> int:
        return self.selected_block[0]

    @property
    def selected_end(self) -> int:
        return self.selected_block[1]

    @property
    def text_color(self) -> RGBA:
        return self.config.text_color

    @property
    def normal_stroke_color(self) -> RGBA:
        return self.config.normal_stroke_color

    @property
    def error_stroke_color(self) -> RGBA:
        return self.config.error_stroke_color

    @override
    def on_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for key, font in GlobalFontMapper().items():
                        selected = key == self.selected_submenu
                        if imgui.selectable(key, selected)[1]:
                            self.selected_submenu = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            selected_font = GlobalFontMapper().get(self.selected_submenu)
            if selected_font is None:
                text_centered("Please select a item")
            else:
                self.do_font_process(selected_font)

    def do_font_process(self, font: Font) -> None:
        input_text_disabled("Font family", font.family)
        input_text_disabled("Font pixel size", str(font.size))

        with begin_child_context(
            label="Planes",
            size=(self._PLANES_SPLIT_X, 0),
            child_flags=self._PLANES_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("##Planes", FIT_SIZE):
                try:
                    self.selectable_blocks(font)
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Codepoints"):
            self.do_codepoint_matrix(font)

    def selectable_blocks(self, font: Font) -> None:
        for block in font.blocks:
            if imgui.selectable(block.as_label(), block == self.selected_block)[1]:
                self.selected_block = block

    def do_codepoint_matrix(self, font: Font) -> None:
        if self.selected_block not in font.blocks:
            text_centered("Please select a item")
            return

        codepoint_begin = self.selected_begin
        normal_stroke_color = imgui.get_color_u32(self.normal_stroke_color)
        error_stroke_color = imgui.get_color_u32(self.error_stroke_color)
        text_color = imgui.get_color_u32(self.text_color)
        padding = self.config.padding
        rounding = self.config.rounding
        rect_flags = self.config.rect_flags
        thickness = self.config.thickness

        cp = imgui.get_cursor_screen_pos()
        cx = cp.x
        cy = cp.y
        draw_list = get_window_draw_list()
        cell_size = font.size
        block_step = font.block_step
        line_count = isqrt(block_step)

        for i in range(block_step):
            x = i % line_count
            y = i // line_count

            x1 = cx + x * (cell_size + padding)
            y1 = cy + y * (cell_size + padding)
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            r_min = x1, y1
            r_max = x2, y2

            codepoint = codepoint_begin + i
            cp_detail = font.get_codepoint_info(codepoint)
            stroke_color = normal_stroke_color if cp_detail else error_stroke_color

            draw_list.add_rect(
                r_min,
                r_max,
                stroke_color,
                rounding,
                rect_flags,
                thickness,
            )

            if cp_detail:
                with font:
                    draw_list.add_text(r_min, text_color, cp_detail.character)

            child_focused = imgui.is_window_focused(focused.ROOT_AND_CHILD_WINDOWS)
            child_hovered = imgui.is_window_hovered(hovered.ROOT_AND_CHILD_WINDOWS)
            if child_focused and imgui.is_mouse_hovering_rect(r_min, r_max):
                if child_hovered and imgui.is_mouse_clicked(MOUSE_LEFT):
                    put_clipboard_text(cp_detail.as_printable_unicode())
                    self.context.msgs.append_toast("Copied to clipboard")

                if imgui.begin_tooltip():
                    try:
                        message = cp_detail.as_unformatted_text()
                        imgui.text_unformatted(message.strip())
                    finally:
                        imgui.end_tooltip()
