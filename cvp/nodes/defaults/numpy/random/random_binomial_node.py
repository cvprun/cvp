# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomBinomialNode(NumpyFunctionNode):
    """Draw samples from a binomial distribution."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Number of trials",
        )
        p_pin = DataInputPin(
            name=PinName("p"),
            dtype=Dtype.any(),
            docs="Probability of success",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("binomial", n_pin, p_pin, size_pin)

    def apply_function(self, n, p, size, **kwargs) -> Any:
        return np.random.binomial(n=n, p=p, size=size)
