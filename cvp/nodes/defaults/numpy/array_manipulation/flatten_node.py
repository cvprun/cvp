# -*- coding: utf-8 -*-

from typing import Any

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class FlattenNode(NumpyFunctionNode):
    """Return a copy of the array collapsed into one dimension."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        super().__init__("flatten", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return a.flatten()
