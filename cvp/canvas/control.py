# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ViewControl:
    pan_x: float = 0.0
    pan_y: float = 0.0
    zoom: float = 1.0
