# -*- coding: utf-8 -*-

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName
from cvp.types.override import override


class Getter(Node):
    """Get a variable to a specific value"""

    def __init__(self):
        self._key = DataInputPin(
            name=PinName("key"),
            dtype=Dtype(str),
            docs="The key of the variable",
            required=True,
            hidden=True,
            default=None,
        )
        self._value = DataOutputPin(
            name=PinName("value"),
            dtype=Dtype.any(),
            docs="The value of the variable",
        )
        super().__init__(self._key, self._value)

    @property
    def key_name(self):
        return self._key.name

    @property
    def value_name(self):
        return self._value.name

    @override
    def run(self, record: NodeRecord) -> Pin:
        key = record.get(self._key)
        assert isinstance(key, str)
        value = record.get_shared(key)
        record.set(self._value, value)
        return self.nonext()
