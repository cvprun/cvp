# -*- coding: utf-8 -*-

from cvp.nodes.node import Node
from cvp.nodes.callable import CallableNode
from cvp.nodes.ntype import Ntype


def generate_node(ntype: Ntype) -> Node:
    if ntype.is_node_interface():
        return ntype.type()
    elif ntype.is_callable():
        return CallableNode(ntype.type)
    else:
        assert False, "Inaccessible section"
