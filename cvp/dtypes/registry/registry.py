# -*- coding: utf-8 -*-

from typing import Any, Optional

from cvp.dtypes.defaults import DEFAULT_PATH_TO_DTYPES as _PATH_TO_DTYPES
from cvp.dtypes.defaults import DEFAULT_TYPE_TO_DTYPES as _TYPE_TO_DTYPES
from cvp.dtypes.dtype import Dtype
from cvp.types.colors import RGBA


class DtypeRegistry:
    def __init__(self, *, no_defaults=False):
        self._path2dtypes = dict(_PATH_TO_DTYPES.items() if not no_defaults else list())
        self._type2dtypes = dict(_TYPE_TO_DTYPES.items() if not no_defaults else list())
        assert len(self._path2dtypes) == len(self._type2dtypes)

    def __len__(self) -> int:
        assert len(self._path2dtypes) == len(self._type2dtypes)
        return len(self._path2dtypes)

    @property
    def path2dtypes(self):
        return self._path2dtypes

    @property
    def type2dtypes(self):
        return self._type2dtypes

    def get(self, key: Any) -> Dtype:
        if isinstance(key, type):
            return self._type2dtypes[key]
        elif isinstance(key, str):
            return self._path2dtypes[key]
        else:
            raise TypeError(f"Unsupported key type: {type(key).__name__}")

    def add(self, dtype: Dtype) -> None:
        if dtype.path in self._path2dtypes:
            raise KeyError(f"Duplicate dtype path: {dtype.path}")

        assert dtype.path not in self._path2dtypes
        assert dtype.base not in self._type2dtypes

        self._path2dtypes[dtype.path] = dtype
        self._type2dtypes[dtype.base] = dtype

    def add_new(
        self,
        base: type,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ) -> Dtype:
        result = Dtype(base, name, path, docs, icon, color)
        self.add(result)
        return result

    def register(
        self,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ):
        def _decorator(base: type):
            self.add_new(base, name, path, docs, icon, color)
            return base

        return _decorator
