# -*- coding: utf-8 -*-

from ctypes import CDLL, c_void_p, cast
from functools import lru_cache
from typing import Optional

from OpenGL import platform


@lru_cache
def get_opengl_dll() -> CDLL:
    # noinspection PyUnresolvedReferences
    return platform.PLATFORM.OpenGL


def get_opengl_process_address(name: str) -> Optional[int]:
    func = getattr(get_opengl_dll(), name, None)
    if func is not None:
        return cast(func, c_void_p).value
    else:
        return None
