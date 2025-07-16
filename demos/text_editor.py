# -*- coding: utf-8 -*-

from cvp.apps.player.modes.text import TextMode
from cvp.context.temp import TempContext
from cvp.renderer.pygame.demos.simple import run_simple_demo


class OnFrame:
    def __init__(self):
        self._text = TextMode(TempContext())

    def __call__(self):
        self._text.on_process()


if __name__ == "__main__":
    run_simple_demo(OnFrame(), force_egl=True, use_accelerate=False)
