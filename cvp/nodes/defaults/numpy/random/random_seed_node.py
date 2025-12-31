# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomSeedNode(NumpyFunctionNode):
    """Seed the generator."""

    def __init__(self):
        seed_pin = DataInputPin(
            name=PinName("seed"),
            dtype=Dtype.any(),
            docs="Seed for random number generator",
            default=None,
        )
        super().__init__("seed", seed_pin)

    def apply_function(self, seed, **kwargs) -> Any:
        np.random.seed(seed)
        return None
