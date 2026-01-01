# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class DrawContoursNode(OpenCVFunctionNode):
    """Draw contours on image."""

    def __init__(self):
        image_pin = DataInputPin(
            name=PinName("image"),
            dtype=Dtype.any(),
            docs="Image to draw on",
        )
        contours_pin = DataInputPin(
            name=PinName("contours"),
            dtype=Dtype.any(),
            docs="List of contours",
        )
        contouridx_pin = DataInputPin(
            name=PinName("contourIdx"),
            dtype=Dtype(int),
            docs="Contour index (-1 for all contours)",
            default=-1,
        )
        color_pin = DataInputPin(
            name=PinName("color"),
            dtype=Dtype.any(),
            docs="Contour color",
            default=(0, 255, 0),
        )
        thickness_pin = DataInputPin(
            name=PinName("thickness"),
            dtype=Dtype(int),
            docs="Contour thickness",
            default=2,
        )
        super().__init__(
            "drawContours",
            image_pin,
            contours_pin,
            contouridx_pin,
            color_pin,
            thickness_pin,
        )

    def apply_function(
        self, image, contours, contourIdx, color, thickness, **kwargs
    ) -> Any:
        return cv2.drawContours(image, contours, contourIdx, color, thickness)
