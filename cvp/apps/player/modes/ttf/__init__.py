# -*- coding: utf-8 -*-

from math import isqrt
from typing import Any, Final

from fontTools.ttLib.ttFont import GlyphOrder
from imgui_bundle import imgui
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FORMAT_FONT
from cvp.context.context import Context
from cvp.fonts.codepoint_info import CodepointInfo
from cvp.fonts.ranges import BlockRange
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.draw_list.atlas.font import FontAtlas
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags import focused, hovered
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.mouse_button import MOUSE_LEFT
from cvp.imgui.input_text import input_text
from cvp.imgui.menu_container import MenuList
from cvp.imgui.menu_item import menu_item
from cvp.imgui.menu_recent_items import menu_recent_items
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.selectable import selectable
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.table_any import table_any
from cvp.logging.logging import logger
from cvp.types.colors import RGBA
from cvp.types.override import override


class TTFMode(BaseMode):
    __cvp_mode_name__ = "TTF Font"
    __cvp_mode_icon__ = FORMAT_FONT

    _EMPTY_CODEPOINT_INFO = CodepointInfo(0)

    _PLANES_SPLIT_X: Final[int] = 150
    _PLANES_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _CANVAS_SPLIT_X: Final[int] = -400
    _CANVAS_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS
    _INFOS_CHILD_FLAGS: Final[int] = BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
        self._open_font_popup = OpenFilePopup(
            title="Load font",
            target=self.on_load_font,
        )

        self._menus = MenuList(("File", self.on_file_menu))
        self._popups = PopupList(self._open_font_popup)

        self._atlas = FontAtlas()

        self._selected_block_index = 0
        self._selected_codepoint = 0
        self._selected_table_name = str()

    @property
    def config(self):
        return self.context.config.font

    @property
    def text_color(self) -> RGBA:
        return self.config.text_color

    @property
    def selected_stroke_color(self) -> RGBA:
        return self.config.selected_stroke_color

    @property
    def normal_stroke_color(self) -> RGBA:
        return self.config.normal_stroke_color

    @property
    def error_stroke_color(self) -> RGBA:
        return self.config.error_stroke_color

    def open_font_file(self, file: str) -> None:
        if self._atlas.opened:
            self._atlas.close()
            logger.info("Font file closed")

        try:
            self._atlas.open(file, size=self.config.preview_size)
            self.add_recent_item(file)
            logger.info(f"Font file opened: '{file}'")
        except BaseException as e:
            logger.error(f"Failed to open font file '{file}': {e}")
            raise

    def close(self) -> None:
        if not self._atlas.opened:
            raise ValueError("Font file not opened")

        self._atlas.close()
        logger.info("Font file closed")

    def get_current_codepoint_info(self) -> CodepointInfo:
        if not (0 <= self._selected_block_index < len(self._atlas.blocks)):
            return self._EMPTY_CODEPOINT_INFO

        block = self._atlas.blocks[self._selected_block_index]
        if not (block.begin <= self._selected_codepoint < block.end):
            return self._EMPTY_CODEPOINT_INFO

        codepoint = self._atlas.codepoints.get(self._selected_codepoint)
        if codepoint is None:
            return self._EMPTY_CODEPOINT_INFO

        return codepoint

    @override
    def on_main_menu(self) -> None:
        self._menus.do_process()

    @override
    def on_status_menu(self) -> None:
        pass

    @override
    def on_event(self, event: Event) -> bool:
        if event.type == DROPFILE:
            self.open_font_file(event.file)
            return True

        return False

    def on_load_font(self, file: str) -> None:
        self.open_font_file(file)

    def on_file_menu(self) -> None:
        if menu_item("Open font"):
            self._open_font_popup.show()

        if recent_item := menu_recent_items(
            label="Recent fonts",
            config=self.context.config.navigation,
            cls=type(self),
            append_clear_menu=True,
            clear_menu_label="Clear recent fonts",
        ):
            self.open_font_file(recent_item.value)

        imgui.separator()
        if menu_item("Close font", enabled=self._atlas.opened):
            self.close()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                if imgui.begin_tab_bar("Tabs"):
                    try:
                        if imgui.begin_tab_item("File")[0]:
                            try:
                                self.on_file_process()
                            finally:
                                imgui.end_tab_item()

                        if imgui.begin_tab_item("Planes")[0]:
                            try:
                                self.on_planes_process()
                            finally:
                                imgui.end_tab_item()

                        if self._atlas.ttf is not None:
                            for tag in self._atlas.ttf.ttfont.keys():
                                table = self._atlas.ttf.ttfont[tag]
                                if isinstance(table, GlyphOrder):
                                    continue

                                if imgui.begin_tab_item(tag)[0]:
                                    try:
                                        imgui.text(f"Table: {tag}")
                                        imgui.separator()
                                        self.on_table_process(tag, table)
                                    finally:
                                        imgui.end_tab_item()
                    finally:
                        imgui.end_tab_bar()

        self._popups.do_process()

    @staticmethod
    def on_table_process(tag: str, table: Any) -> None:
        table_any(f"Table##{tag}", table)

    def on_file_process(self) -> None:
        pass

    def on_planes_process(self) -> None:
        with begin_child_context(
            label="Planes",
            size=(self._PLANES_SPLIT_X, 0),
            child_flags=self._PLANES_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("##Planes", FIT_SIZE):
                try:
                    if self._atlas.blocks:
                        for i, block in enumerate(self._atlas.blocks):
                            label = block.as_label()
                            selected = i == self._selected_block_index
                            if selectable(label, selected).selected:
                                self._selected_block_index = i
                    else:
                        text_centered("Please open the font")
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context(
            label="Canvas",
            size=(self._CANVAS_SPLIT_X, 0),
            child_flags=self._CANVAS_CHILD_FLAGS,
        ):
            if self._atlas.opened:
                if 0 <= self._selected_block_index < len(self._atlas.blocks):
                    block = self._atlas.blocks[self._selected_block_index]
                    self.do_codepoint_matrix(block)
                else:
                    text_centered("Please select a block range")
            else:
                text_centered("Please open the font")

        imgui.same_line()

        with begin_child_context("Infos", child_flags=self._INFOS_CHILD_FLAGS):
            if self._atlas.opened:
                codepoint = self.get_current_codepoint_info()
                self.do_codepoint_process(codepoint)
            else:
                text_centered("Please open the font")

    def do_codepoint_matrix(self, block: BlockRange) -> None:
        codepoint_begin = block.begin

        selected_stroke_color = imgui.get_color_u32(self.selected_stroke_color)
        normal_stroke_color = imgui.get_color_u32(self.normal_stroke_color)
        error_stroke_color = imgui.get_color_u32(self.error_stroke_color)
        text_color = imgui.get_color_u32(self.text_color)
        padding = self.config.padding
        rounding = self.config.rounding
        rect_flags = self.config.rect_flags
        thickness = self.config.thickness
        block_step = self.config.block_size
        cell_size = self.config.preview_size

        cp = imgui.get_cursor_screen_pos()
        cx = cp.x
        cy = cp.y
        draw_list = get_window_draw_list()
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
            info = self._atlas.codepoints.get(codepoint)
            stroke_color = normal_stroke_color if info else error_stroke_color

            if codepoint == self._selected_codepoint:
                border_color = selected_stroke_color
            else:
                border_color = stroke_color

            draw_list.add_rect(
                r_min,
                r_max,
                border_color,
                rounding,
                rect_flags,
                thickness,
            )

            if info:
                draw_list.add_text(r_min, text_color, info.character)

            child_focused = imgui.is_window_focused(focused.ROOT_AND_CHILD_WINDOWS)
            child_hovered = imgui.is_window_hovered(hovered.ROOT_AND_CHILD_WINDOWS)
            if child_focused and imgui.is_mouse_hovering_rect(r_min, r_max):
                if child_hovered and imgui.is_mouse_clicked(MOUSE_LEFT):
                    self._selected_codepoint = codepoint

                if info and imgui.begin_tooltip():
                    try:
                        message = info.as_unformatted_text()
                        imgui.text_unformatted(message.strip())
                    finally:
                        imgui.end_tooltip()

    def do_codepoint_process(self, codepoint: CodepointInfo) -> None:
        input_text("Codepoint", f"{codepoint.codepoint:06X}")
        input_text("Category", codepoint.category)
        input_text("Combining", str(codepoint.combining))
        input_text("Bidirectional", codepoint.bidirectional)
        input_text("Name", codepoint.name)
        input_text("Exists", str(codepoint.exists))
        input_text("Glyph", codepoint.glyph)

        if codepoint.exists:
            self.do_glyph_process(codepoint.character)

    def do_glyph_process(self, char: str) -> None:
        text_color = imgui.get_color_u32(self.text_color)
        cell_size = self.config.preview_size
        rounding = self.config.rounding
        rect_flags = self.config.rect_flags
        thickness = self.config.thickness

        cursor = imgui.get_cursor_screen_pos()
        r_min = cursor.x, cursor.y
        r_max = r_min[0] + cell_size, r_min[1] + cell_size

        with begin_child_context("Glyph", size=(cell_size, cell_size)):
            draw_list = get_window_draw_list()

            draw_list.add_rect(
                r_min,
                r_max,
                text_color,
                rounding,
                rect_flags,
                thickness,
            )

            self._atlas.add_text_atlas(char, r_min, text_color, draw_list)
