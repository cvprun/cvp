# -*- coding: utf-8 -*-

from collections import OrderedDict
from copy import deepcopy
from os import PathLike
from typing import Optional, Union

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.flow.runner import FlowRunner
from cvp.flow.selection import FlowSelection
from cvp.nodes.registry.registry import NodeRegistry
from cvp.resources.home import HomeDir
from cvp.strings.is_uuid import is_uuid4
from cvp.types.shapes import Point
from cvp.yaml.dumpers import IndentListDumper


class FlowManager:
    _graphs: OrderedDict[str, FlowGraph]
    _runners: OrderedDict[str, FlowRunner]

    _clipboard_items: Optional[FlowSelection]
    _clipboard_pivot: Optional[Point]

    def __init__(self, home: HomeDir, *, refresh_graphs=False):
        self._graphs = OrderedDict()
        self._runners = OrderedDict()
        self._dtype_registry = DtypeRegistry()
        self._node_registry = NodeRegistry(self._dtype_registry)

        self._home = home
        self._clipboard_items = None
        self._clipboard_pivot = None

        if refresh_graphs:
            self.refresh_flow_graphs()

    @property
    def graphs(self):
        return self._graphs

    @property
    def runners(self):
        return self._runners

    @property
    def dtype_registry(self):
        return self._dtype_registry

    @property
    def node_registry(self):
        return self._node_registry

    @property
    def dtypes(self):
        return self._dtype_registry.path2dtypes

    @property
    def nodes(self):
        return self._node_registry.nodes

    @property
    def has_clipboard(self) -> bool:
        return self._clipboard_items is not None

    @property
    def clipboard_items(self):
        return self._clipboard_items

    @clipboard_items.setter
    def clipboard_items(self, value: FlowSelection) -> None:
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
    ) -> FlowGraph:
        template = template if template else str()
        assert isinstance(template, str)
        graph = FlowGraph(name=name)
        assert is_uuid4(graph.uuid)

        if append:
            assert graph.uuid
            assert graph.uuid not in self._graphs
            self._graphs[graph.uuid] = graph

        return graph

    def remove_graph(self, uuid: str) -> FlowGraph:
        if uuid in self._graphs:
            raise KeyError(f"Not exists flow graph: '{uuid}'")
        return self._graphs.pop(uuid)

    @staticmethod
    def dumps_graph_yaml(graph: FlowGraph, encoding="utf-8") -> bytes:
        return dump(serialize(graph), Dumper=IndentListDumper).encode(encoding)

    @staticmethod
    def write_graph_yaml(
        filepath: Union[str, PathLike[str]],
        graph: FlowGraph,
        encoding="utf-8",
    ) -> None:
        with open(filepath, "wb") as f:
            f.write(FlowManager.dumps_graph_yaml(graph, encoding=encoding))

    def loads_graph_yaml(self, data: bytes) -> FlowGraph:
        result = deserialize(full_load(data), FlowGraph)
        assert isinstance(result, FlowGraph)
        for node in result.nodes:
            assert node.template is None
            node.template = self._node_registry.nodes[node.path]
        result.update_arcs_io(force=True)
        return result

    def read_graph_yaml(self, filepath: Union[str, PathLike[str]]) -> FlowGraph:
        with open(filepath, "rb") as f:
            return self.loads_graph_yaml(f.read())

    def update_graph_yaml(self, filepath: Union[str, PathLike[str]]) -> None:
        graph = self.read_graph_yaml(filepath)
        if not graph.uuid:
            raise ValueError("The 'uuid' of the flow graph does not exist")
        self._graphs[graph.uuid] = graph

    def add_node(self, graph: FlowGraph, path: str) -> FlowNode:
        node_template = self._node_registry.nodes[path]
        node = FlowNode.from_template(node_template)
        graph.nodes.insert(0, node)
        return node

    def add_setter_node(self, graph: FlowGraph, key: str) -> FlowNode:
        variable = graph.find_variable(key)
        if variable is None:
            raise KeyError(f"Not found variable: '{key}'")

        dtype = deepcopy(variable.dtype)
        node_template = self._node_registry.create_setter_node(key, dtype)
        node = FlowNode.from_template(node_template)
        graph.nodes.insert(0, node)
        return node

    def add_getter_node(self, graph: FlowGraph, key: str) -> FlowNode:
        variable = graph.find_variable(key)
        if variable is None:
            raise KeyError(f"Not found variable: '{key}'")

        dtype = deepcopy(variable.dtype)
        node_template = self._node_registry.create_getter_node(key, dtype)
        node = FlowNode.from_template(node_template)
        graph.nodes.insert(0, node)
        return node
