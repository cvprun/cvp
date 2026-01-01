# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import PinName


class CalcOpticalFlowPyrLKNode(OpenCVFunctionNode):
    """Calculate optical flow using Lucas-Kanade method."""

    def __init__(self):
        previmg_pin = DataInputPin(
            name=PinName("prevImg"),
            dtype=Dtype.any(),
            docs="Previous frame (grayscale)",
        )
        nextimg_pin = DataInputPin(
            name=PinName("nextImg"),
            dtype=Dtype.any(),
            docs="Next frame (grayscale)",
        )
        prevpts_pin = DataInputPin(
            name=PinName("prevPts"),
            dtype=Dtype.any(),
            docs="Points to track from previous frame",
        )
        winsize_pin = DataInputPin(
            name=PinName("winSize"),
            dtype=Dtype.any(),
            docs="Size of search window",
            default=(15, 15),
        )
        maxlevel_pin = DataInputPin(
            name=PinName("maxLevel"),
            dtype=Dtype(int),
            docs="Maximum pyramid level",
            default=2,
        )

        # Override the default output to include multiple outputs
        self._nextpts_output = DataOutputPin(
            name=PinName("nextPts"),
            dtype=Dtype.any(),
            docs="Tracked points in next frame",
        )
        self._status_output = DataOutputPin(
            name=PinName("status"),
            dtype=Dtype.any(),
            docs="Status of tracked points",
        )
        self._error_output = DataOutputPin(
            name=PinName("error"),
            dtype=Dtype.any(),
            docs="Tracking error for each point",
        )

        # Initialize with custom pins
        self._function_name = "calcOpticalFlowPyrLK"
        self._input_pins = (
            previmg_pin,
            nextimg_pin,
            prevpts_pin,
            winsize_pin,
            maxlevel_pin,
        )
        super().__init__.__bases__[0].__init__(
            self,
            *self._input_pins,
            self._nextpts_output,
            self._status_output,
            self._error_output
        )

    def apply_function(
        self, prevImg, nextImg, prevPts, winSize, maxLevel, **kwargs
    ) -> Any:
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01)
        nextPts, status, error = cv2.calcOpticalFlowPyrLK(
            prevImg,
            nextImg,
            prevPts,
            None,
            winSize=winSize,
            maxLevel=maxLevel,
            criteria=criteria,
        )
        return nextPts, status, error

    def run(self, record):
        # Get input values
        inputs = [record.get(pin) for pin in self._input_pins]

        # Apply optical flow
        nextPts, status, error = self.apply_function(*inputs)

        # Set outputs
        record.set(self._nextpts_output, nextPts)
        record.set(self._status_output, status)
        record.set(self._error_output, error)
        return self.nonext()
