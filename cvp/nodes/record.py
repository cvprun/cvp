# -*- coding: utf-8 -*-

from types import TracebackType
from typing import Any, Dict, Optional, Tuple, Type, Union

from cvp.pins.pin import Pin

ExceptionInfo = Tuple[Type[BaseException], BaseException, TracebackType]
NullInfo = Tuple[None, None, None]


class NodeRecord:
    _inputs: Dict[str, Any]
    _outputs: Dict[str, Any]

    _args: Tuple[Any, ...]
    _kwargs: Dict[str, Any]

    _result: Any
    _exception: Optional[ExceptionInfo]

    def __init__(self, *args, **kwargs):
        self._inputs = dict()
        self._outputs = dict()
        self._args = args
        self._kwargs = kwargs
        self._result = None
        self._exception = None

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value: Any) -> None:
        self._result = value
        self._exception = None

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value: Union[ExceptionInfo, NullInfo]) -> None:
        assert value[0] is not None
        assert value[1] is not None
        assert value[2] is not None
        self._result = None
        self._exception = value

    @property
    def exc_type(self) -> Type[BaseException]:
        assert self._exception is not None
        return self._exception[0]

    @property
    def exc_info(self) -> BaseException:
        assert self._exception is not None
        return self._exception[1]

    @property
    def exc_tb(self) -> TracebackType:
        assert self._exception is not None
        return self._exception[2]

    def clear(self) -> None:
        self._result = None
        self._exception = None

    def get(self, key: Pin) -> Any:
        return self._inputs[key.name]

    def set(self, key: Pin, value: Any) -> None:
        self._outputs[key.name] = value
