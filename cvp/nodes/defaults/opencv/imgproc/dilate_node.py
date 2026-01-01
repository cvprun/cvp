# -*- coding: utf-8 -*-

from typing import Any

import cv2
import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class DilateNode(OpenCVFunctionNode):
    """Apply dilation morphological operation."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        kernel_pin = DataInputPin(
            name=PinName("kernel"),
            dtype=Dtype.any(),
            docs="Structuring element",
            default=None,
        )
        anchor_pin = DataInputPin(
            name=PinName("anchor"),
            dtype=Dtype.any(),
            docs="Anchor position",
            default=(-1, -1),
        )
        iterations_pin = DataInputPin(
            name=PinName("iterations"),
            dtype=Dtype(int),
            docs="Number of iterations",
            default=1,
        )
        bordertype_pin = DataInputPin(
            name=PinName("borderType"),
            dtype=Dtype(int),
            docs="Border extrapolation type",
            default=cv2.BORDER_CONSTANT,
        )
        super().__init__(
            "dilate", src_pin, kernel_pin, anchor_pin, iterations_pin, bordertype_pin
        )

    def apply_function(
        self, src, kernel, anchor, iterations, borderType, **kwargs
    ) -> Any:
        if kernel is None:
            kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(
            src, kernel, anchor=anchor, iterations=iterations, borderType=borderType
        )
