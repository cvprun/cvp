# -*- coding: utf-8 -*-

from typing import Any, Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.record import NodeRecord
from cvp.nodes.template import NodeTemplate
from cvp.pins.datas import DataInputPinTemplate, DataOutputPinTemplate
from cvp.pins.template import PinTemplate
from cvp.types.override import override


class GetterNodeTemplate(NodeTemplate):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._key = DataInputPinTemplate(
            name="key",
            dtype=dtype_registry.get(str),
            docs="The key of the variable",
            required=True,
            hidden=True,
            default=None,
        )
        self._value = DataOutputPinTemplate(
            name="value",
            dtype=dtype_registry.get(Any),
            docs="The value of the variable",
        )
        super().__init__(
            name="getter",
            path="cvp.essential.getter",
            docs="Get a variable to a specific value",
            pins=(self._key, self._value),
            tags=("value", "variable", "getter", "accessor"),
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
        value = record.get_shared(key)
        record.set(self._value, value)
        return None
