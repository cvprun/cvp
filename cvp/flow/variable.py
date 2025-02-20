# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from pickle import dumps, loads
from typing import Any, Dict, Optional

from type_serialize import Serializable

from cvp.memory.copy import copy_flexible
from cvp.patterns.proxy import ValueProxy, ValueT
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


class FlowVariable(ValueProxy[ValueT], Serializable):
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

        self._selected = False
        self._hovering = False

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = copy(self.name)
        result.dtype = copy(self.dtype)
        result.docs = copy(self.docs)
        result._value = copy(self._value)
        result._initial = copy(self._initial)
        result.persistent = copy(self.persistent)
        result.use_copy = copy(self.use_copy)
        result.use_deepcopy = copy(self.use_deepcopy)
        result._selected = copy(self._selected)
        result._hovering = copy(self._hovering)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = deepcopy(self.name, memo)
        result.dtype = deepcopy(self.dtype, memo)
        result.docs = deepcopy(self.docs, memo)
        result._value = deepcopy(self._value, memo)
        result._initial = deepcopy(self._initial, memo)
        result.persistent = deepcopy(self.persistent, memo)
        result.use_copy = deepcopy(self.use_copy, memo)
        result.use_deepcopy = deepcopy(self.use_deepcopy, memo)
        result._selected = deepcopy(self._selected, memo)
        result._hovering = deepcopy(self._hovering, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        result = {
            self.Keys.name_: self.name,
            self.Keys.dtype: self.dtype,
            self.Keys.docs: self.docs,
            self.Keys.value_: dumps(self._value),
            self.Keys.initial: dumps(self._initial),
            self.Keys.persistent: self.persistent,
            self.Keys.use_copy: self.use_copy,
            self.Keys.use_deepcopy: self.use_deepcopy,
        }
        return {str(key): val for key, val in result.items()}

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

    @override
    def get(self) -> ValueT:
        return self._value

    @override
    def set(self, value: ValueT) -> None:
        self._value = value

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

    def as_unformatted_text(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"Docs: {self.docs}\n"
            f"Data Type: {self.dtype}\n"
            f"Value: {str(self._value)}\n"
            f"Initial: {str(self._initial)}\n"
            f"Persistent: {self.persistent}\n"
            f"Copy: {self.use_copy}\n"
            f"Deepcopy: {self.use_deepcopy}\n"
            f"Selected: {self._selected}\n"
            f"Hovering: {self._hovering}\n"
        )

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value

    @property
    def hovering(self):
        return self._hovering

    @hovering.setter
    def hovering(self, value: bool) -> None:
        self._hovering = value
