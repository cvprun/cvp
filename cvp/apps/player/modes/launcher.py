# -*- coding: utf-8 -*-

from typing import Any, Optional

from imgui_bundle import imgui
from pygame.event import Event

from cvp.apps.player.modes.interface import ModeInterface
from cvp.imgui.fonts.defaults import add_mixed_font
from cvp.renderer.pygame.demos.simple import SimpleDemoBase
from cvp.types.override import override


class ModeLauncher(SimpleDemoBase):
    def __init__(
        self,
        mode: ModeInterface,
        *,
        force_egl: Optional[bool] = True,
        use_accelerate: Optional[bool] = False,
        font_name="Default",
        font_size=12,
    ):
        super().__init__(force_egl=force_egl, use_accelerate=use_accelerate)
        self._mode = mode
        self._font_name = font_name
        self._font_size = font_size

    @property
    def mode(self):
        return self._mode

    @override
    def on_init(self) -> None:
        imgui.get_io().fonts.clear()
        add_mixed_font(self._font_name, self._font_size)

    @override
    def on_event(self, event: Any) -> bool:
        assert isinstance(event, Event)
        return self._mode.on_event(event)

    @override
    def on_frame(self) -> None:
        imgui.begin_main_menu_bar()
        try:
            self._mode.on_main_menu()
        finally:
            imgui.end_main_menu_bar()

        self._mode.on_process()
