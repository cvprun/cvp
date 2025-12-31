# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .arange_node import ArangeNode
from .array_node import ArrayNode
from .empty_node import EmptyNode
from .eye_node import EyeNode
from .full_node import FullNode
from .identity_node import IdentityNode
from .linspace_node import LinspaceNode
from .logspace_node import LogspaceNode
from .ones_node import OnesNode
from .zeros_node import ZerosNode


def get_array_creation_nodes() -> List[Node]:
    """Get all array_creation nodes."""
    return [
        ArrayNode(),
        ZerosNode(),
        OnesNode(),
        EmptyNode(),
        EyeNode(),
        IdentityNode(),
        ArangeNode(),
        LinspaceNode(),
        LogspaceNode(),
        FullNode(),
    ]
