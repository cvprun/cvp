# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def checkbox_value(label: str, state: bool) -> bool:
    clicked, state = imgui.checkbox(label, state)
    assert isinstance(clicked, bool)
    assert isinstance(state, bool)
    return state
