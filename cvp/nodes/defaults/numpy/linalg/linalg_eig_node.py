# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgEigNode(NumpyFunctionNode):
    """Compute the eigenvalues and right eigenvectors of a square array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Square matrix to compute eigenvalues/vectors",
        )
        super().__init__("eig", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.linalg.eig(a)
