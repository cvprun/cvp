# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import PinName


class FindContoursNode(OpenCVFunctionNode):
    """Find contours in binary image."""

    def __init__(self):
        image_pin = DataInputPin(
            name=PinName("image"),
            dtype=Dtype.any(),
            docs="Source binary image",
        )
        mode_pin = DataInputPin(
            name=PinName("mode"),
            dtype=Dtype(int),
            docs="Contour retrieval mode (cv2.RETR_*)",
            default=cv2.RETR_EXTERNAL,
        )
        method_pin = DataInputPin(
            name=PinName("method"),
            dtype=Dtype(int),
            docs="Contour approximation method (cv2.CHAIN_*)",
            default=cv2.CHAIN_APPROX_SIMPLE,
        )

        # Override the default output to include both contours and hierarchy
        self._contours_output = DataOutputPin(
            name=PinName("contours"),
            dtype=Dtype.any(),
            docs="List of contours",
        )
        self._hierarchy_output = DataOutputPin(
            name=PinName("hierarchy"),
            dtype=Dtype.any(),
            docs="Contour hierarchy information",
        )

        # Initialize with custom pins
        self._function_name = "findContours"
        self._input_pins = (image_pin, mode_pin, method_pin)
        super().__init__.__bases__[0].__init__(
            self, *self._input_pins, self._contours_output, self._hierarchy_output
        )

    def apply_function(self, image, mode, method, **kwargs) -> Any:
        contours, hierarchy = cv2.findContours(image, mode, method)
        return contours, hierarchy

    def run(self, record):
        # Get input values
        inputs = [record.get(pin) for pin in self._input_pins]

        # Apply OpenCV function
        contours, hierarchy = self.apply_function(*inputs)

        # Set outputs
        record.set(self._contours_output, contours)
        record.set(self._hierarchy_output, hierarchy)
        return self.nonext()
