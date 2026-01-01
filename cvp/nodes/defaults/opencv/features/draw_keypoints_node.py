# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class DrawKeypointsNode(OpenCVFunctionNode):
    """Draw keypoints on image."""

    def __init__(self):
        image_pin = DataInputPin(
            name=PinName("image"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        keypoints_pin = DataInputPin(
            name=PinName("keypoints"),
            dtype=Dtype.any(),
            docs="Keypoints to draw",
        )
        color_pin = DataInputPin(
            name=PinName("color"),
            dtype=Dtype.any(),
            docs="Color for keypoints",
            default=(0, 255, 0),
        )
        flags_pin = DataInputPin(
            name=PinName("flags"),
            dtype=Dtype(int),
            docs="Drawing flags",
            default=cv2.DRAW_MATCHES_FLAGS_DEFAULT,
        )
        super().__init__(
            "drawKeypoints", image_pin, keypoints_pin, color_pin, flags_pin
        )

    def apply_function(self, image, keypoints, color, flags, **kwargs) -> Any:
        return cv2.drawKeypoints(image, keypoints, None, color=color, flags=flags)
