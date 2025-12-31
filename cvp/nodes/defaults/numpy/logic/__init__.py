# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .all_node import AllNode
from .any_node import AnyNode
from .argwhere_node import ArgwhereNode
from .equal_node import EqualNode
from .flatnonzero_node import FlatnonzeroNode
from .greater_equal_node import GreaterEqualNode
from .greater_node import GreaterNode
from .iscomplex_node import IscomplexNode
from .iscomplexobj_node import IscomplexobjNode
from .isfinite_node import IsfiniteNode
from .isinfinite_node import IsinfiniteNode
from .isnan_node import IsnanNode
from .isnat_node import IsnatNode
from .isneginfinite_node import IsneginfiniteNode
from .isposinfinite_node import IsposinfiniteNode
from .isreal_node import IsrealNode
from .isrealobj_node import IsrealobjNode
from .isscalar_node import IsscalarNode
from .less_equal_node import LessEqualNode
from .less_node import LessNode
from .logical_and_node import LogicalAndNode
from .logical_not_node import LogicalNotNode
from .logical_or_node import LogicalOrNode
from .logical_xor_node import LogicalXorNode
from .nonzero_node import NonzeroNode
from .not_equal_node import NotEqualNode
from .select_node import SelectNode
from .where_node import WhereNode


def get_logic_nodes() -> List[Node]:
    """Get all logic nodes."""
    return [
        AllNode(),
        AnyNode(),
        IsfiniteNode(),
        IsinfiniteNode(),
        IsnanNode(),
        IsnatNode(),
        IsneginfiniteNode(),
        IsposinfiniteNode(),
        LogicalAndNode(),
        LogicalOrNode(),
        LogicalNotNode(),
        LogicalXorNode(),
        GreaterNode(),
        GreaterEqualNode(),
        LessNode(),
        LessEqualNode(),
        EqualNode(),
        NotEqualNode(),
        WhereNode(),
        SelectNode(),
        NonzeroNode(),
        FlatnonzeroNode(),
        ArgwhereNode(),
        IscomplexNode(),
        IscomplexobjNode(),
        IsrealNode(),
        IsrealobjNode(),
        IsscalarNode(),
    ]
