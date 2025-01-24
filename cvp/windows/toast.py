# -*- coding: utf-8 -*-

from collections import deque
from time import time
from typing import Deque, Final, Optional, Union

import imgui

from cvp.config.sections.toast import ToastWindowConfig
from cvp.imgui.draw_list.get_draw_list import get_foreground_draw_list
from cvp.imgui.measure_window_roi import get_window_roi
from cvp.logging.logging import INFO, convert_level_number
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.transitions.fade import measure_fade_ratio
from cvp.types.override import override

TOAST_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_ALWAYS_AUTO_RESIZE
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_MOVE
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_UNSAVED_DOCUMENT
    | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
    | imgui.WINDOW_NO_FOCUS_ON_APPEARING
    | imgui.WINDOW_NO_INPUTS
)


class ToastMessage:
    def __init__(self, message: str, level: Optional[Union[int, str]] = None):
        if level is None:
            level = INFO

        assert level is not None
        assert isinstance(level, (int, str))

        self.message = message
        self.level = convert_level_number(level)


class ToastWindow(WindowBase[ToastWindowConfig]):
    _items: Deque[ToastMessage]

    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.toast_window,
            title="Toast",
            closable=False,
            flags=TOAST_WINDOW_FLAGS,
        )
        self._items = deque()
        self._begin = time()

    def reset_timer(self) -> None:
        self._begin = time()

    def pop_item(self) -> None:
        if not self._items:
            return
        self._items.pop()
        self.reset_timer()

    def show_toast(self, item: ToastMessage) -> None:
        if not self._items:
            self.reset_timer()

        self._items.append(item)
        self.opened = True

    def show_simple(self, message: str) -> None:
        self.show_toast(ToastMessage(message))

    @property
    def fadein(self):
        return self.window_config.fadein

    @property
    def fadeout(self):
        return self.window_config.fadeout

    @property
    def waiting(self):
        return self.window_config.waiting

    def update_alpha(self, now: float) -> float:
        elapsed = now - self._begin
        return measure_fade_ratio(elapsed, self.fadein, self.waiting, self.fadeout)

    def get_window_roi(self, message: str):
        text_width, text_height = imgui.calc_text_size(message)
        assert isinstance(text_width, float)
        assert isinstance(text_height, float)
        return get_window_roi(
            content_width=text_width,
            content_height=text_height,
            pivot_x=self.window_config.pivot_x,
            pivot_y=self.window_config.pivot_y,
            anchor_x=self.window_config.anchor_x,
            anchor_y=self.window_config.anchor_y,
            margin_x=self.window_config.margin_x,
            margin_y=self.window_config.margin_y,
            padding_x=self.window_config.padding_x,
            padding_y=self.window_config.padding_y,
        )

    @override
    def on_before(self) -> None:
        imgui.set_next_window_bg_alpha(0)

    @override
    def on_process(self) -> None:
        if not self._items:
            self.opened = False
            return

        try:
            alpha = self.update_alpha(time())
        except ValueError:
            self.pop_item()
            return

        current_item = self._items[0]
        message = current_item.message
        level = current_item.level

        br, bg, bb = self._window_config.background_color
        assert isinstance(br, float)
        assert isinstance(bg, float)
        assert isinstance(bb, float)
        background_color = imgui.get_color_u32_rgba(br, bg, bb, alpha)

        fr, fg, fb = self._window_config.get_level_color(level)
        assert isinstance(fr, float)
        assert isinstance(fg, float)
        assert isinstance(fb, float)
        foreground_color = imgui.get_color_u32_rgba(fr, fg, fb, alpha)

        padding_x = self._window_config.padding_x
        padding_y = self._window_config.padding_y
        rounding = self._window_config.rounding

        x1, y1, x2, y2 = self.get_window_roi(message)
        draw_list = get_foreground_draw_list()
        draw_list.add_rect_filled(x1, y1, x2, y2, background_color, rounding)

        text_x = x1 + padding_x
        text_y = y1 + padding_y
        draw_list.add_text(text_x, text_y, foreground_color, message)

        mx, my = imgui.get_mouse_pos()
        assert isinstance(mx, float)
        assert isinstance(my, float)

        hovering = x1 <= mx <= x2 and y1 <= my <= y2
        clicked = imgui.is_mouse_clicked(imgui.MOUSE_BUTTON_LEFT)

        if hovering and clicked:
            self.pop_item()
