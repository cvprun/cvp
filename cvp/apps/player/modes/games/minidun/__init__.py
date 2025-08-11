# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import EMOTICON_DEVIL
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.draw_list.create import create_draw_list_with_shared_data
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.types.override import override


class MinidunMode(BaseMode):
    __cvp_mode_name__ = "Minidun"
    __cvp_mode_icon__ = EMOTICON_DEVIL
    __cvp_mode_show__ = False

    def __init__(self, context: Context):
        super().__init__(context)
        self._draw_list = create_draw_list_with_shared_data()
        self._mouse_pos = 0.0, 0.0
        self._cursor_pos = 0.0, 0.0
        self._cursor_screen_pos = 0.0, 0.0
        self._content_region_size = 0.0, 0.0

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Canvas"):
                self.on_canvas_process()

    def on_canvas_process(self) -> None:
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
