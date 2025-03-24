# -*- coding: utf-8 -*-

from math import floor
from typing import Tuple

from imgui_bundle import imgui

from cvp.config.sections.overlay import OverlayWindowConfig
from cvp.imgui.begin_popup_context_window import (
    begin_popup_context_window,
    end_popup_context_window,
)
from cvp.imgui.flags.condition import ALWAYS
from cvp.imgui.flags.window import OVERLAY_WINDOW_FLAGS
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.text_colored import text_colored
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.system.usage import SystemUsage
from cvp.types.colors import RGBA
from cvp.types.override import override


class OverlayWindow(WindowBase[OverlayWindowConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.overlay_window,
            title="Overlay",
            closable=False,
            flags=OVERLAY_WINDOW_FLAGS,
        )
        self._usage = SystemUsage(interval=1.0)

    @property
    def is_left_side(self):
        return self.window_config.is_left_side

    @property
    def is_top_side(self):
        return self.window_config.is_top_side

    @property
    def window_position(self) -> Tuple[float, float]:
        viewport = imgui.get_main_viewport()
        work_pos = viewport.work_pos  # Use work area to avoid menu-bar/task-bar, if any
        work_size = viewport.work_size
        work_pos_x, work_pos_y = work_pos.x, work_pos.y
        work_size_x, work_size_y = work_size.x, work_size.y
        padding = self.window_config.padding
        x = work_pos_x + (padding if self.is_left_side else work_size_x - padding)
        y = work_pos_y + (padding if self.is_top_side else work_size_y - padding)
        return x, y

    @property
    def window_pivot(self) -> Tuple[float, float]:
        x = 0.0 if self.is_left_side else 1.0
        y = 0.0 if self.is_top_side else 1.0
        return x, y

    def get_framerate_color(self, framerate: float) -> RGBA:
        if framerate >= self.window_config.fps_warning_threshold:
            return self.window_config.normal_color
        elif framerate >= self.window_config.fps_error_threshold:
            return self.window_config.warning_color
        else:
            return self.window_config.error_color

    @override
    def begin(self) -> Tuple[bool, bool]:
        pos_x, pos_y = self.window_position
        pivot_x, pivot_y = self.window_pivot
        imgui.set_next_window_pos((pos_x, pos_y), ALWAYS, (pivot_x, pivot_y))
        imgui.set_next_window_bg_alpha(self.window_config.alpha)
        return super().begin()

    @override
    def on_process(self) -> None:
        io = imgui.get_io()
        framerate_color = self.get_framerate_color(io.framerate)
        text_colored(f"FPS: {floor(io.framerate)}", framerate_color)

        imgui.text(f"Vertices: {io.metrics_render_vertices}")
        imgui.text(f"Indices: {io.metrics_render_indices}")
        imgui.text(f"Visible Windows: {io.metrics_render_windows}")

        imgui.separator()

        usage = self._usage.update_interval()
        imgui.text(f"CPU: {usage.cpu:3.1f}%")
        imgui.text(f"VMEM: {usage.vmem:3.1f}%")

        imgui.separator()
        mouse_pos = imgui.get_mouse_pos()
        imgui.text(f"Mouse: {floor(mouse_pos.x)}, {floor(mouse_pos.y)}")

        if begin_popup_context_window().opened:
            try:
                self.on_popup_context_window()
            finally:
                end_popup_context_window()

    def on_popup_context_window(self) -> None:
        if menu_item("Top-Left", self.window_config.is_top_left):
            self.window_config.set_top_left()
        if menu_item("Top-Right", self.window_config.is_top_right):
            self.window_config.set_top_right()
        if menu_item("Bottom-Left", self.window_config.is_bottom_left):
            self.window_config.set_bottom_left()
        if menu_item("Bottom-Right", self.window_config.is_bottom_right):
            self.window_config.set_bottom_right()

        imgui.separator()

        if menu_item("Close"):
            self.opened = False
