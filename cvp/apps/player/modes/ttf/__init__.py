# -*- coding: utf-8 -*-

from math import isqrt
from typing import Dict, Final, List, Optional

from imgui_bundle import imgui
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FORMAT_FONT
from cvp.context.context import Context
from cvp.fonts.codepoint_info import CodepointInfo
from cvp.fonts.ranges import BlockRange
from cvp.fonts.ttf import TTF
from cvp.imgui.begin_child import begin_child_context
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
from cvp.imgui.widgets.canvas.image import ImageCanvas
from cvp.logging.logging import logger
from cvp.types.colors import RGBA
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX


class TTFMode(BaseMode):
    __cvp_mode_name__ = "TTF Font"
    __cvp_mode_icon__ = FORMAT_FONT

    _EMPTY_CODEPOINT_INFO = CodepointInfo(0)

    _PLANES_SPLIT_X: Final[int] = 150
    _PLANES_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _CANVAS_SPLIT_X: Final[int] = -400
    _CANVAS_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS
    _INFOS_CHILD_FLAGS: Final[int] = BORDERS

    _ttf: Optional[TTF]
    _blocks: List[BlockRange]
    _codepoints: Dict[int, CodepointInfo]

    def __init__(self, context: Context):
        super().__init__(context)
        self._open_font_popup = OpenFilePopup(
            title="Load font",
            target=self.on_load_font,
        )

        self._menus = MenuList(("File", self.on_file_menu))
        self._popups = PopupList(self._open_font_popup)

        self._ttf = None
        self._blocks = list()
        self._codepoints = dict()
        self._canvas = ImageCanvas()
        self._selected_block_index = NOT_FOUND_INDEX
        self._selected_codepoint = NOT_FOUND_INDEX

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

    @property
    def opened(self) -> bool:
        return self._ttf is not None

    @property
    def path(self) -> str:
        return str(self._ttf.path) if self._ttf is not None else str()

    def open_font_file(self, file: str) -> None:
        try:
            ttf = TTF.from_filepath(file)
            blocks = ttf.get_block_ranges(self.config.block_size)

            self._ttf = ttf
            self._blocks = blocks
            self._codepoints.clear()

            # self._canvas.open_with_pillow(self._image)
            self.add_recent_item(file)
            logger.info(f"Font file opened: '{file}'")
        except BaseException as e:
            logger.error(f"Failed to open font file '{file}': {e}")
            raise

    def close(self) -> None:
        if self._ttf is None:
            raise ValueError("Font file not opened")

        self._ttf.close()
        self._ttf = None
        self._blocks.clear()
        self._codepoints.clear()
        # self._canvas.close()
        logger.info("Font file closed")

    def get_codepoint_info(self, codepoint: int) -> CodepointInfo:
        info = self._codepoints.get(codepoint)
        if info is None:
            info = CodepointInfo(codepoint, self._ttf)
            self._codepoints[codepoint] = info
        return info

    def get_current_codepoint_info(self) -> CodepointInfo:
        if not (0 <= self._selected_block_index < len(self._blocks)):
            return self._EMPTY_CODEPOINT_INFO

        block = self._blocks[self._selected_block_index]
        if not (block.begin <= self._selected_codepoint < block.end):
            return self._EMPTY_CODEPOINT_INFO

        codepoint = self._codepoints.get(self._selected_codepoint)
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
        if menu_item("Close font", enabled=self.opened):
            self.close()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            imgui.text(self.path)

            with begin_child_context(
                label="Planes",
                size=(self._PLANES_SPLIT_X, 0),
                child_flags=self._PLANES_CHILD_FLAGS,
            ):
                if imgui.begin_list_box("##Planes", FIT_SIZE):
                    try:
                        if self._blocks:
                            for i, block in enumerate(self._blocks):
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
                if self.opened:
                    if 0 <= self._selected_block_index < len(self._blocks):
                        block = self._blocks[self._selected_block_index]
                        self.do_codepoint_matrix(block)
                    else:
                        text_centered("Please select a block range")
                else:
                    text_centered("Please open the font")

            imgui.same_line()

            with begin_child_context("Infos", child_flags=self._INFOS_CHILD_FLAGS):
                if self.opened:
                    # self._canvas.do_process()
                    codepoint = self.get_current_codepoint_info()
                    self.on_codepoint_process(codepoint)
                else:
                    text_centered("Please open the font")

        self._popups.do_process()

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
            cp_detail = self.get_codepoint_info(codepoint)
            stroke_color = normal_stroke_color if cp_detail else error_stroke_color

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

            if cp_detail:
                draw_list.add_text(r_min, text_color, cp_detail.character)

            child_focused = imgui.is_window_focused(focused.ROOT_AND_CHILD_WINDOWS)
            child_hovered = imgui.is_window_hovered(hovered.ROOT_AND_CHILD_WINDOWS)
            if child_focused and imgui.is_mouse_hovering_rect(r_min, r_max):
                if child_hovered and imgui.is_mouse_clicked(MOUSE_LEFT):
                    self._selected_codepoint = codepoint

                if imgui.begin_tooltip():
                    try:
                        message = cp_detail.as_unformatted_text()
                        imgui.text_unformatted(message.strip())
                    finally:
                        imgui.end_tooltip()

    @staticmethod
    def on_codepoint_process(codepoint: CodepointInfo) -> None:
        input_text("Codepoint", str(codepoint.codepoint))
        input_text("Category", codepoint.category)
        input_text("Combining", str(codepoint.combining))
        input_text("Bidirectional", codepoint.bidirectional)
        input_text("Name", codepoint.name)
        input_text("Exists", str(codepoint.exists))
        input_text("Glyph", codepoint.glyph)
