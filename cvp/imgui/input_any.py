# -*- coding: utf-8 -*-

from typing import Any, NamedTuple

import imgui

from cvp.memory.constraints import Constraints


class InputAnyResult(NamedTuple):
    changed: bool
    value: Any

    def __bool__(self):
        return self.changed


def input_any(
    label: str,
    value: Any,
    *args: Constraints,
    **kwargs: Constraints,
) -> InputAnyResult:
    if args and kwargs:
        raise ValueError("*args and **kwargs cannot coexist")

    result_changed = False
    result_value = value

    if isinstance(value, bool):
        raise NotImplementedError
    elif isinstance(value, int):
        constraints = args[0] if args else Constraints()

        i_step = int(constraints.step)
        i_fast = int(constraints.step_fast)
        i_flags = constraints.flags

        result = imgui.input_int(label, value, i_step, i_fast, i_flags)
        result_changed = result[0]
        result_value = result[1]
    elif isinstance(value, float):
        constraints = args[0] if args else Constraints()

        f_step = float(constraints.step)
        f_fast = float(constraints.step_fast)
        f_fmt = constraints.float_format
        f_flags = constraints.flags

        result = imgui.input_float(label, value, f_step, f_fast, f_fmt, f_flags)
        result_changed = result[0]
        result_value = result[1]
    elif isinstance(value, tuple):
        if value:
            raise NotImplementedError
    elif isinstance(value, list):
        if value:
            raise NotImplementedError
    elif isinstance(value, dict):
        if value:
            raise NotImplementedError
    else:
        raise TypeError(f"Unsupported type: {type(value).__name__}")

    return InputAnyResult(result_changed, result_value)
