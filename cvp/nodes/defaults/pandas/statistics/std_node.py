# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import DataFrameMethodNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class StdNode(DataFrameMethodNode):
    """Calculate standard deviation of DataFrame values."""

    def __init__(self):
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to calculate std (0=index, 1=columns, default=0)",
            required=False,
        )
        skipna_pin = DataInputPin(
            name=PinName("skipna"),
            dtype=Dtype.any(),
            docs="Exclude NA/null values (default=True)",
            required=False,
        )
        ddof_pin = DataInputPin(
            name=PinName("ddof"),
            dtype=Dtype.any(),
            docs="Delta degrees of freedom (default=1)",
            required=False,
        )
        super().__init__("std", axis_pin, skipna_pin, ddof_pin)

    def apply_method(self, df: pd.DataFrame, *args) -> Any:
        kwargs: Dict[str, Any] = {}

        if len(args) > 0 and args[0] is not None:
            kwargs["axis"] = args[0]

        if len(args) > 1 and args[1] is not None:
            kwargs["skipna"] = args[1]

        if len(args) > 2 and args[2] is not None:
            kwargs["ddof"] = args[2]

        return df.std(**kwargs)
