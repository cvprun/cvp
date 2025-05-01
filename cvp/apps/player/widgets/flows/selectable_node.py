# -*- coding: utf-8 -*-

from typing import Optional, Union

from imgui_bundle import imgui

from cvp.apps.player.widgets.flows.drag_types import DRAG_FLOW_NODE
from cvp.imgui.drag_drop import begin_source, end_source, set_payload
from cvp.imgui.flags.cond import Cond
from cvp.imgui.flags.selectable import SelectableFlags
from cvp.imgui.selectable import selectable
from cvp.nodes.node import Node


def drag_node_source(node: Node, cond: Union[Cond, int] = 0):
    if begin_source():
        try:
            set_payload(DRAG_FLOW_NODE, node.path, cond)
            imgui.text(node.path)
        finally:
            end_source()


def selectable_node(
    node: Node,
    selected=False,
    flags: Union[SelectableFlags, int] = 0,
    size: Optional[imgui.ImVec2Like] = None,
    *,
    use_drag_source=False,
    drag_cond: Union[Cond, int] = 0,
):
    result = selectable(node.path, selected, flags, size)
    if use_drag_source:
        drag_node_source(node, drag_cond)
    return result
