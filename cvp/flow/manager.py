# -*- coding: utf-8 -*-

from collections import OrderedDict
from concurrent.futures import Executor
from copy import deepcopy
from os import PathLike
from typing import Any, Optional, Union

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.dtypes.dtype import Dtype
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.flow.graph import FlowGraph, GraphKey, GraphName
from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin
from cvp.flow.runner import FlowRunner
from cvp.flow.selection import FlowSelection
from cvp.flow.variable import FlowVariable
from cvp.flow.wire import FlowWire
from cvp.nodes.node import Node
from cvp.nodes.registry.registry import NodeRegistry
from cvp.resources.subdirs.flows import FlowsPath
from cvp.strings.is_uuid import is_uuid4
from cvp.types.shapes import Point
from cvp.yaml.dumpers import IndentListDumper


class FlowManager:
    _graphs: OrderedDict[GraphKey, FlowGraph]
    _runners: OrderedDict[str, FlowRunner]

    _clipboard_items: Optional[FlowSelection]
    _clipboard_pivot: Optional[Point]

    def __init__(self, path: FlowsPath, *, refresh_graphs=False):
        self._dtype_registry = DtypeRegistry()
        self._node_registry = NodeRegistry()

        self._graphs = OrderedDict()
        self._runners = OrderedDict()

        self._path = path
        self._clipboard_items = None
        self._clipboard_pivot = None

        if refresh_graphs:
            self.refresh_flow_graphs()

    def stop_all_runners(self) -> None:
        for runner in self._runners.values():
            runner.stop()

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
        for file in self._path.find_graph_files():
            self.update_graph_yaml(file)

    def create_graph(
        self,
        name: Optional[str] = None,
        *,
        template: Optional[str] = None,
        append=False,
    ) -> FlowGraph:
        template = template if template else str()
        assert isinstance(template, str)

        graph = FlowGraph(key=None, name=GraphName(name) if name else None)
        assert is_uuid4(graph.key)

        if append:
            assert graph.key
            assert graph.key not in self._graphs
            self._graphs[graph.key] = graph

        return graph

    def remove_graph(self, uuid: GraphKey) -> FlowGraph:
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

    @staticmethod
    def loads_graph_yaml(data: bytes) -> FlowGraph:
        result = deserialize(full_load(data), FlowGraph)
        result.update_wires_io(force=True)
        return result

    def read_graph_yaml(self, filepath: Union[str, PathLike[str]]) -> FlowGraph:
        with open(filepath, "rb") as f:
            return self.loads_graph_yaml(f.read())

    def update_graph_yaml(self, filepath: Union[str, PathLike[str]]) -> None:
        graph = self.read_graph_yaml(filepath)
        if not graph.key:
            raise ValueError("The 'uuid' of the flow graph does not exist")
        self._graphs[graph.key] = graph

    def add_node(self, graph: FlowGraph, node: Union[str, Node]) -> FlowNode:
        node_template = self._node_registry[node]
        flow_node = FlowNode.from_template(node_template)
        graph.nodes.insert(0, flow_node)
        return flow_node

    def add_variable(
        self,
        graph: FlowGraph,
        variable_name: str,
        dtype: Any,
    ) -> FlowVariable:
        if not isinstance(dtype, Dtype):
            dtype = self._dtype_registry[dtype]
        assert isinstance(dtype, Dtype)
        return graph.add_variable(variable_name, dtype)

    @staticmethod
    def _find_variable(graph: FlowGraph, key: Union[str, FlowVariable]) -> FlowVariable:
        if isinstance(key, FlowVariable):
            return key
        assert isinstance(key, str)
        variable = graph.find_variable(key)
        if variable is None:
            raise KeyError(f"Not found variable: '{key}'")
        return variable

    def add_setter_node(
        self,
        graph: FlowGraph,
        key: Union[str, FlowVariable],
    ) -> FlowNode:
        variable = self._find_variable(graph, key)
        dtype = deepcopy(variable.dtype)
        setter_node = self._node_registry.setter_node
        node = FlowNode.from_template(setter_node)
        node.name = f"({dtype.class_name}) {key}"
        node.set_default(setter_node.key_name, variable.name)
        node.set_dtype(setter_node.value_name, dtype)
        graph.nodes.insert(0, node)
        return node

    def add_getter_node(
        self,
        graph: FlowGraph,
        key: Union[str, FlowVariable],
    ) -> FlowNode:
        variable = self._find_variable(graph, key)
        dtype = deepcopy(variable.dtype)
        getter_node = self._node_registry.getter_node
        node = FlowNode.from_template(getter_node)
        node.name = f"({dtype.class_name}) {key}"
        node.set_default(getter_node.key_name, variable.name)
        node.set_dtype(getter_node.value_name, dtype)
        graph.nodes.insert(0, node)
        return node

    @staticmethod
    def add_wire(
        graph: FlowGraph,
        output_node: Union[FlowNode, str],
        output_pin: Union[FlowPin, str],
        input_node: Union[FlowNode, str],
        input_pin: Union[FlowPin, str],
    ) -> FlowWire:
        out_conn = graph.create_node_pin(output_node, output_pin)
        in_conn = graph.create_node_pin(input_node, input_pin)
        return graph.connect_pins(out_conn, in_conn)

    def add_runner(
        self,
        graph: FlowGraph,
        start_node: Union[FlowNode, str],
        executor: Executor,
        *,
        name: Optional[str] = None,
        debug=False,
        verbose=0,
    ):
        runner = FlowRunner(
            executor=executor,
            graph=graph,
            start_node=start_node,
            use_copy=False,
            use_deepcopy=False,
            debug=debug,
            verbose=verbose,
        )
        self._runners[name if name else graph.key] = runner
        return runner
