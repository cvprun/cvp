# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.defaults.numpy.array_creation import get_array_creation_nodes
from cvp.nodes.defaults.numpy.mathematical import get_mathematical_nodes
from cvp.nodes.defaults.numpy.array_manipulation import get_array_manipulation_nodes
from cvp.nodes.defaults.numpy.linalg import get_linalg_nodes
from cvp.nodes.defaults.numpy.statistics import get_statistics_nodes
from cvp.nodes.defaults.numpy.fft import get_fft_nodes
from cvp.nodes.defaults.numpy.random import get_random_nodes
from cvp.nodes.defaults.numpy.logic import get_logic_nodes
from cvp.nodes.node import Node


def get_numpy_nodes() -> List[Node]:
    """Get all numpy nodes."""
    result: List[Node] = []
    result.extend(get_array_creation_nodes())
    result.extend(get_mathematical_nodes())
    result.extend(get_array_manipulation_nodes())
    result.extend(get_linalg_nodes())
    result.extend(get_statistics_nodes())
    result.extend(get_fft_nodes())
    result.extend(get_random_nodes())
    result.extend(get_logic_nodes())
    return result