# -*- coding: utf-8 -*-

from typing import Optional

from cvp.dtypes.dtype import Dtype
from cvp.nodes.record import NodeRecord
from cvp.nodes.template import NodeName, NodePath, NodeTemplate
from cvp.pins.datas import DataInputPinTemplate
from cvp.pins.special import NextPinTemplate, PrevPinTemplate
from cvp.pins.template import PinName, PinTemplate
from cvp.types.override import override


class SetterNodeTemplate(NodeTemplate):
    def __init__(self):
        self._prev = PrevPinTemplate()
        self._next = NextPinTemplate()
        self._key = DataInputPinTemplate(
            name=PinName("key"),
            dtype=Dtype(str),
            docs="The key of the variable",
            required=True,
            hidden=True,
            default=None,
        )
        self._value = DataInputPinTemplate(
            name=PinName("value"),
            dtype=Dtype.any(),
            docs="The value of the variable",
        )
        super().__init__(
            path=NodePath("cvp.essential.setter"),
            name=NodeName("Setter"),
            docs="Set a variable to a specific value",
            pins=(self._prev, self._next, self._key, self._value),
            tags=("value", "variable", "setter", "mutator"),
            hidden=True,
        )

    @property
    def key_name(self):
        return self._key.name

    @property
    def value_name(self):
        return self._value.name

    @override
    def run(self, record: NodeRecord) -> Optional[PinTemplate]:
        key = record.get(self._key)
        assert isinstance(key, str)
        value = record.get(self._value)
        record.set_shared(key, value)
        return self._next
