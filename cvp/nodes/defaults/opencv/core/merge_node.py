# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class MergeNode(OpenCVFunctionNode):
    """Merge separate channels into multi-channel image."""

    def __init__(self):
        channels_pin = DataInputPin(
            name=PinName("mv"),
            dtype=Dtype.any(),
            docs="List of channels to merge",
        )
        super().__init__("merge", channels_pin)

    def apply_function(self, mv, **kwargs) -> Any:
        return cv2.merge(mv)
