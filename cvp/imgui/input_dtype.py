# -*- coding: utf-8 -*-

from typing import Any, NamedTuple, Optional

import imgui

from cvp.dtypes.dtype import Dtype
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
        raise TypeError("Unsupported none type")
    elif dtype.type is bool:
        raise NotImplementedError
    elif dtype.type is int:
        i_step = int(constraints.step)
        i_fast = int(constraints.step_fast)
        i_flags = constraints.flags

        result = imgui.input_int(label, value, i_step, i_fast, i_flags)
        result_changed = result[0]
        result_value = result[1]
    elif dtype.type is float:
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
        s_maxlen = -1
        s_flags = 0

        result = imgui.input_text(label, value, s_maxlen, s_flags)
        result_changed = result[0]
        result_value = result[1]
    elif dtype.type is object:
        raise NotImplementedError
    else:
        raise TypeError(f"Unsupported type: {type(value).__name__}")

    return InputAnyResult(result_changed, result_value)
