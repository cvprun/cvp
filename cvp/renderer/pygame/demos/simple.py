# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from os import environ
from typing import Any, Callable, Final, List, Optional


class SimpleDemoBase:
    DEFAULT_FONT_NAME: Final[str] = "Default"
    DEFAULT_FONT_SIZE: Final[int] = 14

    def __init__(
        self,
        frame_callback: Optional[Callable[[], None]] = None,
        *,
        force_egl: Optional[bool] = None,
        use_accelerate: Optional[bool] = None,
        pygame_hide_support_prompt: Optional[bool] = None,
        hidden=False,
        minimize=False,
        force_exit_before_flip=False,
        font_name=DEFAULT_FONT_NAME,
        font_size=DEFAULT_FONT_SIZE,
        font_init=False,
    ) -> None:
        from cvp.system.environ_keys import (
            PYGAME_HIDE_SUPPORT_PROMPT,
            PYOPENGL_USE_ACCELERATE,
            SDL_VIDEO_X11_FORCE_EGL,
        )

        if force_egl is not None:
            environ[SDL_VIDEO_X11_FORCE_EGL] = "1" if force_egl else "0"
        if use_accelerate is not None:
            environ[PYOPENGL_USE_ACCELERATE] = "1" if use_accelerate else "0"
        if pygame_hide_support_prompt is not None:
            environ[PYGAME_HIDE_SUPPORT_PROMPT] = "1" if use_accelerate else "0"

        self._frame_callback = frame_callback
        self._done = False

        self._hidden = hidden
        self._minimize = minimize

        self._font_name = font_name
        self._font_size = font_size
        self._font_init = font_init

        self._force_exit_before_flip = force_exit_before_flip
        """
        The flag variable to force exit just before `pygame.display.flip()` is called.
        """

    @staticmethod
    def parse_arguments(
        cmdline: Optional[List[str]] = None,
        namespace: Optional[Namespace] = None,
    ):
        from cvp.arguments import (
            add_font_arguments,
            add_opengl_arguments,
            get_opengl_config,
        )

        parser = ArgumentParser()

        add_opengl_arguments(parser)
        add_font_arguments(parser)

        parser.add_argument("--hidden", action="store_true", default=False)
        parser.add_argument("--minimize", action="store_true", default=False)
        parser.add_argument("--disable-auto-config", action="store_true", default=False)

        args = parser.parse_known_args(cmdline, namespace)[0]

        assert isinstance(args.force_egl, bool)
        assert isinstance(args.force_glx, bool)
        assert isinstance(args.enable_accelerate, bool)
        assert isinstance(args.disable_accelerate, bool)

        assert isinstance(args.no_default_font, bool)
        assert isinstance(args.default_font_name, str)
        assert isinstance(args.default_font_size, int)

        assert isinstance(args.hidden, bool)
        assert isinstance(args.minimize, bool)
        assert isinstance(args.disable_auto_config, bool)

        if not args.disable_auto_config:
            from cvp.apps.tester.fetch import fetch_best_opengl_config_from_subprocess

            opengl_config = fetch_best_opengl_config_from_subprocess()
            force_egl = opengl_config.force_egl
            use_accelerate = opengl_config.use_accelerate
        else:
            opengl_config = get_opengl_config(args)
            force_egl = opengl_config.force_egl
            use_accelerate = opengl_config.use_accelerate

        class _DemoArguments(Namespace):
            force_egl: Optional[bool]
            use_accelerate: Optional[bool]
            no_default_font: bool
            default_font_name: str
            default_font_size: int
            hidden: bool
            minimize: bool

        return _DemoArguments(
            force_egl=force_egl,
            use_accelerate=use_accelerate,
            no_default_font=args.no_default_font,
            default_font_name=args.default_font_name,
            default_font_size=args.default_font_size,
            hidden=args.hidden,
            minimize=args.minimize,
        )

    @property
    def done(self) -> bool:
        return self._done

    @done.setter
    def done(self, value: bool) -> None:
        self._done = value

    def on_event(self, event: Any) -> bool:
        return False

    def on_frame(self) -> None:
        if self._frame_callback is not None:
            self._frame_callback()

    def __enter__(self) -> None:
        if __enter__ := getattr(self._frame_callback, "__enter__", None):
            __enter__()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if __exit__ := getattr(self._frame_callback, "__exit__", None):
            __exit__(exc_type, exc_val, exc_tb)

    def run(self) -> None:
        import pygame
        from imgui_bundle import imgui
        from OpenGL import GL

        from cvp.imgui.fonts.defaults import add_mixed_font
        from cvp.renderer.pygame.renderer import PygameRenderer

        pygame.init()

        info = pygame.display.Info()
        size = info.current_w, info.current_h
        flags = pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE
        if self._hidden:
            flags |= pygame.HIDDEN
        pygame.display.set_mode(size, flags)
        if self._minimize:
            pygame.display.iconify()

        imgui.create_context()
        io = imgui.get_io()
        io.display_size = imgui.ImVec2(size[0], size[1])
        io.set_ini_filename(str())
        io.set_log_filename(str())

        renderer = PygameRenderer()

        try:
            if self._font_init:
                io.fonts.clear()
                add_mixed_font(self._font_name, self._font_size)

            with self:
                renderer.refresh_font_texture()

                while not self._done:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self._done = True
                        if not self.on_event(event):
                            renderer.do_event(event)

                    renderer.do_tick()
                    imgui.new_frame()
                    try:
                        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
                        self.on_frame()
                    finally:
                        imgui.render()
                        renderer.render(imgui.get_draw_data())
                        if self._force_exit_before_flip:
                            return
                        pygame.display.flip()
        finally:
            del renderer
            imgui.destroy_context()
            pygame.quit()


def run_simple_demo(frame_callback: Callable[[], None]) -> None:
    args = SimpleDemoBase.parse_arguments()
    demo = SimpleDemoBase(
        frame_callback,
        force_egl=args.force_egl,
        use_accelerate=args.use_accelerate,
        pygame_hide_support_prompt=True,
        hidden=args.hidden,
        minimize=args.minimize,
        force_exit_before_flip=False,
        font_name=args.default_font_name,
        font_size=args.default_font_size,
        font_init=args.no_default_font,
    )
    demo.run()
