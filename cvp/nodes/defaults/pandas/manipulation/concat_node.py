# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import SimplePandasFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ConcatNode(SimplePandasFunctionNode):
    """Concatenate pandas objects."""

    def __init__(self):
        objs_pin = DataInputPin(
            name=PinName("objs"),
            dtype=Dtype.any(),
            docs="List of pandas objects to concatenate",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis to concatenate along (default=0)",
            required=False,
        )
        ignore_index_pin = DataInputPin(
            name=PinName("ignore_index"),
            dtype=Dtype.any(),
            docs="If True, reset index (default=False)",
            required=False,
        )
        super().__init__("concat", objs_pin, axis_pin, ignore_index_pin)

    def apply_function(self, *args) -> Any:
        kwargs: Dict[str, Any] = {"objs": args[0]}

        if len(args) > 1 and args[1] is not None:
            kwargs["axis"] = args[1]

        if len(args) > 2 and args[2] is not None:
            kwargs["ignore_index"] = args[2]

        return pd.concat(**kwargs)
