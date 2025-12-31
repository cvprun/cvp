# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgLstsqNode(NumpyFunctionNode):
    """Return the least-squares solution to a linear matrix equation."""

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
        rcond_pin = DataInputPin(
            name=PinName("rcond"),
            dtype=Dtype.any(),
            docs="Cut-off ratio for small singular values",
            default=None,
        )
        super().__init__("lstsq", a_pin, b_pin, rcond_pin)

    def apply_function(self, a, b, rcond, **kwargs) -> Any:
        return np.linalg.lstsq(a, b, rcond=rcond)
