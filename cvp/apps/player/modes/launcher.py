# -*- coding: utf-8 -*-

from typing import Any, Optional

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import get_pressed

from cvp.apps.player.modes.interface import ModeInterface
from cvp.context.context import Context
from cvp.imgui.begin_main_menu_bar import begin_main_menu_bar_context
from cvp.imgui.begin_main_status_bar import begin_main_status_bar_context
from cvp.imgui.fonts.defaults import add_mixed_font
from cvp.renderer.pygame.demos.simple import SimpleDemoBase
from cvp.types.override import override


class ModeLauncher(SimpleDemoBase):
    def __init__(
        self,
        mode: ModeInterface,
        context: Optional[Context] = None,
        *,
        force_egl: Optional[bool] = True,
        use_accelerate: Optional[bool] = False,
        font_name="Default",
        font_size=12,
    ):
        if context is None:
            context = getattr(mode, "context", None)

        if context is not None:
            if not isinstance(context, Context):
                raise TypeError("The context attribute must be of type Context")

        super().__init__(force_egl=force_egl, use_accelerate=use_accelerate)

        self._mode = mode
        self._context = context
        self._font_name = font_name
        self._font_size = font_size

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
        if self._context is not None:
            for msg in self._context.msgs.pull_nowait():
                self._mode.on_msg(msg)

        self._mode.on_keyboard(get_pressed())

        with begin_main_menu_bar_context() as menu_open:
            if menu_open:
                self._mode.on_main_menu()

        with begin_main_status_bar_context() as status_open:
            if status_open:
                self._mode.on_status_menu()

        self._mode.on_process()
