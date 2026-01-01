# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class WarpAffineNode(OpenCVFunctionNode):
    """Apply affine transformation to image."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        m_pin = DataInputPin(
            name=PinName("M"),
            dtype=Dtype.any(),
            docs="2x3 transformation matrix",
        )
        dsize_pin = DataInputPin(
            name=PinName("dsize"),
            dtype=Dtype.any(),
            docs="Output image size (width, height)",
        )
        flags_pin = DataInputPin(
            name=PinName("flags"),
            dtype=Dtype(int),
            docs="Interpolation flags",
            default=cv2.INTER_LINEAR,
        )
        bordermode_pin = DataInputPin(
            name=PinName("borderMode"),
            dtype=Dtype(int),
            docs="Border extrapolation mode",
            default=cv2.BORDER_CONSTANT,
        )
        bordervalue_pin = DataInputPin(
            name=PinName("borderValue"),
            dtype=Dtype.any(),
            docs="Border value for constant border",
            default=(0, 0, 0),
        )
        super().__init__(
            "warpAffine",
            src_pin,
            m_pin,
            dsize_pin,
            flags_pin,
            bordermode_pin,
            bordervalue_pin,
        )

    def apply_function(
        self, src, M, dsize, flags, borderMode, borderValue, **kwargs
    ) -> Any:
        return cv2.warpAffine(
            src, M, dsize, flags=flags, borderMode=borderMode, borderValue=borderValue
        )
