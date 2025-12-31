# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomMultivariateNormalNode(NumpyFunctionNode):
    """Draw random samples from a multivariate normal distribution."""

    def __init__(self):
        mean_pin = DataInputPin(
            name=PinName("mean"),
            dtype=Dtype.any(),
            docs="Mean of the N-dimensional distribution",
        )
        cov_pin = DataInputPin(
            name=PinName("cov"),
            dtype=Dtype.any(),
            docs="Covariance matrix of the distribution",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Given shape",
            default=None,
        )
        super().__init__("multivariate_normal", mean_pin, cov_pin, size_pin)

    def apply_function(self, mean, cov, size, **kwargs) -> Any:
        return np.random.multivariate_normal(mean=mean, cov=cov, size=size)
