# -*- coding: utf-8 -*-

from typing import Any

import cv2
import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class HoughLinesPNode(OpenCVFunctionNode):
    """Detect line segments using probabilistic Hough transform."""

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
            default=50,
        )
        minlinelength_pin = DataInputPin(
            name=PinName("minLineLength"),
            dtype=Dtype(float),
            docs="Minimum line length",
            default=50.0,
        )
        maxlinegap_pin = DataInputPin(
            name=PinName("maxLineGap"),
            dtype=Dtype(float),
            docs="Maximum allowed gap between line segments",
            default=10.0,
        )
        super().__init__(
            "HoughLinesP",
            image_pin,
            rho_pin,
            theta_pin,
            threshold_pin,
            minlinelength_pin,
            maxlinegap_pin,
        )

    def apply_function(
        self, image, rho, theta, threshold, minLineLength, maxLineGap, **kwargs
    ) -> Any:
        return cv2.HoughLinesP(
            image,
            rho,
            theta,
            threshold,
            minLineLength=minLineLength,
            maxLineGap=maxLineGap,
        )
