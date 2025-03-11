# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, Optional

from type_serialize import Serializable, deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.raw_value import dumps, loads
from cvp.memory.copy import CopyMethod, copy_flexible
from cvp.patterns.proxy import ValueProxy, ValueT
from cvp.types.override import override


class FlowVariable(ValueProxy[ValueT], Serializable):

    @unique
    class _Keys(StrEnum):
        name_ = "name"
        dtype = auto()
        docs = auto()

        value_ = "value"
        initial = auto()

        persistent = auto()
        use_copy = auto()
        use_deepcopy = auto()

    _value: Any
    _initial: Any

    def __init__(
        self,
        name: str,
        dtype: Dtype,
        docs: Optional[str] = None,
        value: Any = None,
        initial: Any = None,
        *,
        persistent: bool = False,
        use_copy: bool = False,
        use_deepcopy: bool = False,
        selected=False,
        hovering=False,
    ):
        self.name = name
        self.dtype = dtype
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

        self._selected = selected
        self._hovering = hovering

    def __str__(self) -> str:
        """In `cvp.flow` module, this return value is used as a key value."""
        return self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.name == other.name
            and self.dtype == other.dtype
            and self.docs == other.docs
            and self._value == other._value
            and self._initial == other._initial
            and self.persistent == other.persistent
            and self.use_copy == other.use_copy
            and self.use_deepcopy == other.use_deepcopy
        )

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
            self._Keys.name_: self.name,
            self._Keys.dtype: serialize(self.dtype),
            self._Keys.docs: self.docs,
            self._Keys.value_: dumps(self._value),
            self._Keys.initial: dumps(self._initial),
            self._Keys.persistent: self.persistent,
            self._Keys.use_copy: self.use_copy,
            self._Keys.use_deepcopy: self.use_deepcopy,
        }
        return {str(key): val for key, val in result.items()}

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self._value = loads(data.get(self._Keys.value_, None))
        self._initial = loads(data.get(self._Keys.initial, None))

        name = data.get(self._Keys.name_)
        if not name:
            raise ValueError(f"The '{self._Keys.name_}' attribute is required")
        if not isinstance(name, str):
            raise TypeError(f"The '{self._Keys.name_}' attribute only allows str type")

        dtype = data.get(self._Keys.dtype)
        if not dtype:
            raise ValueError(f"The '{self._Keys.dtype}' attribute is required")

        self.name = name
        self.dtype = deserialize(dtype, Dtype)
        self.docs = data.get(self._Keys.docs, str())

        self.persistent = data.get(self._Keys.persistent, False)
        self.use_copy = data.get(self._Keys.use_copy, False)
        self.use_deepcopy = data.get(self._Keys.use_deepcopy, False)

        if self.use_copy and self.use_deepcopy:
            raise ValueError("use_copy and use_deepcopy cannot coexist")

        self._selected = False
        self._hovering = False

    @property
    def copy_method(self):
        if self.use_copy and self.use_deepcopy:
            raise ValueError("use_copy and use_deepcopy cannot coexist")

        if self.use_deepcopy:
            return CopyMethod.deepcopy  # noqa
        elif self.use_copy:
            return CopyMethod.copy  # noqa
        else:
            return CopyMethod.assign

    @property
    def is_assign_method(self) -> bool:
        return not self.use_copy and not self.use_deepcopy

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

    @property
    def initial(self):
        return self._initial

    @initial.setter
    def initial(self, initial: Any) -> None:
        self._initial = initial

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
