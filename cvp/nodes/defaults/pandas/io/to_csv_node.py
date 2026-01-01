# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import DataFrameMethodNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ToCsvNode(DataFrameMethodNode):
    """Write DataFrame to a CSV file."""

    def __init__(self):
        path_pin = DataInputPin(
            name=PinName("path_or_buf"),
            dtype=Dtype.any(),
            docs="File path or buffer to write to",
        )
        sep_pin = DataInputPin(
            name=PinName("sep"),
            dtype=Dtype.any(),
            docs="Field delimiter (default: ',')",
            required=False,
        )
        index_pin = DataInputPin(
            name=PinName("index"),
            dtype=Dtype.any(),
            docs="Write row names (index) (default: True)",
            required=False,
        )
        super().__init__("to_csv", path_pin, sep_pin, index_pin)

    def apply_method(self, df: pd.DataFrame, *args) -> Any:
        kwargs: Dict[str, Any] = {"path_or_buf": args[0]}

        if len(args) > 1 and args[1] is not None:
            kwargs["sep"] = args[1]

        if len(args) > 2 and args[2] is not None:
            kwargs["index"] = args[2]

        return df.to_csv(**kwargs)
