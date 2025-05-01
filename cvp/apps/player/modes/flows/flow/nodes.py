# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.flows.flow._base import BaseFlowWindow
from cvp.apps.player.widgets.flows.selectable_node import selectable_node
from cvp.apps.player.windows.graph import FlowGraphWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.push_item_width import align_right_side_context
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
        with align_right_side_context():
            filter_result = imgui.input_text_with_hint(
                "###Filter",
                "Filter nodes ...",
                self._filter,
            )
            self._filter = filter_result[1]

        for node in self._context.flows.nodes.values():
            if self._filter and node.path.find(self._filter) == -1:
                continue
            selectable_node(node, use_drag_source=True)
