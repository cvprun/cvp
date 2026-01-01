# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class HoughCirclesNode(OpenCVFunctionNode):
    """Detect circles using Hough transform."""

    def __init__(self):
        image_pin = DataInputPin(
            name=PinName("image"),
            dtype=Dtype.any(),
            docs="Source grayscale image",
        )
        method_pin = DataInputPin(
            name=PinName("method"),
            dtype=Dtype(int),
            docs="Detection method (cv2.HOUGH_GRADIENT)",
            default=cv2.HOUGH_GRADIENT,
        )
        dp_pin = DataInputPin(
            name=PinName("dp"),
            dtype=Dtype(float),
            docs="Inverse ratio of accumulator resolution to image resolution",
            default=1.0,
        )
        mindist_pin = DataInputPin(
            name=PinName("minDist"),
            dtype=Dtype(float),
            docs="Minimum distance between circle centers",
            default=100.0,
        )
        param1_pin = DataInputPin(
            name=PinName("param1"),
            dtype=Dtype(float),
            docs="Upper threshold for edge detection",
            default=100.0,
        )
        param2_pin = DataInputPin(
            name=PinName("param2"),
            dtype=Dtype(float),
            docs="Accumulator threshold for center detection",
            default=30.0,
        )
        minradius_pin = DataInputPin(
            name=PinName("minRadius"),
            dtype=Dtype(int),
            docs="Minimum circle radius",
            default=0,
        )
        maxradius_pin = DataInputPin(
            name=PinName("maxRadius"),
            dtype=Dtype(int),
            docs="Maximum circle radius",
            default=0,
        )
        super().__init__(
            "HoughCircles",
            image_pin,
            method_pin,
            dp_pin,
            mindist_pin,
            param1_pin,
            param2_pin,
            minradius_pin,
            maxradius_pin,
        )

    def apply_function(
        self, image, method, dp, minDist, param1, param2, minRadius, maxRadius, **kwargs
    ) -> Any:
        return cv2.HoughCircles(
            image,
            method,
            dp,
            minDist,
            param1=param1,
            param2=param2,
            minRadius=minRadius,
            maxRadius=maxRadius,
        )
