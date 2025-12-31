# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgQrNode(NumpyFunctionNode):
    """Compute the qr factorization of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Matrix to be factored",
        )
        mode_pin = DataInputPin(
            name=PinName("mode"),
            dtype=Dtype.any(),
            docs="Decomposition mode ('reduced', 'complete', 'r', 'raw')",
            default="reduced",
        )
        super().__init__("qr", array_pin, mode_pin)

    def apply_function(self, a, mode, **kwargs) -> Any:
        return np.linalg.qr(a, mode=mode)
