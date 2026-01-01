# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class AdaptiveThresholdNode(OpenCVFunctionNode):
    """Apply adaptive threshold."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source grayscale image",
        )
        maxvalue_pin = DataInputPin(
            name=PinName("maxValue"),
            dtype=Dtype(float),
            docs="Maximum value for binary threshold",
            default=255.0,
        )
        adaptivemethod_pin = DataInputPin(
            name=PinName("adaptiveMethod"),
            dtype=Dtype(int),
            docs="Adaptive method (cv2.ADAPTIVE_THRESH_*)",
            default=cv2.ADAPTIVE_THRESH_MEAN_C,
        )
        thresholdtype_pin = DataInputPin(
            name=PinName("thresholdType"),
            dtype=Dtype(int),
            docs="Threshold type (cv2.THRESH_*)",
            default=cv2.THRESH_BINARY,
        )
        blocksize_pin = DataInputPin(
            name=PinName("blockSize"),
            dtype=Dtype(int),
            docs="Size of neighborhood area",
            default=11,
        )
        c_pin = DataInputPin(
            name=PinName("C"),
            dtype=Dtype(float),
            docs="Constant subtracted from the mean",
            default=2.0,
        )
        super().__init__(
            "adaptiveThreshold",
            src_pin,
            maxvalue_pin,
            adaptivemethod_pin,
            thresholdtype_pin,
            blocksize_pin,
            c_pin,
        )

    def apply_function(
        self, src, maxValue, adaptiveMethod, thresholdType, blockSize, C, **kwargs
    ) -> Any:
        return cv2.adaptiveThreshold(
            src, maxValue, adaptiveMethod, thresholdType, blockSize, C
        )
