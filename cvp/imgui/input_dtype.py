# -*- coding: utf-8 -*-

from typing import Any, NamedTuple, Optional

from imgui_bundle import imgui

from cvp.dtypes.dtype import Dtype
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.memory.constraints import Constraints


class InputAnyResult(NamedTuple):
    changed: bool
    value: Any

    def __bool__(self):
        return self.changed


def input_dtype(
    label: str,
    value: Any,
    dtype: Dtype,
    constraints: Optional[Constraints] = None,
) -> InputAnyResult:
    if constraints is None:
        constraints = Constraints()

    assert constraints is not None
    result_changed = False
    result_value = value

    if dtype.type is type(None):
        if not isinstance(value, type(None)):
            raise TypeError("The type of the value must be none type")

        input_text_disabled(label, "None")
    elif dtype.type is Any:
        input_text_disabled(label, str(value))
    elif dtype.type is bool:
        if value is None:
            value = False
        if not isinstance(value, bool):
            raise TypeError("The type of the value must be bool type")

        b_index = 1 if value else 0
        result = imgui.combo(label, b_index, ["False", "True"])
        result_changed = result[0]
        result_value = bool(result[1])
    elif dtype.type is int:
        if value is None:
            value = 0
        if not isinstance(value, int):
            raise TypeError("The type of the value must be int type")

        i_step = int(constraints.step)
        i_fast = int(constraints.step_fast)
        i_flags = constraints.flags

        result = imgui.input_int(label, value, i_step, i_fast, i_flags)
        result_changed = result[0]
        result_value = result[1]
    elif dtype.type is float:
        if value is None:
            value = 0.0
        if not isinstance(value, float):
            raise TypeError("The type of the value must be float type")
        f_step = float(constraints.step)
        f_fast = float(constraints.step_fast)
        f_fmt = constraints.float_format
        f_flags = constraints.flags

        result = imgui.input_float(label, value, f_step, f_fast, f_fmt, f_flags)
        result_changed = result[0]
        result_value = result[1]
    elif dtype.type is complex:
        raise NotImplementedError
    elif dtype.type is tuple:
        raise NotImplementedError
    elif dtype.type is list:
        raise NotImplementedError
    elif dtype.type is set:
        raise NotImplementedError
    elif dtype.type is dict:
        raise NotImplementedError
    elif dtype.type is bytes:
        raise NotImplementedError
    elif dtype.type is str:
        if value is None:
            value = ""
        if not isinstance(value, str):
            raise TypeError("The type of the value must be str type")
        s_maxlen = -1
        s_flags = 0

        result = imgui.input_text(label, value, s_maxlen, s_flags)
        result_changed = result[0]
        result_value = result[1]
    elif dtype.type is object:
        raise NotImplementedError
    else:
        raise TypeError(f"Unsupported type: {dtype.type.__name__}")

    return InputAnyResult(result_changed, result_value)
