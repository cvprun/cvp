# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import DataFrameMethodNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class GroupByNode(DataFrameMethodNode):
    """Group DataFrame using a mapper or by columns."""

    def __init__(self):
        by_pin = DataInputPin(
            name=PinName("by"),
            dtype=Dtype.any(),
            docs="Grouper or column name(s) to group by",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis to group by (0=index, 1=columns, default=0)",
            required=False,
        )
        sort_pin = DataInputPin(
            name=PinName("sort"),
            dtype=Dtype.any(),
            docs="Sort group keys (default=True)",
            required=False,
        )
        super().__init__("groupby", by_pin, axis_pin, sort_pin)

    def apply_method(self, df: pd.DataFrame, *args) -> Any:
        kwargs: Dict[str, Any] = {"by": args[0]}

        if len(args) > 1 and args[1] is not None:
            kwargs["axis"] = args[1]

        if len(args) > 2 and args[2] is not None:
            kwargs["sort"] = args[2]

        return df.groupby(**kwargs)
