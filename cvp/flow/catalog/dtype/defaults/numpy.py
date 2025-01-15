# -*- coding: utf-8 -*-

from numpy import ndarray

from cvp.flow.icons.dtype import DTYPE_ICON_MAPPING
from cvp.flow.templates.dtype import Dtype
from cvp.types.colors import WHITE_RGBA


class NDArrayDtype(Dtype):
    def __init__(self):
        super().__init__(
            name="ndarray",
            path="numpy.ndarray",
            base=ndarray,
            docs=(
                "An array object represents a multidimensional, "
                "homogeneous array of fixed-size items"
            ),
            icon=DTYPE_ICON_MAPPING["N"],
            color=WHITE_RGBA,
        )
