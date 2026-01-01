# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName


class DataFrameNode(Node):
    """Create a DataFrame from data."""

    def __init__(self):
        self._data_pin = DataInputPin(
            name=PinName("data"),
            dtype=Dtype.any(),
            docs="Data to create DataFrame from (dict, array, etc.)",
        )
        self._index_pin = DataInputPin(
            name=PinName("index"),
            dtype=Dtype.any(),
            docs="Index for the DataFrame (optional)",
            required=False,
        )
        self._columns_pin = DataInputPin(
            name=PinName("columns"),
            dtype=Dtype.any(),
            docs="Column labels for the DataFrame (optional)",
            required=False,
        )
        self._output = DataOutputPin(
            name=PinName("dataframe"),
            dtype=Dtype.any(),
            docs="Created DataFrame",
        )
        super().__init__(
            self._data_pin, self._index_pin, self._columns_pin, self._output
        )

    def run(self, record: NodeRecord) -> Pin:
        data = record.get(self._data_pin)

        kwargs: Dict[str, Any] = {"data": data}

        try:
            index = record.get(self._index_pin)
            if index is not None:
                kwargs["index"] = index
        except KeyError:
            pass

        try:
            columns = record.get(self._columns_pin)
            if columns is not None:
                kwargs["columns"] = columns
        except KeyError:
            pass

        df = pd.DataFrame(**kwargs)
        record.set(self._output, df)
        return self.nonext()
