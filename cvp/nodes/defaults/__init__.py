# -*- coding: utf-8 -*-

from types import MappingProxyType
from typing import List, Sequence

from cvp.nodes.defaults.builtins import get_builtin_nodes
from cvp.nodes.defaults.casting import get_casting_nodes
from cvp.nodes.defaults.essential import get_essential_nodes
from cvp.nodes.defaults.numpy import get_numpy_nodes
from cvp.nodes.defaults.opencv import get_opencv_nodes
from cvp.nodes.defaults.operators import get_operators_nodes
from cvp.nodes.defaults.pandas import get_pandas_nodes
from cvp.nodes.node import Node
from cvp.nodes.ntype import NodePath

NodeMapping = MappingProxyType[NodePath, Node]


def get_default_nodes() -> Sequence[Node]:
    result: List[Node] = list()
    result.extend(get_builtin_nodes())
    result.extend(get_casting_nodes())
    result.extend(get_essential_nodes())
    result.extend(get_operators_nodes())
    result.extend(get_numpy_nodes())
    result.extend(get_pandas_nodes())
    result.extend(get_opencv_nodes())
    return tuple(result)


def get_default_path2nodes() -> NodeMapping:
    return NodeMapping({node.path: node for node in get_default_nodes()})
