# -*- coding: utf-8 -*-

from math import isqrt
from typing import Final

from fontTools.ttLib.ttFont import GlyphOrder
from imgui_bundle import imgui
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FORMAT_FONT
from cvp.concurrency.threading.progress_value import ProgressValue
from cvp.context.context import Context
from cvp.fonts.codepoint_info import CodepointInfo
from cvp.fonts.ranges import BlockRange
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.draw_list.atlas.font import FontAtlas, FontAtlasLoader
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags import focused, hovered
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.mouse_button import MOUSE_LEFT
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS
from cvp.imgui.input_text import input_text
from cvp.imgui.menu_container import MenuList
from cvp.imgui.menu_item import menu_item
from cvp.imgui.menu_recent_items import menu_recent_items
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.selectable import selectable
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text
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
            title="Open font",
            target=self.on_open_font,
        )
        self._open_runner = context.create_thread_runner(self.on_open_runner)
        self._open_progress = ProgressValue()

        self._menus = MenuList(("File", self.on_file_menu))
        self._popups = PopupList(self._open_font_popup)

        self._atlas = FontAtlas()

        self._selected_block_index = 0
        self._selected_codepoint = 0
        self._selected_table_name = str()

    def on_open_font(self, file: str) -> None:
        self.open_font_file(file)

    @staticmethod
    def on_open_runner(file: str, font_size: int, progress: ProgressValue):
        try:
            loader = FontAtlasLoader(
                file,
                font_size,
                callback=lambda c, m: progress.set(c, limit=m),
            )
            logger.info(f"Font file loaded: '{file}'")
            return loader
        except BaseException as e:
            logger.error(f"Failed to load font file '{file}': {e}")
            raise

    def open_font_file(self, file: str) -> None:
        if self._open_runner.running:
            raise ValueError("Open runner is already running")

        if self._atlas.opened:
            self._atlas.close()
            logger.info("Font file closed")

        try:
            self._open_runner(file, self.config.preview_size, self._open_progress)
            self.add_recent_item(file)
        except BaseException as e:
            logger.exception(e)
            self.context.toast_error(f"Font open failed: '{e}'")

    def close(self) -> None:
        if self._open_runner.running:
            raise ValueError("Open runner is already running")

        if not self._atlas.opened:
            raise ValueError("Font file not opened")

        self._atlas.close()
        logger.info("Font file closed")

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
    def error_color(self) -> RGBA:
        return self.context.config.appearance.error_color

    def get_current_codepoint_info(self) -> CodepointInfo:
        assert not self._open_runner.running
        assert self._atlas.opened

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
        if self._open_runner.running:
            value, limit, _ = self._open_progress.get()
            imgui.text(f"Opening {value}/{limit} ...")
            return

        if self._open_runner.error is not None:
            error_message = str(self._open_runner.error)
            imgui.text_colored(self.error_color, error_message)
            return

        if not self._atlas.opened:
            imgui.text("Not opened")
            return

        imgui.text(self._atlas.path)

    @override
    def on_event(self, event: Event) -> bool:
        if event.type == DROPFILE:
            self.open_font_file(event.file)
            return True

        return False

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
                self.on_main_process()
        self._popups.do_process()

    def on_main_process(self) -> None:
        with begin_child_context("Main"):
            if self._open_runner.running:
                value, limit, _ = self._open_progress.get()
                overlay = f"Opening {value}/{limit} ..."
                imgui.progress_bar(value / limit, None, overlay)
                return

            if self._open_runner.error is not None:
                error_message = str(self._open_runner.error)
                imgui.text_colored(self.error_color, error_message)
                return

            if not self._atlas.opened:
                if self._open_runner.result is None:
                    text_centered("Please open the font")
                    return

                loader = self._open_runner.result
                assert isinstance(loader, FontAtlasLoader)
                self._atlas.open_with_loader(loader)
                logger.info(f"Font file opened: '{self._atlas.path}'")
                assert self._atlas.opened
                assert self._atlas.ttf is not None
                self._open_runner.clear()

            assert self._atlas.ttf is not None
            self.on_opened_main_process()

    def on_opened_main_process(self) -> None:
        assert not self._open_runner.running
        assert self._open_runner.error is None
        assert self._atlas.opened
        assert self._atlas.ttf is not None

        if imgui.begin_tab_bar("Tabs"):
            try:
                if imgui.begin_tab_item("Basic")[0]:
                    try:
                        self.on_basic_process()
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
                                table_any(f"Table##{tag}", table)
                            finally:
                                imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()

    def on_basic_process(self) -> None:
        assert not self._open_runner.running
        assert self._open_runner.error is None
        assert self._atlas.opened
        assert self._atlas.ttf is not None

        input_text("Font file path", f"{str(self._atlas.path)}")
        input_text("Font size", f"{self._atlas.font_size}")
        input_text("Font texture size", f"{self._atlas.size}")
        input_text("Font block size", f"{self._atlas.block_size:06X}")
        input_text("Font blocks count", f"{len(self._atlas.blocks)}")
        input_text("Font codepoints count", f"{len(self._atlas.codepoints)}")

        ttf = self._atlas.ttf

        input_text("Units per EM (head)", str(ttf.units_per_em))
        hovered_tooltip_text(type(ttf).units_per_em.__doc__)

        input_text("Ascent (hhea)", str(ttf.ascent))
        hovered_tooltip_text(type(ttf).ascent.__doc__)

        input_text("Descent (hhea)", str(ttf.descent))
        hovered_tooltip_text(type(ttf).descent.__doc__)

        input_text("Line Gap (hhea)", str(ttf.line_gap))
        hovered_tooltip_text(type(ttf).line_gap.__doc__)

        input_text("Typo ascender (OS/2)", str(ttf.typo_ascender))
        hovered_tooltip_text(type(ttf).typo_ascender.__doc__)

        input_text("Typo descender (OS/2)", str(ttf.typo_descender))
        hovered_tooltip_text(type(ttf).typo_descender.__doc__)

        input_text("Typo line gap (OS/2)", str(ttf.typo_line_gap))
        hovered_tooltip_text(type(ttf).typo_line_gap.__doc__)

        input_text("x-height (OS/2)", str(ttf.x_height))
        hovered_tooltip_text(type(ttf).x_height.__doc__)

        input_text("Cap height (OS/2)", str(ttf.cap_height))
        hovered_tooltip_text(type(ttf).cap_height.__doc__)

        if imgui.begin_table("Names", 8, DEFAULT_TABLE_FLAGS):
            try:
                imgui.table_setup_column("Platform ID")
                imgui.table_setup_column("Platform")
                imgui.table_setup_column("Encoding ID")
                imgui.table_setup_column("Encoding")
                imgui.table_setup_column("Language ID")
                imgui.table_setup_column("Name ID")
                imgui.table_setup_column("Description")
                imgui.table_setup_column("Value")
                imgui.table_headers_row()

                for name in ttf.names:
                    imgui.table_next_row()

                    imgui.table_set_column_index(0)
                    imgui.text(str(name.platform_id))

                    if platform := name.platform:
                        imgui.table_set_column_index(1)
                        imgui.text(platform)

                    imgui.table_set_column_index(2)
                    imgui.text(str(name.encoding_id))

                    if encoding := name.encoding:
                        imgui.table_set_column_index(3)
                        imgui.text(encoding)

                    imgui.table_set_column_index(4)
                    imgui.text(str(name.language_id))

                    imgui.table_set_column_index(5)
                    imgui.text(str(name.name_id))

                    imgui.table_set_column_index(6)
                    imgui.text(str(name.name_description))

                    imgui.table_set_column_index(7)
                    imgui.text(name.value)
            finally:
                imgui.end_table()

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
