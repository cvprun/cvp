# -*- coding: utf-8 -*-

from typing import Dict

from cvp.flow.datas.templates.dtype import Dtype
from cvp.flow.dtypes.builtin import builtin_dtypes
from cvp.flow.dtypes.registry import global_dtype_registry


class FlowDtypes:
    _dtypes: Dict[str, Dtype]

    def __init__(self, *, no_builtins=False, no_global_register=False):
        self._dtypes = dict()
        if not no_builtins:
            self._dtypes.update(builtin_dtypes())
        if not no_global_register:
            self._dtypes.update(global_dtype_registry())

    def __getitem__(self, path: str) -> Dtype:
        return self._dtypes.__getitem__(path)

    def __setitem__(self, path: str, value: Dtype) -> None:
        self._dtypes.__setitem__(path, value)

    def __contains__(self, path: str) -> bool:
        return self._dtypes.__contains__(path)

    def __len__(self) -> int:
        return self._dtypes.__len__()

    def __bool__(self) -> bool:
        return bool(self._dtypes)

    def keys(self):
        return self._dtypes.keys()

    def values(self):
        return self._dtypes.values()

    def items(self):
        return self._dtypes.items()
