# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def input_int_value(
    label: str,
    value: int,
    step=1,
    step_fast=100,
    flags=0,
) -> int:
    changed, value = imgui.input_int(label, value, step, step_fast, flags)
    assert isinstance(changed, bool)
    assert isinstance(value, int)
    return value
