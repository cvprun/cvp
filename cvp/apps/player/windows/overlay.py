# -*- coding: utf-8 -*-

from math import floor
from typing import Final, Tuple

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.flags.condition import ALWAYS
from cvp.imgui.flags.window import WindowFlags, merge_window_flags
from cvp.imgui.menu_item import menu_item
from cvp.imgui.text_colored import text_colored
from cvp.system.usage import SystemUsage
from cvp.types.colors import RGBA

_OVERLAY_WINDOW_FLAGS: Final[int] = merge_window_flags(
    WindowFlags.no_move,
    WindowFlags.always_auto_resize,
    WindowFlags.no_saved_settings,
    WindowFlags.no_docking,
    WindowFlags.no_nav,  # no_nav_inputs | no_nav_focus
    WindowFlags.no_decoration,  # no_title_bar | no_resize | no_scrollbar | no_collapse
    WindowFlags.no_scroll_with_mouse,
    WindowFlags.no_bring_to_front_on_focus,
)


class OverlayWindow:
    def __init__(self, context: Context):
        self._context = context
        self._usage = SystemUsage(interval=1.0)

    @property
    def config(self):
        return self._context.config.overlay

    @property
    def opened(self):
        return self.config.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self.config.opened = value

    def flip_opened(self) -> None:
        self.config.opened = not self.config.opened

    @property
    def is_left_side(self):
        return self.config.is_left_side

    @property
    def is_top_side(self):
        return self.config.is_top_side

    @property
    def window_position(self) -> Tuple[float, float]:
        viewport = imgui.get_main_viewport()
        work_pos = viewport.work_pos  # Use work area to avoid menu-bar/task-bar, if any
        work_size = viewport.work_size
        work_pos_x, work_pos_y = work_pos.x, work_pos.y
        work_size_x, work_size_y = work_size.x, work_size.y
        padding = self.config.padding
        x = work_pos_x + (padding if self.is_left_side else work_size_x - padding)
        y = work_pos_y + (padding if self.is_top_side else work_size_y - padding)
        return x, y

    @property
    def window_pivot(self) -> Tuple[float, float]:
        x = 0.0 if self.is_left_side else 1.0
        y = 0.0 if self.is_top_side else 1.0
        return x, y

    def get_framerate_color(self, framerate: float) -> RGBA:
        if framerate >= self.config.fps_warning_threshold:
            return self.config.normal_color
        elif framerate >= self.config.fps_error_threshold:
            return self.config.warning_color
        else:
            return self.config.error_color

    def on_process(self) -> None:
        if not self.opened:
            return

        pos_x, pos_y = self.window_position
        pivot_x, pivot_y = self.window_pivot
        imgui.set_next_window_pos((pos_x, pos_y), ALWAYS, (pivot_x, pivot_y))
        imgui.set_next_window_bg_alpha(self.config.alpha)
        with begin_context("Overlay", closable=False, flags=_OVERLAY_WINDOW_FLAGS):
            io = imgui.get_io()
            framerate_color = self.get_framerate_color(io.framerate)
            text_colored(f"FPS: {floor(io.framerate)}", framerate_color)

            imgui.text(f"Vertices: {io.metrics_render_vertices}")
            imgui.text(f"Indices: {io.metrics_render_indices}")
            imgui.text(f"Visible Windows: {io.metrics_render_windows}")

            imgui.separator()

            usage = self._usage.get()
            imgui.text(f"CPU: {usage.cpu:3.1f}%")
            imgui.text(f"VMEM: {usage.vmem:3.1f}%")

            imgui.separator()
            mouse_pos = imgui.get_mouse_pos()
            imgui.text(f"Mouse: {floor(mouse_pos.x)}, {floor(mouse_pos.y)}")

            if imgui.begin_popup_context_window():
                try:
                    self.on_popup_context_window()
                finally:
                    imgui.end_popup()

    def on_popup_context_window(self) -> None:
        if menu_item("Top-Left", self.config.is_top_left):
            self.config.set_top_left()
        if menu_item("Top-Right", self.config.is_top_right):
            self.config.set_top_right()
        if menu_item("Bottom-Left", self.config.is_bottom_left):
            self.config.set_bottom_left()
        if menu_item("Bottom-Right", self.config.is_bottom_right):
            self.config.set_bottom_right()

        imgui.separator()

        if menu_item("Close"):
            self.opened = False
