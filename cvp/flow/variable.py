# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from pickle import dumps, loads
from typing import Any, Optional

from type_serialize import Serializable

from cvp.memory.copy import copy_flexible
from cvp.types.override import override


@unique
class FlowVariableKeys(StrEnum):
    name_ = "name"
    dtype = auto()
    docs = auto()

    value_ = "value"
    initial = auto()

    persistent = auto()
    use_copy = auto()
    use_deepcopy = auto()


class FlowVariable(Serializable):
    Keys = FlowVariableKeys

    _value: Any
    _initial: Any

    def __init__(
        self,
        name: Optional[str] = None,
        dtype: Optional[str] = None,
        docs: Optional[str] = None,
        value: Any = None,
        initial: Any = None,
        *,
        persistent: bool = False,
        use_copy: bool = False,
        use_deepcopy: bool = False,
    ):
        self.name = name if name else str()
        self.dtype = dtype if dtype else str()
        self.docs = docs if docs else str()

        self._value = value
        self._initial = copy_flexible(
            initial,
            use_copy=use_copy,
            use_deepcopy=use_deepcopy,
        )

        self.persistent = persistent
        self.use_copy = use_copy
        self.use_deepcopy = use_deepcopy

    @override
    def __serialize__(self) -> Any:
        return {
            self.Keys.name_: self.name,
            self.Keys.dtype: self.dtype,
            self.Keys.docs: self.docs,
            self.Keys.value_: dumps(self._value),
            self.Keys.initial: dumps(self._initial),
            self.Keys.persistent: self.persistent,
            self.Keys.use_copy: self.use_copy,
            self.Keys.use_deepcopy: self.use_deepcopy,
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        value = data.get(self.Keys.value_, None)
        if value is None:
            self._value = None
        elif isinstance(value, bytes):
            self._value = loads(value)
        else:
            raise TypeError(f"Unexpected value type: {type(value).__name__}")

        initial = data.get(self.Keys.initial, None)
        if initial is None:
            self._initial = None
        elif isinstance(initial, bytes):
            self._initial = loads(initial)
        else:
            raise TypeError(f"Unexpected initial type: {type(initial).__name__}")

        self.name = data.get(self.Keys.name_, str())
        self.dtype = data.get(self.Keys.dtype, str())
        self.docs = data.get(self.Keys.docs, str())

        self.persistent = data.get(self.Keys.persistent, False)
        self.use_copy = data.get(self.Keys.use_copy, False)
        self.use_deepcopy = data.get(self.Keys.use_deepcopy, False)

        if self.use_copy and self.use_deepcopy:
            raise ValueError("use_copy and use_deepcopy cannot coexist")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value

    def update_value_with_initial(self) -> None:
        self._value = copy_flexible(
            self._initial,
            use_copy=self.use_copy,
            use_deepcopy=self.use_deepcopy,
        )

    def update_initial_with_value(self) -> None:
        self._initial = copy_flexible(
            self._value,
            use_copy=self.use_copy,
            use_deepcopy=self.use_deepcopy,
        )
