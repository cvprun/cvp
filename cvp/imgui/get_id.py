# -*- coding: utf-8 -*-

from typing import Optional, Union

from imgui_bundle import imgui


def get_id(id_: Optional[Union[str, int]] = None) -> int:
    if id_ is None:
        return 0
    elif isinstance(id_, str):
        return imgui.get_id(id_)
    elif isinstance(id_, int):
        return id_
    else:
        raise TypeError(f"Unsupported id type: '{type(id_).__name__}'")
