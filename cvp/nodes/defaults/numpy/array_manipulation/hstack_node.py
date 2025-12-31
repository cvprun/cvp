# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class HstackNode(NumpyFunctionNode):
    """Stack arrays in sequence horizontally (column wise)."""

    def __init__(self):
        arrays_pin = DataInputPin(
            name=PinName("tup"),
            dtype=Dtype.any(),
            docs="Sequence of arrays",
        )
        super().__init__("hstack", arrays_pin)

    def apply_function(self, tup, **kwargs) -> Any:
        return np.hstack(tup)
