# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin

from cvp.dtypes.defaults import DEFAULT_PATH_TO_DTYPES, DEFAULT_TYPE_TO_DTYPES
from cvp.dtypes.defaults.typing import get_typing_any
from cvp.dtypes.dtype import Dtype
from cvp.fonts.types import IconCode
from cvp.modules.class_path import TypePath
from cvp.types.colors import RGBA


class DtypeRegistry:
    _path2dtypes: Dict[TypePath, Dtype]
    _type2dtypes: Dict[Type, Dtype]

    def __init__(self, *, no_defaults=False):
        self._path2dtypes = dict()
        self._type2dtypes = dict()

        if not no_defaults:
            self._path2dtypes.update(DEFAULT_PATH_TO_DTYPES)
            self._type2dtypes.update(DEFAULT_TYPE_TO_DTYPES)

        assert len(self._path2dtypes) == len(self._type2dtypes)

    @property
    def path2dtypes(self):
        return self._path2dtypes

    @property
    def type2dtypes(self):
        return self._type2dtypes

    @property
    def any_dtype(self) -> Dtype:
        dtype = self._type2dtypes.get(Any)  # type: ignore[call-overload]
        if dtype is not None:
            return dtype
        return get_typing_any()

    def path_keys(self):
        return self._path2dtypes.keys()

    def type_keys(self):
        return self._type2dtypes.keys()

    def path_values(self):
        return self._path2dtypes.values()

    def type_values(self):
        return self._type2dtypes.values()

    def path_items(self):
        return self._path2dtypes.items()

    def type_items(self):
        return self._type2dtypes.items()

    def clear(self) -> None:
        self._path2dtypes.clear()
        self._type2dtypes.clear()

    def update(self, other: "DtypeRegistry") -> None:
        self._path2dtypes.update(other.path2dtypes)
        self._type2dtypes.update(other.type2dtypes)

    def has(self, key) -> bool:
        if get_origin(key) == Union:
            return all(self.has(tp) for tp in get_args(key))
        elif key in (Parameter.empty, Any):
            return True
        elif isinstance(key, type):
            return key in self._type2dtypes
        elif isinstance(key, str):
            return key in self._path2dtypes
        else:
            raise TypeError(f"Unsupported key type: {type(key).__name__}")

    def get(self, key) -> Dtype:
        if get_origin(key) == Union:
            raise TypeError("Union key type is not supported")
        elif key in (Parameter.empty, Any):
            return self.any_dtype
        elif isinstance(key, type):
            return self._type2dtypes[key]
        elif isinstance(key, str):
            return self._path2dtypes[TypePath(key)]
        else:
            raise TypeError(f"Unsupported key type: {type(key).__name__}")

    def get_with_union(self, key) -> List[Dtype]:
        if get_origin(key) == Union:
            return [self.get(tp) for tp in get_args(key)]
        else:
            return [self.get(key)]

    def __len__(self) -> int:
        assert len(self._path2dtypes) == len(self._type2dtypes)
        return len(self._path2dtypes)

    def __contains__(self, key) -> bool:
        return self.has(key)

    def __getitem__(self, key) -> Dtype:
        return self.get(key)

    def add(self, dtype: Dtype) -> None:
        if dtype.path in self._path2dtypes:
            raise KeyError(f"Duplicate dtype path: {dtype.path}")

        assert dtype.path not in self._path2dtypes
        assert dtype.type not in self._type2dtypes

        self._path2dtypes[dtype.path] = dtype
        self._type2dtypes[dtype.type] = dtype

    def add_new(
        self,
        base: type,
        name: Optional[str] = None,
        path: Optional[TypePath] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
    ) -> Dtype:
        result = Dtype(base, name, path, docs, icon, color)
        self.add(result)
        return result

    def register(
        self,
        name: Optional[str] = None,
        path: Optional[TypePath] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
    ):
        def _decorator(base: type):
            self.add_new(base, name, path, docs, icon, color)
            return base

        return _decorator
