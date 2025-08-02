# -*- coding: utf-8 -*-

from typing import Optional


class TesterApplication:
    def __init__(
        self,
        force_egl: Optional[bool] = None,
        use_accelerate: Optional[bool] = None,
    ):
        self._force_egl = force_egl
        self._use_accelerate = use_accelerate
        self._opened = True

    def on_frame(self) -> None:
        from imgui_bundle import imgui

        opened = imgui.show_demo_window(self._opened)
        assert isinstance(opened, bool)
        self._opened = opened

    def start(self) -> None:
        from cvp.renderer.pygame.demos.simple import SimpleDemoBase

        demo = SimpleDemoBase(
            self.on_frame,
            force_egl=self._force_egl,
            use_accelerate=self._use_accelerate,
            pygame_hide_support_prompt=True,
            hidden=True,
            minimize=False,
            force_exit_before_flip=True,
        )
        demo.run()
