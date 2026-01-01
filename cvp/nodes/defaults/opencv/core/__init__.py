# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .absdiff_node import AbsdiffNode
from .add_node import AddNode
from .add_weighted_node import AddWeightedNode
from .bitwise_and_node import BitwiseAndNode
from .bitwise_not_node import BitwiseNotNode
from .bitwise_or_node import BitwiseOrNode
from .bitwise_xor_node import BitwiseXorNode
from .convertscaleabs_node import ConvertScaleAbsNode
from .copyto_node import CopyToNode
from .divide_node import DivideNode
from .flip_node import FlipNode
from .hconcat_node import HConcatNode
from .inrange_node import InRangeNode
from .merge_node import MergeNode
from .multiply_node import MultiplyNode
from .norm_node import NormNode
from .split_node import SplitNode
from .subtract_node import SubtractNode
from .transpose_node import TransposeNode
from .vconcat_node import VConcatNode


def get_core_nodes() -> List[Node]:
    """Get all core OpenCV nodes."""
    return [
        AbsdiffNode(),
        AddNode(),
        AddWeightedNode(),
        BitwiseAndNode(),
        BitwiseNotNode(),
        BitwiseOrNode(),
        BitwiseXorNode(),
        ConvertScaleAbsNode(),
        CopyToNode(),
        DivideNode(),
        FlipNode(),
        HConcatNode(),
        InRangeNode(),
        MergeNode(),
        MultiplyNode(),
        NormNode(),
        SplitNode(),
        SubtractNode(),
        TransposeNode(),
        VConcatNode(),
    ]
