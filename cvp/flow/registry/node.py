# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Dict

from cvp.flow.templates.node import NodeTemplate
from cvp.patterns.singleton import singleton


class FlowNodeRegistry(Dict[str, NodeTemplate]):
    def register_node_template(self):
        pass

    def register_node(self):
        pass

    def register_callable(self):
        pass

    def register_function(self):
        pass


@singleton
class GlobalFlowNodeRegistry(FlowNodeRegistry):
    pass


@lru_cache
def global_node_registry() -> GlobalFlowNodeRegistry:
    return GlobalFlowNodeRegistry()


def register_node():
    pass
