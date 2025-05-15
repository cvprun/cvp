# -*- coding: utf-8 -*-

import numpy as np


def calculate_iou(seg1: np.ndarray, seg2: np.ndarray) -> float:
    intersection_area = np.logical_and(seg1, seg2).sum()
    union_area = np.logical_or(seg1, seg2).sum()

    if union_area == 0:
        return 0.0

    return float(intersection_area / union_area)
