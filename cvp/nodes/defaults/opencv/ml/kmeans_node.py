# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import PinName


class KMeansNode(OpenCVFunctionNode):
    """Apply K-means clustering."""

    def __init__(self):
        data_pin = DataInputPin(
            name=PinName("data"),
            dtype=Dtype.any(),
            docs="Input data for clustering",
        )
        k_pin = DataInputPin(
            name=PinName("K"),
            dtype=Dtype(int),
            docs="Number of clusters",
            default=2,
        )
        attempts_pin = DataInputPin(
            name=PinName("attempts"),
            dtype=Dtype(int),
            docs="Number of attempts",
            default=10,
        )
        flags_pin = DataInputPin(
            name=PinName("flags"),
            dtype=Dtype(int),
            docs="Initialization flags",
            default=cv2.KMEANS_RANDOM_CENTERS,
        )

        # Override the default output to include multiple outputs
        self._compactness_output = DataOutputPin(
            name=PinName("compactness"),
            dtype=Dtype.any(),
            docs="Compactness measure",
        )
        self._labels_output = DataOutputPin(
            name=PinName("labels"),
            dtype=Dtype.any(),
            docs="Cluster labels for each data point",
        )
        self._centers_output = DataOutputPin(
            name=PinName("centers"),
            dtype=Dtype.any(),
            docs="Cluster centers",
        )

        # Initialize with custom pins
        self._function_name = "kmeans"
        self._input_pins = (data_pin, k_pin, attempts_pin, flags_pin)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        self._criteria = criteria
        super().__init__.__bases__[0].__init__(
            self,
            *self._input_pins,
            self._compactness_output,
            self._labels_output,
            self._centers_output
        )

    def apply_function(self, data, K, attempts, flags, **kwargs) -> Any:
        compactness, labels, centers = cv2.kmeans(
            data, K, None, self._criteria, attempts, flags
        )
        return compactness, labels, centers

    def run(self, record):
        # Get input values
        inputs = [record.get(pin) for pin in self._input_pins]

        # Apply K-means
        compactness, labels, centers = self.apply_function(*inputs)

        # Set outputs
        record.set(self._compactness_output, compactness)
        record.set(self._labels_output, labels)
        record.set(self._centers_output, centers)
        return self.nonext()
