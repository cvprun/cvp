# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import DataFrameMethodNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class SortValuesNode(DataFrameMethodNode):
    """Sort DataFrame by values of specified column(s)."""

    def __init__(self):
        by_pin = DataInputPin(
            name=PinName("by"),
            dtype=Dtype.any(),
            docs="Column name(s) to sort by",
        )
        ascending_pin = DataInputPin(
            name=PinName("ascending"),
            dtype=Dtype.any(),
            docs="Sort ascending vs. descending (default=True)",
            required=False,
        )
        inplace_pin = DataInputPin(
            name=PinName("inplace"),
            dtype=Dtype.any(),
            docs="If True, perform operation in-place (default=False)",
            required=False,
        )
        super().__init__("sort_values", by_pin, ascending_pin, inplace_pin)

    def apply_method(self, df: pd.DataFrame, *args) -> Any:
        kwargs: Dict[str, Any] = {"by": args[0]}

        if len(args) > 1 and args[1] is not None:
            kwargs["ascending"] = args[1]

        if len(args) > 2 and args[2] is not None:
            kwargs["inplace"] = args[2]

        return df.sort_values(**kwargs)
