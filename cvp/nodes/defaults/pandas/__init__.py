# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.defaults.pandas.core import get_core_nodes
from cvp.nodes.defaults.pandas.groupby import get_groupby_nodes
from cvp.nodes.defaults.pandas.io import get_io_nodes
from cvp.nodes.defaults.pandas.manipulation import get_manipulation_nodes
from cvp.nodes.defaults.pandas.statistics import get_statistics_nodes
from cvp.nodes.node import Node


def get_pandas_nodes() -> List[Node]:
    """Get all pandas nodes."""
    result: List[Node] = []
    result.extend(get_core_nodes())
    result.extend(get_io_nodes())
    result.extend(get_manipulation_nodes())
    result.extend(get_statistics_nodes())
    result.extend(get_groupby_nodes())
    return result
