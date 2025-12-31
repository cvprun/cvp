# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class DstackNode(NumpyFunctionNode):
    """Stack arrays in sequence depth wise (along third axis)."""

    def __init__(self):
        arrays_pin = DataInputPin(
            name=PinName("tup"),
            dtype=Dtype.any(),
            docs="Sequence of arrays",
        )
        super().__init__("dstack", arrays_pin)

    def apply_function(self, tup, **kwargs) -> Any:
        return np.dstack(tup)
