# -*- coding: utf-8 -*-

from dataclasses import is_dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum
from inspect import isclass, ismodule
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Type

from numpy import ndarray

from cvp.types.matcher.interface import TypesMatcherInterface

TypesMatcherCallable = Callable[[Any, Any], Any]
TypesMatcherDict = Dict[Type, TypesMatcherCallable]


class TypesMatcherMapper(TypesMatcherDict):
    def __init__(
        self,
        callback: TypesMatcherInterface,
        matchers: Optional[TypesMatcherDict] = None,
    ):
        super().__init__(matchers if matchers else {})
        self._callback = callback

    @classmethod
    def from_default(cls, callback: TypesMatcherInterface):
        return cls(
            callback=callback,
            matchers={
                type(None): callback.on_none_data,
                bytes: callback.on_bytes_data,
                bytearray: callback.on_bytearray_data,
                memoryview: callback.on_memoryview_data,
                complex: callback.on_complex_data,
                float: callback.on_float_data,
                int: callback.on_int_data,
                bool: callback.on_bool_data,
                str: callback.on_str_data,
                tuple: callback.on_tuple_data,
                set: callback.on_set_data,
                list: callback.on_list_data,
                dict: callback.on_dict_data,
                ndarray: callback.on_ndarray_data,
                datetime: callback.on_datetime_data,
                date: callback.on_date_data,
                time: callback.on_time_data,
                timedelta: callback.on_timedelta_data,
            },
        )

    def match_data(self, data: Any, extra=None) -> Any:
        if callback := self.get(type(data)):
            return callback(data, extra)

        match data:
            case None:
                return self._callback.on_none_data(data, extra)
            case bytes():
                return self._callback.on_bytes_data(data, extra)
            case bytearray():
                return self._callback.on_bytearray_data(data, extra)
            case memoryview():
                return self._callback.on_memoryview_data(data, extra)
            case complex():
                return self._callback.on_complex_data(data, extra)
            case float():
                return self._callback.on_float_data(data, extra)
            case int():
                return self._callback.on_int_data(data, extra)
            case bool():
                return self._callback.on_bool_data(data, extra)
            case str():
                return self._callback.on_str_data(data, extra)
            case tuple():
                return self._callback.on_tuple_data(data, extra)
            case set():
                return self._callback.on_set_data(data, extra)
            case list():
                return self._callback.on_list_data(data, extra)
            case dict():
                return self._callback.on_dict_data(data, extra)
            case ndarray():
                return self._callback.on_ndarray_data(data, extra)
            case datetime():
                return self._callback.on_datetime_data(data, extra)
            case date():
                return self._callback.on_date_data(data, extra)
            case time():
                return self._callback.on_time_data(data, extra)
            case timedelta():
                return self._callback.on_timedelta_data(data, extra)
            case Path():
                return self._callback.on_path_data(data, extra)
            case Enum():
                return self._callback.on_enum_data(data, extra)
            case x if isinstance(x, Mapping):
                return self._callback.on_mapping_data(x, extra)
            case x if isinstance(x, Iterable):
                return self._callback.on_iterable_data(x, extra)
            case x if is_dataclass(x):
                return self._callback.on_dataclass_data(x, extra)
            case x if ismodule(x):
                return self._callback.on_module_data(x, extra)
            case x if isclass(x):
                return self._callback.on_class_data(x, extra)
            case x:
                return self._callback.on_unknown_data(x, extra)

    def __call__(self, data: Any, extra=None) -> Any:
        return self.match_data(data, extra)
