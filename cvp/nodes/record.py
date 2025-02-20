# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from types import TracebackType
from typing import Any, Dict, Optional, Sequence, Tuple, Type, Union

from cvp.patterns.proxy import ValueProxy
from cvp.pins.pin import Pin

ExceptionInfo = Tuple[Type[BaseException], BaseException, TracebackType]
NullInfo = Tuple[None, None, None]


class NodeExecutionRecord:
    def __init__(
        self,
        index: int,
        node_uuid: str,
        variables: Dict[str, Any],
        args: Sequence[Any],
        kwargs: Dict[str, Any],
        result_key: Optional[str] = None,
        result: Any = None,
        exception: Optional[ExceptionInfo] = None,
        shared_variables: Optional[Dict[str, ValueProxy]] = None,
    ):
        self._index = index
        self._node_uuid = node_uuid
        self._variables = variables
        self._args = tuple(args)
        self._kwargs = kwargs
        self._begin = datetime.now()
        self._end = datetime.now()
        self._result_key = result_key if result_key else str()
        self._result = result
        self._exception = exception
        self._shared_variables = dict(shared_variables if shared_variables else dict())

    @property
    def index(self):
        return self._index

    @property
    def node_uuid(self):
        return self._node_uuid

    @property
    def variables(self):
        return self._variables

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def begin(self) -> datetime:
        return self._begin

    def set_begin_now(self) -> None:
        self._begin = datetime.now()

    @property
    def end(self) -> datetime:
        return self._end

    def set_end_now(self) -> None:
        self._end = datetime.now()

    @property
    def duration(self) -> timedelta:
        return self._end - self._begin

    @property
    def result_key(self) -> str:
        return self._result_key

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value: Any) -> None:
        self._result = value
        self._exception = None

    @property
    def has_exception(self) -> bool:
        return self._exception is not None

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
    def exc_val(self) -> BaseException:
        assert self._exception is not None
        return self._exception[1]

    @property
    def exc_tb(self) -> TracebackType:
        assert self._exception is not None
        return self._exception[2]

    def clear(self) -> None:
        self._result = None
        self._exception = None

    def get(self, key: Union[Pin, str]) -> Any:
        if isinstance(key, Pin):
            return self._variables[key.name]
        elif isinstance(key, str):
            return self._variables[key]
        else:
            raise TypeError(f"Unsupported key type: {type(key).__name__}")

    def set(self, key: Union[Pin, str], value: Any) -> None:
        if isinstance(key, Pin):
            self._variables[key.name] = value
        elif isinstance(key, str):
            self._variables[key] = value
        else:
            raise TypeError(f"Unsupported key type: {type(key).__name__}")

    def get_shared(self, key: str) -> Any:
        return self._shared_variables[key].get()

    def set_shared(self, key: str, value: Any) -> None:
        self._shared_variables[key].set(value)
