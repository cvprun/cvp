# -*- coding: utf-8 -*-

from typing import Optional

from cvp.dtypes.icons import DTYPE_ICON_MAPPING
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.variables import FLOW_PATH_SEPARATOR


def default_dtype_name_with_type(base: type) -> str:
    return base.__name__


def default_dtype_path_with_type(base: type, name: Optional[str] = None) -> str:
    return base.__module__ + FLOW_PATH_SEPARATOR + (name if name else base.__name__)


def default_dtype_docs_with_type(base: type) -> str:
    return base.__doc__ if base.__doc__ else str()


def default_dtype_icon_with_type(base: type, name: Optional[str] = None) -> str:
    return DTYPE_ICON_MAPPING[(name if name else base.__name__)[0]]


class Dtype:
    def __init__(
        self,
        base: type,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ):
        if not isinstance(base, type):
            raise TypeError(f"Only types can be registered: {base}")

        self.base = base
        self.name = name if name else default_dtype_name_with_type(base)
        self.path = path if path else default_dtype_path_with_type(base, self.name)
        self.docs = docs if docs else default_dtype_docs_with_type(base)
        self.icon = icon if icon else default_dtype_icon_with_type(base, self.name)
        self.color = color if color else WHITE_RGBA

        if not self.name:
            raise ValueError("The 'name' attribute is required")
        if not self.path:
            raise ValueError("The 'path' attribute is required")
