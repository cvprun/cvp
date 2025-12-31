# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgEighvalsNode(NumpyFunctionNode):
    """Return eigenvalues of a complex Hermitian matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Complex Hermitian matrix",
        )
        uplo_pin = DataInputPin(
            name=PinName("UPLO"),
            dtype=Dtype.any(),
            docs="Whether to use lower ('L') or upper ('U') triangular part",
            default="L",
        )
        super().__init__("eigvalsh", array_pin, uplo_pin)

    def apply_function(self, a, uplo, **kwargs) -> Any:
        return np.linalg.eigvalsh(a, UPLO=uplo)
