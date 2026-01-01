# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class BlurNode(OpenCVFunctionNode):
    """Apply simple box filter blur."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        ksize_pin = DataInputPin(
            name=PinName("ksize"),
            dtype=Dtype.any(),
            docs="Blur kernel size (width, height)",
            default=(5, 5),
        )
        anchor_pin = DataInputPin(
            name=PinName("anchor"),
            dtype=Dtype.any(),
            docs="Anchor point",
            default=(-1, -1),
        )
        bordertype_pin = DataInputPin(
            name=PinName("borderType"),
            dtype=Dtype(int),
            docs="Border extrapolation type",
            default=cv2.BORDER_DEFAULT,
        )
        super().__init__("blur", src_pin, ksize_pin, anchor_pin, bordertype_pin)

    def apply_function(self, src, ksize, anchor, borderType, **kwargs) -> Any:
        return cv2.blur(src, ksize, anchor=anchor, borderType=borderType)
