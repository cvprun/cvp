# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class GetStructuringElementNode(OpenCVFunctionNode):
    """Create structuring element for morphological operations."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype(int),
            docs="Shape of structuring element (cv2.MORPH_*)",
            default=cv2.MORPH_RECT,
        )
        ksize_pin = DataInputPin(
            name=PinName("ksize"),
            dtype=Dtype.any(),
            docs="Size of structuring element (width, height)",
            default=(5, 5),
        )
        anchor_pin = DataInputPin(
            name=PinName("anchor"),
            dtype=Dtype.any(),
            docs="Anchor position",
            default=(-1, -1),
        )
        super().__init__("getStructuringElement", shape_pin, ksize_pin, anchor_pin)

    def apply_function(self, shape, ksize, anchor, **kwargs) -> Any:
        return cv2.getStructuringElement(shape, ksize, anchor=anchor)
