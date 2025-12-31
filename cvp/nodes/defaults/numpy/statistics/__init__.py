# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .argmax_node import ArgmaxNode
from .argmin_node import ArgminNode
from .argsort_node import ArgsortNode
from .bincount_node import BincountNode
from .corrcoef_node import CorrcoefNode
from .cov_node import CovNode
from .cumprod_node import CumprodNode
from .cumsum_node import CumsumNode
from .histogram_node import HistogramNode
from .max_node import MaxNode
from .mean_node import MeanNode
from .median_node import MedianNode
from .min_node import MinNode
from .percentile_node import PercentileNode
from .prod_node import ProdNode
from .ptp_node import PtpNode
from .quantile_node import QuantileNode
from .sort_node import SortNode
from .std_node import StdNode
from .sum_node import SumNode
from .var_node import VarNode


def get_statistics_nodes() -> List[Node]:
    """Get all statistics nodes."""
    return [
        MeanNode(),
        MedianNode(),
        StdNode(),
        VarNode(),
        MinNode(),
        MaxNode(),
        PtpNode(),
        PercentileNode(),
        QuantileNode(),
        SumNode(),
        ProdNode(),
        CumsumNode(),
        CumprodNode(),
        ArgminNode(),
        ArgmaxNode(),
        ArgsortNode(),
        SortNode(),
        HistogramNode(),
        BincountNode(),
        CorrcoefNode(),
        CovNode(),
    ]
