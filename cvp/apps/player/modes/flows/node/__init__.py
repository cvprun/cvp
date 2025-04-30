# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.text_centered import text_centered
from cvp.nodes.node import Node
from cvp.types.override import override


class NodeMode(BaseMode):
    __cvp_mode_name__ = "Node"

    _MENU_SPLIT_X: Final[int] = 150
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def nodes(self):
        return self.context.flows.nodes

    @override
    def do_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context(
                label="Menu",
                size=(self._MENU_SPLIT_X, 0),
                child_flags=self._MENU_CHILD_FLAGS,
            ):
                if imgui.begin_list_box("##List", FIT_SIZE):
                    try:
                        for path, node in self.nodes.items():
                            label = f"{node.class_name}###{path}"
                            selected = path == self.selected_submenu
                            if imgui.selectable(label, selected)[1]:
                                self.selected_submenu = path
                    finally:
                        imgui.end_list_box()

            imgui.same_line()

            with begin_child_context("Main"):
                if node := self.nodes.get(self.selected_submenu):
                    self.do_node_process(node)
                else:
                    text_centered("Please select a item")

    @staticmethod
    def do_node_process(node: Node) -> None:
        input_text_disabled("Class Name", node.class_name)
        input_text_disabled("Path", node.path)
