# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Dict, Optional

from cvp.flow.styles.dtype import DTYPE_ICON_MAPPING
from cvp.flow.templates.dtype import Dtype
from cvp.patterns.singleton import singleton
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.variables import FLOW_PATH_SEPARATOR


class FlowDtypeRegistry(Dict[str, Dtype]):
    def register(
        self,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ):
        def _decorator(base):
            if not isinstance(base, type):
                raise TypeError(f"Only types can be registered: {base}")

            b_name = name if name else base.__name__
            b_path = path if path else base.__module__ + FLOW_PATH_SEPARATOR + b_name
            b_docs = docs if docs else base.__doc__
            b_icon = icon if icon else DTYPE_ICON_MAPPING[b_name[0]]
            b_color = color if color else WHITE_RGBA

            if self.__contains__(b_path):
                raise KeyError(f"Duplicate dtype key: {b_path}")

            dtype = Dtype(
                name=b_name,
                path=b_path,
                base=base,
                docs=b_docs,
                icon=b_icon,
                color=b_color,
            )

            self.__setitem__(b_path, dtype)

        return _decorator


@singleton
class GlobalFlowDtypeRegistry(FlowDtypeRegistry):
    pass


@lru_cache
def global_dtype_registry() -> GlobalFlowDtypeRegistry:
    return GlobalFlowDtypeRegistry()


def register_dtype(
    name: Optional[str] = None,
    path: Optional[str] = None,
    docs: Optional[str] = None,
    icon: Optional[str] = None,
    color: Optional[RGBA] = None,
):
    return global_dtype_registry().register(
        name=name,
        path=path,
        docs=docs,
        icon=icon,
        color=color,
    )
