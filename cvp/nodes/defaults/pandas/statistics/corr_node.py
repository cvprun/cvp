# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.pandas._base import DataFrameMethodNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class CorrNode(DataFrameMethodNode):
    """Compute pairwise correlation of columns."""

    def __init__(self):
        method_pin = DataInputPin(
            name=PinName("method"),
            dtype=Dtype.any(),
            docs="Correlation method ('pearson', 'kendall', 'spearman')",
            required=False,
        )
        min_periods_pin = DataInputPin(
            name=PinName("min_periods"),
            dtype=Dtype.any(),
            docs="Minimum number of observations required per pair (optional)",
            required=False,
        )
        super().__init__("corr", method_pin, min_periods_pin)

    def apply_method(self, df: pd.DataFrame, *args) -> Any:
        kwargs: Dict[str, Any] = {}

        if len(args) > 0 and args[0] is not None:
            kwargs["method"] = args[0]

        if len(args) > 1 and args[1] is not None:
            kwargs["min_periods"] = args[1]

        return df.corr(**kwargs)
