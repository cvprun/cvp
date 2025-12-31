# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class WhereNode(NumpyFunctionNode):
    """Return elements chosen from x or y depending on condition."""

    def __init__(self):
        condition_pin = DataInputPin(
            name=PinName("condition"),
            dtype=Dtype.any(),
            docs="Where True, yield x, otherwise yield y",
        )
        x_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Values from which to choose when condition is True",
            default=None,
        )
        y_pin = DataInputPin(
            name=PinName("y"),
            dtype=Dtype.any(),
            docs="Values from which to choose when condition is False",
            default=None,
        )
        super().__init__("where", condition_pin, x_pin, y_pin)

    def apply_function(self, condition, x, y, **kwargs) -> Any:
        if x is None and y is None:
            return np.where(condition)
        return np.where(condition, x, y)
