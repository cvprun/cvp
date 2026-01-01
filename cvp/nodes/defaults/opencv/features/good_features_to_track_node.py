# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class GoodFeaturesToTrackNode(OpenCVFunctionNode):
    """Detect corners using Shi-Tomasi corner detection algorithm."""

    def __init__(self):
        image_pin = DataInputPin(
            name=PinName("image"),
            dtype=Dtype.any(),
            docs="Source grayscale image",
        )
        maxcorners_pin = DataInputPin(
            name=PinName("maxCorners"),
            dtype=Dtype(int),
            docs="Maximum number of corners to return",
            default=100,
        )
        qualitylevel_pin = DataInputPin(
            name=PinName("qualityLevel"),
            dtype=Dtype(float),
            docs="Minimal accepted quality of image corners",
            default=0.01,
        )
        mindistance_pin = DataInputPin(
            name=PinName("minDistance"),
            dtype=Dtype(float),
            docs="Minimum possible Euclidean distance between corners",
            default=10.0,
        )
        mask_pin = DataInputPin(
            name=PinName("mask"),
            dtype=Dtype.any(),
            docs="Optional region mask",
            default=None,
        )
        blocksize_pin = DataInputPin(
            name=PinName("blockSize"),
            dtype=Dtype(int),
            docs="Size of averaging block for gradient computation",
            default=3,
        )
        useharis_pin = DataInputPin(
            name=PinName("useHarrisDetector"),
            dtype=Dtype(bool),
            docs="Use Harris corner detector",
            default=False,
        )
        k_pin = DataInputPin(
            name=PinName("k"),
            dtype=Dtype(float),
            docs="Harris corner detector free parameter",
            default=0.04,
        )
        super().__init__(
            "goodFeaturesToTrack",
            image_pin,
            maxcorners_pin,
            qualitylevel_pin,
            mindistance_pin,
            mask_pin,
            blocksize_pin,
            useharis_pin,
            k_pin,
        )

    def apply_function(
        self,
        image,
        maxCorners,
        qualityLevel,
        minDistance,
        mask,
        blockSize,
        useHarrisDetector,
        k,
        **kwargs
    ) -> Any:
        return cv2.goodFeaturesToTrack(
            image,
            maxCorners,
            qualityLevel,
            minDistance,
            mask=mask,
            blockSize=blockSize,
            useHarrisDetector=useHarrisDetector,
            k=k,
        )
