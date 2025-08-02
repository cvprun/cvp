# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional


class TesterApplication:
    def __init__(
        self,
        force_egl: Optional[bool] = None,
        use_accelerate: Optional[bool] = None,
        use_simple_window=False,
    ):
        self._force_egl = force_egl
        self._use_accelerate = use_accelerate
        self._use_simple_window = use_simple_window

    def on_frame_with_demo_window(self) -> None:
        from imgui_bundle import imgui

        if self._use_simple_window:
            imgui.begin(type(self).__name__)
            imgui.text(datetime.now().astimezone().isoformat())
            imgui.end()
        else:
            imgui.show_demo_window()

    def start(self) -> None:
        from cvp.renderer.pygame.demos.simple import SimpleDemoBase

        demo = SimpleDemoBase(
            frame_callback=self.on_frame_with_demo_window,
            force_egl=self._force_egl,
            use_accelerate=self._use_accelerate,
            pygame_hide_support_prompt=True,
            init_callback=None,
            event_callback=None,
            hidden=True,
            minimize=False,
            force_exit_before_flip=True,
        )
        demo.run()
