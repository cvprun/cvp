# -*- coding: utf-8 -*-

from collections import deque
from time import time
from typing import Deque, Optional, Union

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.calc_text_size import calc_text_size
from cvp.imgui.draw_list.get_draw_list import get_foreground_draw_list
from cvp.imgui.flags.mouse_button import MOUSE_LEFT
from cvp.imgui.flags.window import TOAST_WINDOW_FLAGS
from cvp.imgui.measure_window_roi import get_window_roi
from cvp.logging.logging import INFO, convert_level_number
from cvp.transitions.fade import measure_fade_ratio


class ToastMessage:
    def __init__(self, message: str, level: Optional[Union[int, str]] = None):
        if level is None:
            level = INFO

        assert level is not None
        assert isinstance(level, (int, str))

        self.message = message
        self.level = convert_level_number(level)


class ToastWindow:
    _items: Deque[ToastMessage]

    def __init__(self, context: Context):
        self._context = context
        self._items = deque()
        self._begin = time()
        self._opened = False

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
        self._opened = True

    def show(self, message: str, level: Optional[Union[int, str]] = None) -> None:
        self.show_toast(ToastMessage(message, level))

    @property
    def config(self):
        return self._context.config.toast_window

    @property
    def fadein(self):
        return self.config.fadein

    @property
    def fadeout(self):
        return self.config.fadeout

    @property
    def waiting(self):
        return self.config.waiting

    def update_alpha(self, now: float) -> float:
        elapsed = now - self._begin
        return measure_fade_ratio(elapsed, self.fadein, self.waiting, self.fadeout)

    def get_window_roi(self, message: str):
        text_width, text_height = calc_text_size(message)
        assert isinstance(text_width, float)
        assert isinstance(text_height, float)
        return get_window_roi(
            content_width=text_width,
            content_height=text_height,
            pivot_x=self.config.pivot_x,
            pivot_y=self.config.pivot_y,
            anchor_x=self.config.anchor_x,
            anchor_y=self.config.anchor_y,
            margin_x=self.config.margin_x,
            margin_y=self.config.margin_y,
            padding_x=self.config.padding_x,
            padding_y=self.config.padding_y,
        )

    def on_process(self) -> None:
        if not self._opened:
            return

        imgui.set_next_window_bg_alpha(0)
        with begin_context(type(self).__name__, self._opened, TOAST_WINDOW_FLAGS):
            if not self._items:
                self._opened = False
                return

            try:
                alpha = self.update_alpha(time())
            except ValueError:
                self.pop_item()
                return

            current_item = self._items[0]
            message = current_item.message
            level = current_item.level

            br, bg, bb = self.config.background_color
            assert isinstance(br, float)
            assert isinstance(bg, float)
            assert isinstance(bb, float)
            background_color = imgui.get_color_u32((br, bg, bb, alpha))

            fr, fg, fb = self.config.get_level_color(level)
            assert isinstance(fr, float)
            assert isinstance(fg, float)
            assert isinstance(fb, float)
            foreground_color = imgui.get_color_u32((fr, fg, fb, alpha))

            padding_x = self.config.padding_x
            padding_y = self.config.padding_y
            rounding = self.config.rounding

            x1, y1, x2, y2 = self.get_window_roi(message)
            draw_list = get_foreground_draw_list()
            draw_list.add_rect_filled((x1, y1), (x2, y2), background_color, rounding)

            text_x = x1 + padding_x
            text_y = y1 + padding_y
            draw_list.add_text((text_x, text_y), foreground_color, message)

            mouse_pos = imgui.get_mouse_pos()
            mx, my = mouse_pos.x, mouse_pos.y
            assert isinstance(mx, float)
            assert isinstance(my, float)

            hovering = x1 <= mx <= x2 and y1 <= my <= y2
            clicked = imgui.is_mouse_clicked(MOUSE_LEFT)

            if hovering and clicked:
                self.pop_item()
