# -*- coding: utf-8 -*-

from numpy import ndarray

from cvp.flow.templates.dtype import Dtype


class NDArrayDtype(Dtype):
    def __init__(self):
        super().__init__(ndarray)
