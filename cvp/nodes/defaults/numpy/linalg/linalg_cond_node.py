# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgCondNode(NumpyFunctionNode):
    """Compute the condition number of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Matrix whose condition number is sought",
        )
        p_pin = DataInputPin(
            name=PinName("p"),
            dtype=Dtype.any(),
            docs="Order of the norm used in the condition number computation",
            default=None,
        )
        super().__init__("cond", array_pin, p_pin)

    def apply_function(self, x, p, **kwargs) -> Any:
        return np.linalg.cond(x, p=p)
