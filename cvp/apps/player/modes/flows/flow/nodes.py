# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.flows.flow._base import BaseFlowWindow
from cvp.apps.player.windows.graph import FlowGraphWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.drag_types import DRAG_FLOW_NODE
from cvp.imgui.push_item_width import align_right_side
from cvp.types.override import override


class NodesFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Nodes"

    def __init__(self, context: Context):
        super().__init__(context)
        self._filter = str()

    @override
    def do_process(self, window: Optional[FlowGraphWindow]) -> None:
        with begin_context(self.get_window_name()):
            self.do_child_process()

    def do_child_process(self) -> None:
        with align_right_side():
            filter_result = imgui.input_text_with_hint(
                "###Filter",
                "Filter...",
                self._filter,
            )
            self._filter = filter_result[1]

        for node in self._context.flows.nodes.values():
            if self._filter and node.path.find(self._filter) == -1:
                continue

            imgui.selectable(node.path, p_selected=False)
            if imgui.begin_drag_drop_source():
                try:
                    data = node.path.encode()
                    imgui.set_drag_drop_payload(DRAG_FLOW_NODE, data, len(data))
                    imgui.text(node.path)
                finally:
                    imgui.end_drag_drop_source()
