# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import DataFrameMethodNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class DescribeNode(DataFrameMethodNode):
    """Generate descriptive statistics of DataFrame."""

    def __init__(self):
        include_pin = DataInputPin(
            name=PinName("include"),
            dtype=Dtype.any(),
            docs="Data types to include in result (optional)",
            required=False,
        )
        exclude_pin = DataInputPin(
            name=PinName("exclude"),
            dtype=Dtype.any(),
            docs="Data types to exclude from result (optional)",
            required=False,
        )
        super().__init__("describe", include_pin, exclude_pin)

    def apply_method(self, df: pd.DataFrame, *args) -> Any:
        kwargs: Dict[str, Any] = {}

        if len(args) > 0 and args[0] is not None:
            kwargs["include"] = args[0]

        if len(args) > 1 and args[1] is not None:
            kwargs["exclude"] = args[1]

        return df.describe(**kwargs)
