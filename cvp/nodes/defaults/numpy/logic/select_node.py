# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class SelectNode(NumpyFunctionNode):
    """Return an array drawn from elements in choicelist, depending on conditions."""

    def __init__(self):
        condlist_pin = DataInputPin(
            name=PinName("condlist"),
            dtype=Dtype.any(),
            docs="List of conditions which determine from which array to choose",
        )
        choicelist_pin = DataInputPin(
            name=PinName("choicelist"),
            dtype=Dtype.any(),
            docs="List of arrays from which to choose",
        )
        default_pin = DataInputPin(
            name=PinName("default"),
            dtype=Dtype.any(),
            docs="Element inserted in output when all conditions evaluate to False",
            default=0,
        )
        super().__init__("select", condlist_pin, choicelist_pin, default_pin)

    def apply_function(self, condlist, choicelist, default, **kwargs) -> Any:
        return np.select(condlist, choicelist, default=default)
