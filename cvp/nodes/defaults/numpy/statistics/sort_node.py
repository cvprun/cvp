# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class SortNode(NumpyFunctionNode):
    """Return a sorted copy of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array to be sorted",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to sort",
            default=-1,
        )
        kind_pin = DataInputPin(
            name=PinName("kind"),
            dtype=Dtype.any(),
            docs="Sorting algorithm",
            default=None,
        )
        super().__init__("sort", array_pin, axis_pin, kind_pin)

    def apply_function(self, a, axis, kind, **kwargs) -> Any:
        return np.sort(a, axis=axis, kind=kind)
