# -*- coding: utf-8 -*-

from typing import Dict, TypeAlias, Union

from cvp.flow.catalog.builtin import builtin_templates
from cvp.flow.catalog.registry import global_registry
from cvp.flow.datas.templates.node import NodeTemplate
from cvp.flow.path import FlowPath

ModulePath: TypeAlias = str
NodeName: TypeAlias = str
ModuleToNodes: TypeAlias = Dict[ModulePath, Dict[NodeName, NodeTemplate]]


class FlowCatalog:
    _nodes: Dict[FlowPath, NodeTemplate]

    def __init__(self, *, no_builtins=False, no_global_register=False):
        self._nodes = dict()
        if not no_builtins:
            self._nodes.update(builtin_templates())
        if not no_global_register:
            self._nodes.update(global_registry())

    @staticmethod
    def normalize_path(path: Union[str, FlowPath]) -> FlowPath:
        if isinstance(path, FlowPath):
            return path
        if isinstance(path, str):
            return FlowPath(path)
        raise TypeError(f"Unsupported path type: {type(path).__name__}")

    def __getitem__(self, path: Union[str, FlowPath]) -> NodeTemplate:
        return self._nodes.__getitem__(self.normalize_path(path))

    def __setitem__(self, path: Union[str, FlowPath], value: NodeTemplate) -> None:
        self._nodes.__setitem__(self.normalize_path(path), value)

    def __contains__(self, path: Union[str, FlowPath]) -> bool:
        return self._nodes.__contains__(self.normalize_path(path))

    def __len__(self) -> int:
        return self._nodes.__len__()

    def __bool__(self) -> bool:
        return bool(self._nodes)

    def keys(self):
        return self._nodes.keys()

    def values(self):
        return self._nodes.values()

    def items(self):
        return self._nodes.items()

    def as_module2nodes(self) -> ModuleToNodes:
        result: ModuleToNodes = dict()
        for path, node in self._nodes.items():
            module_path, node_name = path.split()
            assert isinstance(module_path, str)
            assert isinstance(node_name, str)
            if module_path not in result:
                result[module_path] = dict()
            nodes = result.get(module_path)
            if nodes is None:
                nodes = dict()
                result[module_path] = nodes
            assert isinstance(nodes, dict)
            nodes[node_name] = node
        return result
