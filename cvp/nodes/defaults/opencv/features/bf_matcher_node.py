# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class BFMatcherNode(OpenCVFunctionNode):
    """Match descriptors using Brute-Force matcher."""

    def __init__(self):
        desc1_pin = DataInputPin(
            name=PinName("queryDescriptors"),
            dtype=Dtype.any(),
            docs="Query descriptors",
        )
        desc2_pin = DataInputPin(
            name=PinName("trainDescriptors"),
            dtype=Dtype.any(),
            docs="Train descriptors",
        )
        normtype_pin = DataInputPin(
            name=PinName("normType"),
            dtype=Dtype(int),
            docs="Distance measurement type",
            default=cv2.NORM_L2,
        )
        crosscheck_pin = DataInputPin(
            name=PinName("crossCheck"),
            dtype=Dtype(bool),
            docs="Enable cross check",
            default=False,
        )
        k_pin = DataInputPin(
            name=PinName("k"),
            dtype=Dtype(int),
            docs="Number of best matches to find",
            default=2,
        )

        # Initialize with custom functionality
        self._function_name = "BFMatcher_match"
        self._input_pins = (desc1_pin, desc2_pin, normtype_pin, crosscheck_pin, k_pin)
        super().__init__.__bases__[0].__init__(self, *self._input_pins)

    def apply_function(
        self, queryDescriptors, trainDescriptors, normType, crossCheck, k, **kwargs
    ) -> Any:
        matcher = cv2.BFMatcher(normType, crossCheck)
        if k == 1:
            matches = matcher.match(queryDescriptors, trainDescriptors)
            return matches
        else:
            # knnMatch returns List[List[DMatch]], return directly with proper type
            return matcher.knnMatch(queryDescriptors, trainDescriptors, k=k)

    def run(self, record):
        # Get input values
        inputs = [record.get(pin) for pin in self._input_pins]

        # Apply matching
        matches = self.apply_function(*inputs)

        # Set output
        record.set(self._output, matches)
        return self.nonext()
