# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .concatenate_node import ConcatenateNode
from .dsplit_node import DsplitNode
from .dstack_node import DstackNode
from .expand_dims_node import ExpandDimsNode
from .flatten_node import FlattenNode
from .flip_node import FlipNode
from .fliplr_node import FliplrNode
from .flipud_node import FlipudNode
from .hsplit_node import HsplitNode
from .hstack_node import HstackNode
from .moveaxis_node import MoveaxisNode
from .ravel_node import RavelNode
from .repeat_node import RepeatNode
from .reshape_node import ReshapeNode
from .split_node import SplitNode
from .squeeze_node import SqueezeNode
from .stack_node import StackNode
from .swapaxes_node import SwapaxesNode
from .tile_node import TileNode
from .transpose_node import TransposeNode
from .vsplit_node import VsplitNode
from .vstack_node import VstackNode


def get_array_manipulation_nodes() -> List[Node]:
    """Get all array_manipulation nodes."""
    return [
        ReshapeNode(),
        TransposeNode(),
        SwapaxesNode(),
        MoveaxisNode(),
        FlipNode(),
        FliplrNode(),
        FlipudNode(),
        SqueezeNode(),
        ExpandDimsNode(),
        ConcatenateNode(),
        StackNode(),
        HstackNode(),
        VstackNode(),
        DstackNode(),
        SplitNode(),
        HsplitNode(),
        VsplitNode(),
        DsplitNode(),
        TileNode(),
        RepeatNode(),
        FlattenNode(),
        RavelNode(),
    ]
