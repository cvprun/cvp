# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import DataFrameMethodNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class DropNode(DataFrameMethodNode):
    """Drop specified labels from rows or columns."""

    def __init__(self):
        labels_pin = DataInputPin(
            name=PinName("labels"),
            dtype=Dtype.any(),
            docs="Index or column labels to drop",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis to drop from (0='index', 1='columns', default=0)",
            required=False,
        )
        inplace_pin = DataInputPin(
            name=PinName("inplace"),
            dtype=Dtype.any(),
            docs="If True, do operation inplace (default=False)",
            required=False,
        )
        super().__init__("drop", labels_pin, axis_pin, inplace_pin)

    def apply_method(self, df: pd.DataFrame, *args) -> Any:
        kwargs: Dict[str, Any] = {"labels": args[0]}

        if len(args) > 1 and args[1] is not None:
            kwargs["axis"] = args[1]

        if len(args) > 2 and args[2] is not None:
            kwargs["inplace"] = args[2]

        return df.drop(**kwargs)
