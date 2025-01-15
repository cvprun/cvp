# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import PathLike
from typing import Optional, Union

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.flow.components.graph import Graph
from cvp.flow.components.node import Node
from cvp.flow.components.selection import Selection
from cvp.flow.registry.globals import global_registry
from cvp.flow.registry.registry import FlowRegistry
from cvp.resources.home import HomeDir
from cvp.strings.is_uuid import is_uuid4
from cvp.types.shapes import Point
from cvp.yaml.dumpers import IndentListDumper


class FlowManager(OrderedDict[str, Graph]):
    _clipboard_items: Optional[Selection]
    _clipboard_pivot: Optional[Point]

    def __init__(self, home: HomeDir, *, refresh_graphs=False, no_globals=False):
        super().__init__()
        self._registry = FlowRegistry()

        if not no_globals:
            self._registry.update(global_registry())

        self._home = home
        self._clipboard_items = None
        self._clipboard_pivot = None

        if refresh_graphs:
            self.refresh_flow_graphs()

    @property
    def dtypes(self):
        return self._registry.path2dtypes

    @property
    def nodes(self):
        return self._registry.nodes

    @property
    def has_clipboard(self) -> bool:
        return self._clipboard_items is not None

    @property
    def clipboard_items(self):
        return self._clipboard_items

    @clipboard_items.setter
    def clipboard_items(self, value: Selection) -> None:
        self._clipboard_items = value

    @property
    def clipboard_pivot(self):
        return self._clipboard_pivot

    @clipboard_pivot.setter
    def clipboard_pivot(self, value: Point) -> None:
        self._clipboard_pivot = value

    def clear_clipboard(self) -> None:
        self._clipboard_items = None
        self._clipboard_pivot = None

    def refresh_flow_graphs(self):
        for file in self._home.flows.find_graph_files():
            self.update_graph_yaml(file)

    def create_graph(
        self,
        name: str,
        *,
        template: Optional[str] = None,
        append=False,
    ) -> Graph:
        template = template if template else str()
        assert isinstance(template, str)
        graph = Graph(name=name)
        assert is_uuid4(graph.uuid)

        if append:
            assert graph.uuid
            assert graph.uuid not in self
            self[graph.uuid] = graph

        return graph

    def remove_graph(self, uuid: str) -> Graph:
        if uuid in self:
            raise KeyError(f"Not exists flow graph: '{uuid}'")
        return self.pop(uuid)

    @staticmethod
    def dumps_graph_yaml(graph: Graph, encoding="utf-8") -> bytes:
        return dump(serialize(graph), Dumper=IndentListDumper).encode(encoding)

    @staticmethod
    def loads_graph_yaml(data: bytes) -> Graph:
        result = deserialize(full_load(data), Graph)
        assert isinstance(result, Graph)
        return result

    @staticmethod
    def write_graph_yaml(
        filepath: Union[str, PathLike[str]],
        graph: Graph,
        encoding="utf-8",
    ) -> None:
        with open(filepath, "wb") as f:
            f.write(FlowManager.dumps_graph_yaml(graph, encoding=encoding))

    @staticmethod
    def read_graph_yaml(filepath: Union[str, PathLike[str]]) -> Graph:
        with open(filepath, "rb") as f:
            return FlowManager.loads_graph_yaml(f.read())

    def update_graph_yaml(self, filepath: Union[str, PathLike[str]]) -> None:
        graph = self.read_graph_yaml(filepath)
        if not graph.uuid:
            raise ValueError("The 'uuid' of the flow graph does not exist")
        self[graph.uuid] = graph

    def get_node_template(self, path: str):
        return self.nodes[path]

    def add_node(self, graph: Graph, path: str) -> Node:
        node_template = self.get_node_template(path)
        node = Node.from_template(node_template)
        graph.nodes.insert(0, node)
        return node
