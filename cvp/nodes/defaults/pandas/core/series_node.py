# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName


class SeriesNode(Node):
    """Create a Series from data."""

    def __init__(self):
        self._data_pin = DataInputPin(
            name=PinName("data"),
            dtype=Dtype.any(),
            docs="Data to create Series from (array-like)",
        )
        self._index_pin = DataInputPin(
            name=PinName("index"),
            dtype=Dtype.any(),
            docs="Index for the Series (optional)",
            required=False,
        )
        self._name_pin = DataInputPin(
            name=PinName("name"),
            dtype=Dtype.any(),
            docs="Name for the Series (optional)",
            required=False,
        )
        self._output = DataOutputPin(
            name=PinName("series"),
            dtype=Dtype.any(),
            docs="Created Series",
        )
        super().__init__(self._data_pin, self._index_pin, self._name_pin, self._output)

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
            name = record.get(self._name_pin)
            if name is not None:
                kwargs["name"] = name
        except KeyError:
            pass

        series = pd.Series(**kwargs)
        record.set(self._output, series)
        return self.nonext()
