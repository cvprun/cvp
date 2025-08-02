# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.renderer.pygame.demos.simple import run_simple_demo


def on_frame() -> None:
    imgui.show_demo_window()


if __name__ == "__main__":
    run_simple_demo(on_frame)
