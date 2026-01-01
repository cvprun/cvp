# -*- coding: utf-8 -*-

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName


class FilterNode(Node):
    """Filter DataFrame rows based on boolean condition."""

    def __init__(self):
        self._dataframe_pin = DataInputPin(
            name=PinName("dataframe"),
            dtype=Dtype.any(),
            docs="Input DataFrame",
        )
        self._condition_pin = DataInputPin(
            name=PinName("condition"),
            dtype=Dtype.any(),
            docs="Boolean condition for filtering rows",
        )
        self._output = DataOutputPin(
            name=PinName("result"),
            dtype=Dtype.any(),
            docs="Filtered DataFrame",
        )
        super().__init__(self._dataframe_pin, self._condition_pin, self._output)

    def run(self, record: NodeRecord) -> Pin:
        df = record.get(self._dataframe_pin)
        condition = record.get(self._condition_pin)

        result = df[condition]
        record.set(self._output, result)
        return self.nonext()
