# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomChoiceNode(NumpyFunctionNode):
    """Generates a random sample from a given 1-D array."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="1-D array-like or int",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        replace_pin = DataInputPin(
            name=PinName("replace"),
            dtype=Dtype.any(),
            docs="Whether the sample is with or without replacement",
            default=True,
        )
        p_pin = DataInputPin(
            name=PinName("p"),
            dtype=Dtype.any(),
            docs="Probabilities associated with each entry",
            default=None,
        )
        super().__init__("choice", a_pin, size_pin, replace_pin, p_pin)

    def apply_function(self, a, size, replace, p, **kwargs) -> Any:
        return np.random.choice(a, size=size, replace=replace, p=p)
