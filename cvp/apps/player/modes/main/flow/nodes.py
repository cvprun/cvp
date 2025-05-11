# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.apps.player.widgets.flows.selectable_node import selectable_node
from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.push_item_width import align_right_side_context
from cvp.imgui.text_centered import text_centered
from cvp.nodes.node import Node
from cvp.types.override import override


class NodeFlowWindow(BaseWindow):
    __cvp_window_name__ = "Node"
    __cvp_window_position__ = DockPosition.center_bottom

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def nodes(self):
        return self.context.flows.nodes

    @override
    def on_main_process(self) -> None:
        if dtype := self.nodes.get(self.selected_submenu):
            self.do_node_process(dtype)
        else:
            text_centered("Please select a item")

    @staticmethod
    def do_node_process(node: Node) -> None:
        input_text_disabled("Module Path", node.module_path)
        input_text_disabled("Class Name", node.class_name)
        imgui.input_text_multiline("Docs", node.docs)


class NodesFlowWindow(BaseWindow):
    __cvp_window_name__ = "Nodes"
    __cvp_window_position__ = DockPosition.left_bottom

    def __init__(self, context: Context):
        super().__init__(context)
        self._filter = str()

    def get_selected_node(self, *, suffix=None) -> str:
        return self._context.get_selected_submenu(NodeFlowWindow, suffix=suffix)

    def set_selected_node(self, value: str, *, suffix=None) -> None:
        self._context.set_selected_submenu(NodeFlowWindow, value, suffix=suffix)

    @override
    def on_main_process(self) -> None:
        with align_right_side_context():
            filter_result = imgui.input_text_with_hint(
                "###Filter",
                "Filter nodes ...",
                self._filter,
            )
            self._filter = filter_result[1]

        selected_node = self.get_selected_node()
        for node in self._context.flows.nodes.values():
            if self._filter and node.path.find(self._filter) == -1:
                continue

            selected = node.path == selected_node
            if selectable_node(node, selected=selected, use_drag_source=True):
                self.set_selected_node(node.path)
