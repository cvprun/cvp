# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.path import FlowPath
from cvp.imgui.drag_types import DRAG_FLOW_GRAPH_TYPE as DRAG_GRAPH
from cvp.imgui.drag_types import DRAG_FLOW_NODE_TYPE as DRAG_NODE
from cvp.imgui.indent import indent
from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.override import override


class Catalogs(WidgetInterface):
    def __init__(self, context: Context):
        self._context = context
        self._catalog = self._context.fm.catalog

    @override
    def on_process(self) -> None:
        imgui.text("Catalogs:")

        if self._context.fm:
            expanded, visible = imgui.collapsing_header("graphs")
            if imgui.is_item_hovered():
                with imgui.begin_tooltip():
                    imgui.text("List of saved graphs")

            if expanded:
                with indent(imgui.get_tree_node_to_label_spacing()):
                    for uuid, graph in self._context.fm.items():
                        imgui.selectable(f"{graph.name}##{graph.uuid}")

                        # if not self._context.fm.opened:
                        #     continue

                        with imgui.begin_drag_drop_source() as drag_drop_src:
                            if drag_drop_src.dragging:
                                graph_uuid = graph.uuid.encode()

                                imgui.set_drag_drop_payload(DRAG_GRAPH, graph_uuid)
                                imgui.text(graph.name)

        for module_path, nodes in self._context.fm.catalog.as_module2nodes().items():
            imgui.push_id(module_path)
            try:
                expanded, visible = imgui.collapsing_header(module_path)
                if imgui.is_item_hovered():
                    with imgui.begin_tooltip():
                        imgui.text(module_path)

                if expanded:
                    with indent(imgui.get_tree_node_to_label_spacing()):
                        for node_name, node_template in nodes.items():
                            imgui.selectable(node_name)

                            with imgui.begin_drag_drop_source() as drag_drop_src:
                                if drag_drop_src.dragging:
                                    node_name = node_template.name
                                    node_path = node_template.path

                                    flow_path = FlowPath(node_path).join(node_name)
                                    node_data = bytes(flow_path)

                                    imgui.set_drag_drop_payload(DRAG_NODE, node_data)
                                    imgui.text(node_name)
            finally:
                imgui.pop_id()
