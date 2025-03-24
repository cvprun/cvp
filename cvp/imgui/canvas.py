# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Final, Optional, Union

from imgui_bundle import imgui

from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags.child import BORDERS, ChildFlags
from cvp.imgui.flags.color_var import CHILD_BG
from cvp.imgui.flags.style_var import WINDOW_PADDING
from cvp.imgui.flags.window import CANVAS_FLAGS, WindowFlags
from cvp.types.colors import GRAY_RGBA


class NoPaddingSize:
    pass


NO_PADDING_SIZE: Final[NoPaddingSize] = NoPaddingSize()


@contextmanager
def canvas_context(
    label: Union[str, int],
    size: Optional[Union[NoPaddingSize, imgui.ImVec2Like]] = NO_PADDING_SIZE,
    child_flags: Union[ChildFlags, int] = BORDERS,
    window_flags: Union[WindowFlags, int] = CANVAS_FLAGS,
    *,
    clear_color=GRAY_RGBA,
    rect_filled=False,
):
    if isinstance(child_flags, ChildFlags):
        child_flags = int(child_flags)

    if isinstance(window_flags, WindowFlags):
        window_flags = int(window_flags)

    if isinstance(size, NoPaddingSize):
        size = 0, -imgui.get_style().item_spacing.y

    assert isinstance(child_flags, int)
    assert isinstance(window_flags, int)

    clear_color_u32 = imgui.get_color_u32(clear_color)

    imgui.push_style_var(WINDOW_PADDING, (0, 0))
    imgui.push_style_color(CHILD_BG, clear_color_u32)
    imgui.begin_child(label, size, child_flags, window_flags)

    try:
        draw_list = get_window_draw_list()
        if rect_filled:
            screen_pos = imgui.get_cursor_screen_pos()
            region_size = imgui.get_content_region_avail()
            cx, cy = screen_pos.x, screen_pos.y
            cw, ch = region_size.x, region_size.y
            assert isinstance(cx, float)
            assert isinstance(cy, float)
            assert isinstance(cw, float)
            assert isinstance(ch, float)

            draw_list.add_rect_filled(cx, cy, cx + cw, cy + ch, clear_color_u32)
        yield draw_list
    finally:
        imgui.end_child()
        imgui.pop_style_color()
        imgui.pop_style_var()
