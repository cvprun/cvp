# -*- coding: utf-8 -*-

from typing import Dict, TypeAlias

from cvp.flow.catalog.builtin import builtin_templates
from cvp.flow.catalog.registry import global_node_registry
from cvp.flow.datas.templates.node import NodeTemplate


class FlowCatalog:
    _nodes: Dict[str, NodeTemplate]

    def __init__(self, *, no_builtins=False, no_global_register=False):
        self._nodes = dict()
        if not no_builtins:
            self._nodes.update(builtin_templates())
        if not no_global_register:
            self._nodes.update(global_node_registry())

    def __getitem__(self, path: str) -> NodeTemplate:
        return self._nodes.__getitem__(path)

    def __setitem__(self, path: str, value: NodeTemplate) -> None:
        self._nodes.__setitem__(path, value)

    def __contains__(self, path: str) -> bool:
        return self._nodes.__contains__(path)

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
