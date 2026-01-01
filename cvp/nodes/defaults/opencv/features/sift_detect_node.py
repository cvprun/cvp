# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import PinName


class SIFTDetectNode(OpenCVFunctionNode):
    """Detect keypoints using SIFT algorithm."""

    def __init__(self):
        image_pin = DataInputPin(
            name=PinName("image"),
            dtype=Dtype.any(),
            docs="Source grayscale image",
        )
        mask_pin = DataInputPin(
            name=PinName("mask"),
            dtype=Dtype.any(),
            docs="Optional mask for keypoint detection",
            default=None,
        )

        # Override the default output to include both keypoints and descriptors
        self._keypoints_output = DataOutputPin(
            name=PinName("keypoints"),
            dtype=Dtype.any(),
            docs="Detected keypoints",
        )
        self._descriptors_output = DataOutputPin(
            name=PinName("descriptors"),
            dtype=Dtype.any(),
            docs="SIFT descriptors",
        )

        # Initialize with custom pins
        self._function_name = "SIFT_detectAndCompute"
        self._input_pins = (image_pin, mask_pin)
        self._sift = cv2.SIFT_create()
        super().__init__.__bases__[0].__init__(
            self, *self._input_pins, self._keypoints_output, self._descriptors_output
        )

    def apply_function(self, image, mask, **kwargs) -> Any:
        keypoints, descriptors = self._sift.detectAndCompute(image, mask)
        return keypoints, descriptors

    def run(self, record):
        # Get input values
        inputs = [record.get(pin) for pin in self._input_pins]

        # Apply SIFT detection
        keypoints, descriptors = self.apply_function(*inputs)

        # Set outputs
        record.set(self._keypoints_output, keypoints)
        record.set(self._descriptors_output, descriptors)
        return self.nonext()
