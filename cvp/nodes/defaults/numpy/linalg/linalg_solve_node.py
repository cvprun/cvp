# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgSolveNode(NumpyFunctionNode):
    """Solve a linear matrix equation, or system of linear scalar equations."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Coefficient matrix",
        )
        b_pin = DataInputPin(
            name=PinName("b"),
            dtype=Dtype.any(),
            docs="Ordinate or dependent variable values",
        )
        super().__init__("solve", a_pin, b_pin)

    def apply_function(self, a, b, **kwargs) -> Any:
        return np.linalg.solve(a, b)
