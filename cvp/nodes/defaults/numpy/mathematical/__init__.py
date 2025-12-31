# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .absolute_node import AbsoluteNode
from .add_node import AddNode
from .arccos_node import ArccosNode
from .arccosh_node import ArccoshNode
from .arcsin_node import ArcsinNode
from .arcsinh_node import ArcsinhNode
from .arctan2_node import Arctan2Node
from .arctan_node import ArctanNode
from .arctanh_node import ArctanhNode
from .ceil_node import CeilNode
from .cos_node import CosNode
from .cosh_node import CoshNode
from .divide_node import DivideNode
from .exp2_node import Exp2Node
from .exp_node import ExpNode
from .expm1_node import Expm1Node
from .fabs_node import FabsNode
from .floor_divide_node import FloorDivideNode
from .floor_node import FloorNode
from .fmax_node import FmaxNode
from .fmin_node import FminNode
from .log1p_node import Log1pNode
from .log2_node import Log2Node
from .log10_node import Log10Node
from .log_node import LogNode
from .maximum_node import MaximumNode
from .minimum_node import MinimumNode
from .mod_node import ModNode
from .multiply_node import MultiplyNode
from .negative_node import NegativeNode
from .positive_node import PositiveNode
from .power_node import PowerNode
from .reciprocal_node import ReciprocalNode
from .remainder_node import RemainderNode
from .round_node import RoundNode
from .sign_node import SignNode
from .sin_node import SinNode
from .sinh_node import SinhNode
from .sqrt_node import SqrtNode
from .square_node import SquareNode
from .subtract_node import SubtractNode
from .tan_node import TanNode
from .tanh_node import TanhNode
from .true_divide_node import TrueDivideNode
from .trunc_node import TruncNode


def get_mathematical_nodes() -> List[Node]:
    """Get all mathematical nodes."""
    return [
        SinNode(),
        CosNode(),
        TanNode(),
        ArcsinNode(),
        ArccosNode(),
        ArctanNode(),
        Arctan2Node(),
        SinhNode(),
        CoshNode(),
        TanhNode(),
        ArcsinhNode(),
        ArccoshNode(),
        ArctanhNode(),
        ExpNode(),
        Exp2Node(),
        LogNode(),
        Log2Node(),
        Log10Node(),
        Log1pNode(),
        Expm1Node(),
        AddNode(),
        SubtractNode(),
        MultiplyNode(),
        DivideNode(),
        TrueDivideNode(),
        FloorDivideNode(),
        PowerNode(),
        ModNode(),
        RemainderNode(),
        RoundNode(),
        FloorNode(),
        CeilNode(),
        TruncNode(),
        SqrtNode(),
        SquareNode(),
        AbsoluteNode(),
        FabsNode(),
        SignNode(),
        NegativeNode(),
        PositiveNode(),
        ReciprocalNode(),
        MaximumNode(),
        MinimumNode(),
        FmaxNode(),
        FminNode(),
    ]
