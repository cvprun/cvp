# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class CvtColorNode(OpenCVFunctionNode):
    """Convert image from one color space to another."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        code_pin = DataInputPin(
            name=PinName("code"),
            dtype=Dtype(int),
            docs="Color conversion code (cv2.COLOR_*)",
            default=cv2.COLOR_BGR2RGB,
        )
        dstcn_pin = DataInputPin(
            name=PinName("dstCn"),
            dtype=Dtype(int),
            docs="Number of channels in destination image",
            default=0,
        )
        super().__init__("cvtColor", src_pin, code_pin, dstcn_pin)

    def apply_function(self, src, code, dstCn, **kwargs) -> Any:
        return cv2.cvtColor(src, code, dstCn=dstCn)
