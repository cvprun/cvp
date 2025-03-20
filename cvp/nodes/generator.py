# -*- coding: utf-8 -*-

from cvp.nodes.callable import CallableNode
from cvp.nodes.interface import NodeInterface
from cvp.nodes.node import Node
from cvp.nodes.ntype import Ntype


def generate_node(ntype: Ntype) -> Node:
    if ntype.is_node_interface():
        assert isinstance(ntype.type, type)
        assert issubclass(ntype.type, NodeInterface)
        assert issubclass(ntype.type, Node)
        assert not issubclass(ntype.type, CallableNode)
        return ntype.type()
    elif ntype.is_callable():
        assert callable(ntype.type)
        return CallableNode(ntype.type)
    else:
        assert False, "Inaccessible section"
