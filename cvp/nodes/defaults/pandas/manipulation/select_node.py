# -*- coding: utf-8 -*-

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName


class SelectNode(Node):
    """Select columns from DataFrame."""

    def __init__(self):
        self._dataframe_pin = DataInputPin(
            name=PinName("dataframe"),
            dtype=Dtype.any(),
            docs="Input DataFrame",
        )
        self._columns_pin = DataInputPin(
            name=PinName("columns"),
            dtype=Dtype.any(),
            docs="Column name(s) to select",
        )
        self._output = DataOutputPin(
            name=PinName("result"),
            dtype=Dtype.any(),
            docs="Selected columns as DataFrame or Series",
        )
        super().__init__(self._dataframe_pin, self._columns_pin, self._output)

    def run(self, record: NodeRecord) -> Pin:
        df = record.get(self._dataframe_pin)
        columns = record.get(self._columns_pin)

        result = df[columns]
        record.set(self._output, result)
        return self.nonext()
