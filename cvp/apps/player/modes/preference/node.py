# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.text_centered import text_centered
from cvp.nodes.node import Node
from cvp.types.override import override
from cvp.variables import SIDE_MENU_WIDTH


class NodePreference(BasePreference):
    __cvp_menu_name__ = "Node"

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def nodes(self):
        return self.context.fm.nodes

    @override
    def do_process(self) -> None:
        child_flags = RESIZE_X | BORDERS
        with begin_child_context("Menu", SIDE_MENU_WIDTH, child_flags=child_flags):
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for path, node in self.nodes.items():
                        label = f"{node.class_name}###{path}"
                        selected = path == self.selected
                        if imgui.selectable(label, selected)[1]:
                            self.selected = path
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if node := self.nodes.get(self.selected):
                self.do_node_process(node)
            else:
                text_centered("Please select a item")

    @staticmethod
    def do_node_process(node: Node) -> None:
        input_text_disabled("Class Name", node.class_name)
        input_text_disabled("Path", node.path)
