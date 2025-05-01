# -*- coding: utf-8 -*-

from collections import OrderedDict
from concurrent.futures import Executor
from copy import deepcopy
from typing import Any, Optional, Union
from uuid import uuid4

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
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.flows import FlowsPath
from cvp.strings.is_uuid import is_uuid4
from cvp.types.shapes import Point


class FlowManager:
    _dtype_registry: DtypeRegistry
    _node_registry: NodeRegistry

    _graphs: ResourceManager[GraphKey, FlowGraph]
    _runners: OrderedDict[str, FlowRunner]

    _focused_key: Optional[GraphKey]
    _clipboard_items: Optional[FlowSelection]
    _clipboard_pivot: Optional[Point]

    def __init__(
        self,
        path: FlowsPath,
        *,
        no_dtype_defaults=False,
        no_node_defaults=False,
        reload=False,
        raise_errors=False,
    ):
        self._path = path

        self._dtype_registry = DtypeRegistry(no_defaults=no_dtype_defaults)
        self._node_registry = NodeRegistry(no_defaults=no_node_defaults)

        self._graphs = ResourceManager(
            key_type=GraphKey,
            config_type=FlowGraph,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._runners = OrderedDict()

        self._focused_key = None
        self._clipboard_items = None
        self._clipboard_pivot = None

        if reload:
            self.read_all_graph_files(raise_errors=raise_errors)

    def stop_all_runners(self) -> None:
        for runner in self._runners.values():
            runner.stop()

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
    def graphs(self):
        return self._graphs

    @property
    def runners(self):
        return self._runners

    @property
    def focused_key(self):
        return self._focused_key

    @focused_key.setter
    def focused_key(self, value: GraphKey) -> None:
        self._focused_key = value

    @property
    def focused_graph(self) -> Optional[FlowGraph]:
        if self._focused_key is None:
            return None
        return self._graphs.get(self._focused_key)

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

    def create_graph(
        self,
        name: Optional[str] = None,
        *,
        key: Optional[GraphKey] = None,
        append=False,
        opened=False,
    ) -> FlowGraph:
        graph_key = key if key else GraphKey(str(uuid4()))
        graph_name = GraphName(name) if name else None
        graph = FlowGraph(key=graph_key, name=graph_name, opened=opened)
        assert is_uuid4(graph.key)

        if append:
            assert graph.key
            assert graph.key not in self._graphs
            self._graphs.add(graph_key, graph)

        return graph

    def write_graph_file(self, graph: FlowGraph) -> int:
        return self._graphs.write_serialized_config_file(graph.key, graph)

    def write_all_graph_file(self, *, raise_errors=False) -> None:
        return self._graphs.write_all_config_files(raise_errors=raise_errors)

    def list_graph_filenames(self):
        return self._graphs.list_config_filenames()

    def list_graph_keys(self):
        return self._graphs.list_config_filekeys()

    def read_all_graph_files(self, *, raise_errors=False):
        self._graphs.read_all_config_files(raise_errors=raise_errors)

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
