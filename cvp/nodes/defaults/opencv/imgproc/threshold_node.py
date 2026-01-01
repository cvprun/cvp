# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import PinName


class ThresholdNode(OpenCVFunctionNode):
    """Apply fixed-level threshold."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source grayscale image",
        )
        thresh_pin = DataInputPin(
            name=PinName("thresh"),
            dtype=Dtype(float),
            docs="Threshold value",
            default=127.0,
        )
        maxval_pin = DataInputPin(
            name=PinName("maxval"),
            dtype=Dtype(float),
            docs="Maximum value for THRESH_BINARY",
            default=255.0,
        )
        type_pin = DataInputPin(
            name=PinName("type"),
            dtype=Dtype(int),
            docs="Threshold type (cv2.THRESH_*)",
            default=cv2.THRESH_BINARY,
        )

        # Override the default output to include both threshold and image
        self._retval_output = DataOutputPin(
            name=PinName("retval"),
            dtype=Dtype.any(),
            docs="Actual threshold value used",
        )
        self._thresh_output = DataOutputPin(
            name=PinName("dst"),
            dtype=Dtype.any(),
            docs="Thresholded image",
        )

        # Initialize with custom pins
        self._function_name = "threshold"
        self._input_pins = (src_pin, thresh_pin, maxval_pin, type_pin)
        super().__init__.__bases__[0].__init__(
            self, *self._input_pins, self._retval_output, self._thresh_output
        )

    def apply_function(self, src, thresh, maxval, type, **kwargs) -> Any:
        retval, dst = cv2.threshold(src, thresh, maxval, type)
        return retval, dst

    def run(self, record):
        # Get input values
        inputs = [record.get(pin) for pin in self._input_pins]

        # Apply OpenCV function
        retval, dst = self.apply_function(*inputs)

        # Set outputs
        record.set(self._retval_output, retval)
        record.set(self._thresh_output, dst)
        return self.nonext()
