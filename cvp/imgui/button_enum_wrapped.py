# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Type

from cvp.imgui.button_wrapped import button_wrapped as _button_wrapped


def button_enum_wrapped(
    enum_type: Type[Enum],
    outer_width: Optional[float] = None,
    *,
    show_debugging=False,
) -> Optional[int]:
    labels = [(e if isinstance(e, str) else e.name) for e in list(enum_type)]
    return _button_wrapped(labels, outer_width, show_debugging=show_debugging)
