# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import SimplePandasFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class MergeNode(SimplePandasFunctionNode):
    """Merge DataFrame or named Series objects."""

    def __init__(self):
        left_pin = DataInputPin(
            name=PinName("left"),
            dtype=Dtype.any(),
            docs="Left DataFrame to merge",
        )
        right_pin = DataInputPin(
            name=PinName("right"),
            dtype=Dtype.any(),
            docs="Right DataFrame to merge",
        )
        on_pin = DataInputPin(
            name=PinName("on"),
            dtype=Dtype.any(),
            docs="Column name(s) to merge on (optional)",
            required=False,
        )
        how_pin = DataInputPin(
            name=PinName("how"),
            dtype=Dtype.any(),
            docs="Type of merge ('left', 'right', 'outer', 'inner') (default='inner')",
            required=False,
        )
        super().__init__("merge", left_pin, right_pin, on_pin, how_pin)

    def apply_function(self, *args) -> Any:
        kwargs: Dict[str, Any] = {
            "left": args[0],
            "right": args[1],
        }

        if len(args) > 2 and args[2] is not None:
            kwargs["on"] = args[2]

        if len(args) > 3 and args[3] is not None:
            kwargs["how"] = args[3]

        return pd.merge(**kwargs)
