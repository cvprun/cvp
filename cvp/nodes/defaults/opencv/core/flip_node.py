# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class FlipNode(OpenCVFunctionNode):
    """Flip image around vertical, horizontal, or both axes."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        flipcode_pin = DataInputPin(
            name=PinName("flipCode"),
            dtype=Dtype(int),
            docs="Flip code (0=horizontal, 1=vertical, -1=both)",
            default=1,
        )
        super().__init__("flip", src_pin, flipcode_pin)

    def apply_function(self, src, flipCode, **kwargs) -> Any:
        return cv2.flip(src, flipCode)
