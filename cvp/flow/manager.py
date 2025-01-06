# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import PathLike
from typing import Optional, Union

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.flow.catalog import FlowCatalog
from cvp.flow.datas.chosen import SelectedItems
from cvp.flow.datas.graph import Graph
from cvp.flow.datas.node import Node
from cvp.flow.path import FlowPath
from cvp.resources.home import HomeDir
from cvp.strings.is_uuid import is_uuid4
from cvp.yaml.dumpers import IndentListDumper


class FlowManager(OrderedDict[str, Graph]):
    _clipboard: Optional[SelectedItems]

    def __init__(self, home: HomeDir, *, update=False):
        super().__init__()
        self._catalog = FlowCatalog.from_builtins()
        self._home = home
        self._clipboard = None
        if update:
            self.refresh_flow_graphs()

    @property
    def has_clipboard(self) -> bool:
        return self._clipboard is not None

    @property
    def clipboard(self):
        return self._clipboard

    def set_clipboard(self, items: SelectedItems) -> None:
        self._clipboard = items

    def clear_clipboard(self) -> None:
        self._clipboard = None

    def refresh_flow_graphs(self):
        for file in self._home.flows.find_graph_files():
            self.update_graph_yaml(file)

    @property
    def catalog(self):
        return self._catalog

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

    def get_node_template(self, path: Union[str, FlowPath]):
        return self._catalog.get_node_template(path)

    def add_node(self, graph: Graph, path: Union[str, FlowPath]) -> Node:
        node_template = self.get_node_template(path)
        node = Node.from_template(node_template)
        graph.nodes.append(node)
        return node
