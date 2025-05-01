# -*- coding: utf-8 -*-

from typing import Union

from cvp.apps.player.widgets.flows.drag_types import DragTypes
from cvp.imgui.drag_drop import accept_payload, begin_target, end_target
from cvp.imgui.flags.drag_drop import DragDropFlags


def accept_target(flags: Union[DragDropFlags, int] = 0):
    if isinstance(flags, DragDropFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if begin_target():
        try:
            if payload := accept_payload(DragTypes.flow_graph, flags):
                return payload
            if payload := accept_payload(DragTypes.flow_node, flags):
                return payload
            if payload := accept_payload(DragTypes.flow_dtype, flags):
                return payload
            if payload := accept_payload(DragTypes.flow_variable, flags):
                return payload
            return None
        finally:
            end_target()
