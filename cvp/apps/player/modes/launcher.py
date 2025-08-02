# -*- coding: utf-8 -*-

from typing import Any, Optional, Type

from pygame.event import Event
from pygame.key import get_pressed

from cvp.apps.player.modes.interface import ModeInterface
from cvp.context.context import Context
from cvp.context.temp import TempContext
from cvp.imgui.begin_main_menu_bar import begin_main_menu_bar_context
from cvp.imgui.begin_main_status_bar import begin_main_status_bar_context
from cvp.renderer.pygame.demos.simple import SimpleDemoBase
from cvp.types.override import override


class ModeLauncher(SimpleDemoBase):
    def __init__(
        self,
        mode: ModeInterface,
        context: Optional[Context] = None,
        *,
        force_egl: Optional[bool] = None,
        use_accelerate: Optional[bool] = None,
        hidden=False,
        minimize=False,
        font_name=SimpleDemoBase.DEFAULT_FONT_NAME,
        font_size=SimpleDemoBase.DEFAULT_FONT_SIZE,
        font_init=False,
    ):
        if context is None:
            context = getattr(mode, "context", None)

        if context is not None:
            if not isinstance(context, Context):
                raise TypeError("The context attribute must be of type Context")

        super().__init__(
            force_egl=force_egl,
            use_accelerate=use_accelerate,
            pygame_hide_support_prompt=True,
            hidden=hidden,
            minimize=minimize,
            force_exit_before_flip=False,
            font_name=font_name,
            font_size=font_size,
            font_init=font_init,
        )

        self._mode = mode
        self._context = context

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


def launch_mode(cls: Type[ModeInterface], context: Optional[Context] = None) -> None:
    if context is None:
        context = TempContext()
    assert isinstance(context, Context)
    mode = cls(context)

    args = ModeLauncher.parse_arguments()
    launcher = ModeLauncher(
        mode=mode,
        context=context,
        force_egl=args.force_egl,
        use_accelerate=args.use_accelerate,
        hidden=args.hidden,
        minimize=args.minimize,
        font_name=args.default_font_name,
        font_size=args.default_font_size,
        font_init=args.no_default_font,
    )
    launcher.run()
