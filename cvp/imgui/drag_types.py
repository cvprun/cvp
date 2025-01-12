# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final


@unique
class DragTypes(StrEnum):
    flow_graph = auto()
    flow_node = auto()
    flow_dtype = auto()


DRAG_FLOW_GRAPH: Final[str] = str(DragTypes.flow_graph)
DRAG_FLOW_NODE: Final[str] = str(DragTypes.flow_node)
DRAG_FLOW_DTYPE: Final[str] = str(DragTypes.flow_dtype)
