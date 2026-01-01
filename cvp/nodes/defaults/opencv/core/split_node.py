# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class SplitNode(OpenCVFunctionNode):
    """Split multi-channel image into separate channels."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Multi-channel source image",
        )
        super().__init__("split", src_pin)

    def apply_function(self, src, **kwargs) -> Any:
        return cv2.split(src)
