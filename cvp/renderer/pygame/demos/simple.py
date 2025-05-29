# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from os import environ
from typing import Callable, Optional


class SimpleDemoInterface(ABC):
    @abstractmethod
    def on_init(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_frame(self) -> None:
        raise NotImplementedError


class SimpleDemoBase(SimpleDemoInterface):
    def __init__(
        self,
        frame_callback: Optional[Callable[[], None]] = None,
        *,
        force_egl: Optional[bool] = True,
        use_accelerate: Optional[bool] = False,
        init_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        if force_egl is not None:
            environ["SDL_VIDEO_X11_FORCE_EGL"] = "1" if force_egl else "0"
        if use_accelerate is not None:
            environ["PYOPENGL_USE_ACCELERATE"] = "1" if use_accelerate else "0"

        self._frame_callback = frame_callback
        self._init_callback = init_callback
        self._done = False

    @property
    def done(self) -> bool:
        return self._done

    @done.setter
    def done(self, value: bool) -> None:
        self._done = value

    def run(self) -> None:
        import pygame
        from imgui_bundle import imgui
        from OpenGL import GL

        from cvp.gl.accelerate import load_accelerate
        from cvp.renderer.pygame.renderer import PygameRenderer

        load_accelerate()

        pygame.init()

        info = pygame.display.Info()
        size = info.current_w, info.current_h
        flags = pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE
        pygame.display.set_mode(size, flags)

        imgui.create_context()
        io = imgui.get_io()
        io.display_size = imgui.ImVec2(size[0], size[1])
        io.set_ini_filename(str())
        io.set_log_filename(str())

        renderer = PygameRenderer()
        self.on_init()
        renderer.refresh_font_texture()

        try:
            while not self._done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._done = True
                    renderer.do_event(event)

                renderer.do_tick()
                imgui.new_frame()
                try:
                    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
                    self.on_frame()
                finally:
                    imgui.render()
                    renderer.render(imgui.get_draw_data())
                    pygame.display.flip()
        finally:
            del renderer
            imgui.destroy_context()
            pygame.quit()

    def on_init(self) -> None:
        if self._init_callback is not None:
            self._init_callback()

    def on_frame(self) -> None:
        if self._frame_callback is not None:
            self._frame_callback()


def run_simple_demo(
    frame_callback: Callable[[], None],
    *,
    force_egl: Optional[bool] = False,
    use_accelerate: Optional[bool] = False,
    init_callback: Optional[Callable[[], None]] = None,
) -> None:
    demo = SimpleDemoBase(
        frame_callback,
        force_egl=force_egl,
        use_accelerate=use_accelerate,
        init_callback=init_callback,
    )
    demo.run()
