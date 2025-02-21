# -*- coding: utf-8 -*-

from collections import deque
from copy import deepcopy
from inspect import signature
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    SupportsIndex,
    TypeVar,
    Union,
)

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class MappingDeque(Generic[_KT, _VT]):
    _deque: Deque[_VT]
    _mapping: Dict[_KT, _VT]

    def __init__(
        self,
        items: Optional[Iterable[_VT]] = None,
        *,
        keyable: Optional[Callable[[_VT], _KT]] = None,
    ):
        if keyable is not None:
            sig = signature(keyable)
            if self.is_indexable_key(sig.return_annotation):
                raise TypeError("The 'keyable' argument must not be indexable")
        else:
            keyable = self.default_keyable

        self._keyable = keyable
        self._deque = deque(items) if items else deque()
        self._mapping = dict()
        for child in self._deque:
            self._mapping[self._keyable(child)] = child
        assert len(self._deque) == len(self._mapping)

    @staticmethod
    def default_keyable(value):
        return str(value)

    @staticmethod
    def is_indexable_key(key: Any) -> bool:
        return hasattr(key, "__index__")

    @staticmethod
    def deque_index(index: SupportsIndex) -> int:
        if MappingDeque.is_indexable_key(index):
            return index.__index__()
        else:
            raise TypeError(f"Unsupported index type: {type(index).__name__}")

    @property
    def keyable(self):
        return self._keyable

    def mapping_key(self, value: _VT) -> _KT:
        return self._keyable(value)

    def as_list(self) -> List[_VT]:
        return list(self._deque)

    def as_dict(self) -> Dict[_KT, _VT]:
        return self._mapping.copy()

    def append(self, item: _VT) -> None:
        _k = self.mapping_key(item)
        if _k in self._mapping:
            raise KeyError(f"{_k} already exists")
        self._deque.append(item)
        self._mapping[_k] = item
        assert len(self._deque) == len(self._mapping)

    def appendleft(self, item: _VT) -> None:
        _k = self.mapping_key(item)
        if _k in self._mapping:
            raise KeyError(f"{_k} already exists")
        self._deque.appendleft(item)
        self._mapping[_k] = item
        assert len(self._deque) == len(self._mapping)

    def insert(self, index: SupportsIndex, item: _VT) -> None:
        _k = self.mapping_key(item)
        if _k in self._mapping:
            raise KeyError(f"{_k} already exists")
        _i = self.deque_index(index)
        self._deque.insert(_i, item)
        self._mapping[_k] = item
        assert len(self._deque) == len(self._mapping)

    def remove(self, value: _VT) -> None:
        self.remove_with_index(self._deque.index(value))

    def remove_with_index(self, index: SupportsIndex) -> _VT:
        _i = self.deque_index(index)
        item = self._deque[_i]
        _k = self.mapping_key(item)
        del self._deque[_i]
        del self._mapping[_k]
        assert len(self._deque) == len(self._mapping)
        return item

    def remove_with_key(self, key: _KT) -> _VT:
        item = self._mapping[key]
        self._deque.remove(item)
        del self._mapping[key]
        assert len(self._deque) == len(self._mapping)
        return item

    def pop(self, index: Optional[SupportsIndex] = None) -> _VT:
        if index is None:
            return self.popright()
        else:
            return self.popindex(index)

    def popindex(self, index: SupportsIndex) -> _VT:
        return self.remove_with_index(index)

    def popright(self) -> _VT:
        item = self._deque.pop()
        _k = self.mapping_key(item)
        del self._mapping[_k]
        assert len(self._deque) == len(self._mapping)
        return item

    def popleft(self) -> _VT:
        item = self._deque.popleft()
        _k = self.mapping_key(item)
        del self._mapping[_k]
        assert len(self._deque) == len(self._mapping)
        return item

    def count(self, item: _VT) -> int:
        return self._deque.count(item)

    def reverse(self) -> None:
        self._deque.reverse()

    def extend(self, items: Iterable[_VT]) -> None:
        for item in items:
            self.append(item)

    def extendleft(self, items: Iterable[_VT]) -> None:
        for item in items:
            self.appendleft(item)

    def rotate(self, n=1) -> None:
        self._deque.rotate(n)

    def index(self, value: _VT, start=0, stop: Optional[int] = None):
        if stop is not None:
            return self._deque.index(value, start, stop)
        else:
            return self._deque.index(value, start)

    def clear(self) -> None:
        self._deque.clear()
        self._mapping.clear()

    def copy(self):
        return type(self)(
            items=self._deque.copy(),
            keyable=self._keyable,
        )

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        result = type(self)(
            items=deepcopy(self._deque, memo),
            keyable=deepcopy(self._keyable, memo),
        )
        memo[id(self)] = result
        return result

    def get(self, key: _KT, default=None) -> Optional[_VT]:
        if default is not None:
            return self._mapping.get(key, default)
        else:
            return self._mapping.get(key)

    def items(self):
        return self._mapping.items()

    def keys(self):
        return self._mapping.keys()

    def values(self):
        return self._mapping.values()

    def _update_unsafe(
        self,
        prev_index: SupportsIndex,
        prev_key: _KT,
        next_value: _VT,
    ) -> None:
        next_key = self.mapping_key(next_value)
        del self._mapping[prev_key]
        self._mapping[next_key] = next_value
        self._deque[prev_index] = next_value
        assert len(self._deque) == len(self._mapping)

    def update_with_index(self, key: SupportsIndex, value: _VT) -> _VT:
        prev_index = self.deque_index(key)
        if prev_index < 0 or len(self._deque) <= prev_index:
            raise IndexError("Deque index out of range")

        prev = self._deque[prev_index]
        prev_key = self.mapping_key(prev)
        assert self._mapping[prev_key] == prev

        self._update_unsafe(prev_index, prev_key, value)
        return prev

    def update_with_key_value(self, key: _KT, value: _VT) -> _VT:
        prev = self._mapping[key]
        prev_index = self._deque.index(prev)
        assert self._deque[prev_index] == prev

        self._update_unsafe(prev_index, key, value)
        return prev

    def update_with_value(self, value: _VT) -> _VT:
        return self.update_with_key_value(self.mapping_key(value), value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._deque.__eq__(other._deque)

    def __len__(self):
        return self._deque.__len__()

    def __contains__(self, key: _KT):
        return self._mapping.__contains__(key)

    def __getitem__(self, key: Union[SupportsIndex, _KT]) -> _VT:
        if self.is_indexable_key(key):
            _i = self.deque_index(key)  # type: ignore[arg-type]
            return self._deque.__getitem__(_i)
        else:
            _k = self.mapping_key(key)  # type: ignore[arg-type]
            return self._mapping.__getitem__(_k)

    def __setitem__(self, key: Union[SupportsIndex, _KT], value: _VT) -> None:
        if self.is_indexable_key(key):
            self.update_with_index(key, value)  # type: ignore[arg-type]
        else:
            self.update_with_key_value(key, value)  # type: ignore[arg-type]

    def __delitem__(self, key: Union[SupportsIndex, _KT]) -> None:
        if self.is_indexable_key(key):
            self.remove_with_index(key)  # type: ignore[arg-type]
        else:
            self.remove_with_key(key)  # type: ignore[arg-type]

    def __iter__(self):
        return self._deque.__iter__()

    def __reversed__(self):
        return self._deque.__reversed__()

    def __iadd__(self, other: Iterable[_VT]):
        self.extend(other)
        return self
