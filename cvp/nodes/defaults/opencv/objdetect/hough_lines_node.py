# -*- coding: utf-8 -*-

from typing import Any

import cv2
import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class HoughLinesNode(OpenCVFunctionNode):
    """Detect lines using standard Hough transform."""

    def __init__(self):
        image_pin = DataInputPin(
            name=PinName("image"),
            dtype=Dtype.any(),
            docs="Source binary image (typically edge image)",
        )
        rho_pin = DataInputPin(
            name=PinName("rho"),
            dtype=Dtype(float),
            docs="Distance resolution in pixels",
            default=1.0,
        )
        theta_pin = DataInputPin(
            name=PinName("theta"),
            dtype=Dtype(float),
            docs="Angle resolution in radians",
            default=np.pi / 180,
        )
        threshold_pin = DataInputPin(
            name=PinName("threshold"),
            dtype=Dtype(int),
            docs="Minimum number of intersections for line detection",
            default=100,
        )
        srn_pin = DataInputPin(
            name=PinName("srn"),
            dtype=Dtype(float),
            docs="Divisor for distance resolution rho",
            default=0.0,
        )
        stn_pin = DataInputPin(
            name=PinName("stn"),
            dtype=Dtype(float),
            docs="Divisor for angle resolution theta",
            default=0.0,
        )
        super().__init__(
            "HoughLines", image_pin, rho_pin, theta_pin, threshold_pin, srn_pin, stn_pin
        )

    def apply_function(self, image, rho, theta, threshold, srn, stn, **kwargs) -> Any:
        return cv2.HoughLines(image, rho, theta, threshold, srn=srn, stn=stn)
