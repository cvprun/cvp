# -*- coding: utf-8 -*-

from typing import Any

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class CopyToNode(OpenCVFunctionNode):
    """Copy source image to destination with optional mask."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        dst_pin = DataInputPin(
            name=PinName("dst"),
            dtype=Dtype.any(),
            docs="Destination image",
        )
        mask_pin = DataInputPin(
            name=PinName("mask"),
            dtype=Dtype.any(),
            docs="Mask for selective copying",
            default=None,
        )
        super().__init__("copyTo", src_pin, dst_pin, mask_pin)

    def apply_function(self, src, dst, mask, **kwargs) -> Any:
        if mask is None:
            src.copyTo(dst)
        else:
            src.copyTo(dst, mask)
        return dst
