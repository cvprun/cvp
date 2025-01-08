# -*- coding: utf-8 -*-

from typing import Dict, Union

from cvp.flow.datas.templates.dtype import Dtype
from cvp.flow.dtypes.builtin import builtin_dtypes
from cvp.flow.dtypes.registry import global_registry
from cvp.flow.path import FlowPath


class FlowDtypes:
    _dtypes: Dict[FlowPath, Dtype]

    def __init__(self, *, no_builtins=False, no_global_register=False):
        self._dtypes = dict()
        if not no_builtins:
            self._dtypes.update(builtin_dtypes())
        if not no_global_register:
            self._dtypes.update(global_registry())

    @staticmethod
    def normalize_path(path: Union[str, FlowPath]) -> FlowPath:
        if isinstance(path, FlowPath):
            return path
        if isinstance(path, str):
            return FlowPath(path)
        raise TypeError(f"Unsupported path type: {type(path).__name__}")

    def __getitem__(self, path: Union[str, FlowPath]) -> Dtype:
        return self._dtypes.__getitem__(self.normalize_path(path))

    def __setitem__(self, path: Union[str, FlowPath], value: Dtype) -> None:
        self._dtypes.__setitem__(self.normalize_path(path), value)

    def __contains__(self, path: Union[str, FlowPath]) -> bool:
        return self._dtypes.__contains__(self.normalize_path(path))

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
