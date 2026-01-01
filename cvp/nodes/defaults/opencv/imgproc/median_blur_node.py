# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class MedianBlurNode(OpenCVFunctionNode):
    """Apply median blur filter."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        ksize_pin = DataInputPin(
            name=PinName("ksize"),
            dtype=Dtype(int),
            docs="Size of median filter kernel (odd number)",
            default=5,
        )
        super().__init__("medianBlur", src_pin, ksize_pin)

    def apply_function(self, src, ksize, **kwargs) -> Any:
        return cv2.medianBlur(src, ksize)
