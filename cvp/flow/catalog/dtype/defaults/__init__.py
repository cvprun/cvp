# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.flow.catalog.dtype.defaults.numpy import NDArrayDtype
from cvp.flow.templates.dtype import Dtype


def get_default_dtypes() -> Sequence[Dtype]:
    return (NDArrayDtype(),)
