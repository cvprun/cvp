# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from typing import Any, Final, List, Optional

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import get_pressed

from cvp.apps.player.modes.interface import ModeInterface
from cvp.arguments import add_opengl_arguments
from cvp.context.context import Context
from cvp.imgui.begin_main_menu_bar import begin_main_menu_bar_context
from cvp.imgui.begin_main_status_bar import begin_main_status_bar_context
from cvp.imgui.fonts.defaults import add_mixed_font
from cvp.renderer.pygame.demos.simple import SimpleDemoBase
from cvp.types.override import override


class ModeLauncher(SimpleDemoBase):
    DEFAULT_FONT_NAME: Final[str] = "Default"
    DEFAULT_FONT_SIZE: Final[int] = 12

    def __init__(
        self,
        mode: ModeInterface,
        context: Optional[Context] = None,
        *,
        force_egl: Optional[bool] = True,
        use_accelerate: Optional[bool] = False,
        font_name=DEFAULT_FONT_NAME,
        font_size=DEFAULT_FONT_SIZE,
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

    @classmethod
    def from_args(
        cls,
        mode: ModeInterface,
        cmdline: Optional[List[str]] = None,
        namespace: Optional[Namespace] = None,
    ):
        parser = ArgumentParser()
        add_opengl_arguments(parser)

        parser.add_argument(
            "--font-name",
            type=str,
            default=cls.DEFAULT_FONT_NAME,
            metavar="{name}",
            help=f"Default font name (default: '{cls.DEFAULT_FONT_NAME}')",
        )
        parser.add_argument(
            "--font-size",
            type=int,
            default=cls.DEFAULT_FONT_SIZE,
            metavar="{pt}",
            help=f"Default font size (default: '{cls.DEFAULT_FONT_SIZE}')",
        )

        args = parser.parse_known_args(cmdline, namespace)[0]
        assert isinstance(args.force_egl, bool)
        assert isinstance(args.use_accelerate, bool)
        assert isinstance(args.font_name, str)
        assert isinstance(args.font_size, int)

        return cls(
            mode,
            force_egl=args.force_egl,
            use_accelerate=args.use_accelerate,
            font_name=args.font_name,
            font_size=args.font_size,
        )

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
