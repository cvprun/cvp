# -*- coding: utf-8 -*-

from types import TracebackType
from typing import Any, Dict, Optional, Tuple, Type, Union

ExceptionInfo = Tuple[Type[BaseException], BaseException, TracebackType]
NullInfo = Tuple[None, None, None]


class NodeRecord:
    _args: Tuple[Any, ...]
    _kwargs: Dict[str, Any]
    _result: Any
    _exc_info: Optional[ExceptionInfo]

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._result = None
        self._exc_info = None

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    def get(self, key: str):
        return self._kwargs.get(key)

    @property
    def result(self):
        return self._result

    @property
    def exc_info(self):
        return self._exc_info

    def clear_result(self) -> None:
        self._result = None
        self._exc_info = None

    def set_result(self, value: Any) -> None:
        self._result = value
        self._exc_info = None

    def set_exception(self, value: Union[ExceptionInfo, NullInfo]) -> None:
        assert value[0] is not None
        assert value[1] is not None
        assert value[2] is not None
        self._result = None
        self._exc_info = value
