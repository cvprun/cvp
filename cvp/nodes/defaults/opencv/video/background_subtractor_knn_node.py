# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class BackgroundSubtractorKNNNode(OpenCVFunctionNode):
    """Apply KNN background subtraction."""

    def __init__(self):
        frame_pin = DataInputPin(
            name=PinName("frame"),
            dtype=Dtype.any(),
            docs="Input frame",
        )
        learningrate_pin = DataInputPin(
            name=PinName("learningRate"),
            dtype=Dtype(float),
            docs="Learning rate for background model",
            default=-1.0,
        )

        # Initialize background subtractor
        self._bg_subtractor = cv2.createBackgroundSubtractorKNN()
        self._function_name = "BackgroundSubtractorKNN"
        self._input_pins = (frame_pin, learningrate_pin)
        super().__init__.__bases__[0].__init__(self, *self._input_pins)

    def apply_function(self, frame, learningRate, **kwargs) -> Any:
        return self._bg_subtractor.apply(frame, learningRate=learningRate)

    def run(self, record):
        # Get input values
        inputs = [record.get(pin) for pin in self._input_pins]

        # Apply background subtraction
        result = self.apply_function(*inputs)

        # Set output
        record.set(self._output, result)
        return self.nonext()
