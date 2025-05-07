# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.renderer.pygame.demos.simple import run_simple_demo


def on_frame() -> None:
    imgui.begin("Style editor")
    imgui.show_style_editor()
    imgui.end()


if __name__ == "__main__":
    run_simple_demo(on_frame, force_egl=True, use_accelerate=False)
