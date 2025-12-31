# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class DsplitNode(NumpyFunctionNode):
    """Split array along the 3rd axis (depth)."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("ary"),
            dtype=Dtype.any(),
            docs="Array to be divided into sub-arrays",
        )
        indices_pin = DataInputPin(
            name=PinName("indices_or_sections"),
            dtype=Dtype.any(),
            docs="If integer, number of equal sections",
        )
        super().__init__("dsplit", array_pin, indices_pin)

    def apply_function(self, ary, indices_or_sections, **kwargs) -> Any:
        return np.dsplit(ary, indices_or_sections)
