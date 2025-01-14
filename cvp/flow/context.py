# -*- coding: utf-8 -*-

from types import TracebackType
from typing import Any, Dict, Optional, Tuple, Type, Union

from cvp.flow.envs import FlowEnvs

ExceptionInfo = Tuple[Type[BaseException], BaseException, TracebackType]
NullInfo = Tuple[None, None, None]


class FlowContext:
    _envs: FlowEnvs
    _args: Tuple[Any, ...]
    _kwargs: Dict[str, Any]
    _result: Any
    _exc_info: Optional[ExceptionInfo]

    def __init__(self, __flow_envs__: FlowEnvs, /, *args, **kwargs):
        self._envs = __flow_envs__
        self._args = args
        self._kwargs = kwargs
        self._result = None
        self._exc_info = None

    @property
    def envs(self):
        return self._envs

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def result(self):
        return self._result

    @property
    def exc_info(self):
        return self._exc_info

    def set_result(self, value: Any) -> None:
        self._result = value
        self._exc_info = None

    def set_exception(self, value: Union[ExceptionInfo, NullInfo]) -> None:
        assert value[0] is not None
        assert value[1] is not None
        assert value[2] is not None
        self._result = None
        self._exc_info = value
