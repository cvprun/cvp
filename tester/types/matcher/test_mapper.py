# -*- coding: utf-8 -*-

import os
from collections import OrderedDict, deque
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum, auto, unique
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable, Mapping
from unittest import TestCase, main

from numpy import ndarray, zeros

from cvp.resources.subdirs.temp import TempPath
from cvp.types.matcher.base import BaseTypesMatcher
from cvp.types.matcher.mapper import TypesMatcherMapper
from cvp.types.override import override


@unique
class _TestEnum(Enum):
    value1 = auto()
    value2 = auto()


@dataclass
class _TestDataClass:
    value1: str = field(default_factory=str)
    value2: str = field(default_factory=str)


class _TestClass:
    def __init__(self):
        pass


class _TestMapping(Mapping):
    def __iter__(self):
        pass

    def __len__(self):
        pass

    def __getitem__(self, __key):
        pass


class _TestIterable(Iterable):
    def __iter__(self):
        pass


class MapperTestCase(TestCase, BaseTypesMatcher):
    @override
    def on_none_data(self, data: None, extra: Any):
        return self.on_none_data.__name__

    @override
    def on_bytes_data(self, data: bytes, extra: Any):
        return self.on_bytes_data.__name__

    @override
    def on_bytearray_data(self, data: bytearray, extra: Any):
        return self.on_bytearray_data.__name__

    @override
    def on_memoryview_data(self, data: memoryview, extra: Any):
        return self.on_memoryview_data.__name__

    @override
    def on_complex_data(self, data: complex, extra: Any):
        return self.on_complex_data.__name__

    @override
    def on_float_data(self, data: float, extra: Any):
        return self.on_float_data.__name__

    @override
    def on_int_data(self, data: int, extra: Any):
        return self.on_int_data.__name__

    @override
    def on_bool_data(self, data: bool, extra: Any):
        return self.on_bool_data.__name__

    @override
    def on_str_data(self, data: str, extra: Any):
        return self.on_str_data.__name__

    @override
    def on_tuple_data(self, data: tuple, extra: Any):
        return self.on_tuple_data.__name__

    @override
    def on_set_data(self, data: set, extra: Any):
        return self.on_set_data.__name__

    @override
    def on_list_data(self, data: list, extra: Any):
        return self.on_list_data.__name__

    @override
    def on_dict_data(self, data: dict, extra: Any):
        return self.on_dict_data.__name__

    @override
    def on_ndarray_data(self, data: ndarray, extra: Any):
        return self.on_ndarray_data.__name__

    @override
    def on_datetime_data(self, data: datetime, extra: Any):
        return self.on_datetime_data.__name__

    @override
    def on_date_data(self, data: date, extra: Any):
        return self.on_date_data.__name__

    @override
    def on_time_data(self, data: time, extra: Any):
        return self.on_time_data.__name__

    @override
    def on_timedelta_data(self, data: timedelta, extra: Any):
        return self.on_timedelta_data.__name__

    @override
    def on_path_data(self, data: Path, extra: Any):
        return self.on_path_data.__name__

    @override
    def on_enum_data(self, data: Enum, extra: Any):
        return self.on_enum_data.__name__

    @override
    def on_mapping_data(self, data: Mapping, extra: Any):
        return self.on_mapping_data.__name__

    @override
    def on_iterable_data(self, data: Iterable, extra: Any):
        return self.on_iterable_data.__name__

    @override
    def on_dataclass_data(self, data: Any, extra: Any):
        return self.on_dataclass_data.__name__

    @override
    def on_module_data(self, data: ModuleType, extra: Any):
        return self.on_module_data.__name__

    @override
    def on_class_data(self, data: Any, extra: Any):
        return self.on_class_data.__name__

    @override
    def on_unknown_data(self, data: Any, extra: Any):
        return self.on_unknown_data.__name__

    def test_mapping(self):
        mapper = TypesMatcherMapper.from_default(self)
        self.assertEqual("on_none_data", mapper(None))
        self.assertEqual("on_bytes_data", mapper(b""))
        self.assertEqual("on_bytearray_data", mapper(bytearray(b"")))
        self.assertEqual("on_memoryview_data", mapper(memoryview(b"")))
        self.assertEqual("on_complex_data", mapper(2j))
        self.assertEqual("on_float_data", mapper(0.1))
        self.assertEqual("on_int_data", mapper(100))
        self.assertEqual("on_bool_data", mapper(True))
        self.assertEqual("on_str_data", mapper(""))
        self.assertEqual("on_tuple_data", mapper((1,)))
        self.assertEqual("on_set_data", mapper({1}))
        self.assertEqual("on_list_data", mapper([1]))
        self.assertEqual("on_dict_data", mapper({1: 0}))
        self.assertEqual("on_ndarray_data", mapper(zeros((1, 1))))
        self.assertEqual("on_datetime_data", mapper(datetime.now().astimezone()))
        self.assertEqual("on_date_data", mapper(date(2024, 10, 28)))
        self.assertEqual("on_time_data", mapper(time(13, 23, 49, 123)))
        self.assertEqual("on_timedelta_data", mapper(datetime.now() - datetime.now()))
        self.assertEqual("on_path_data", mapper(Path.home()))
        self.assertEqual("on_path_data", mapper(TempPath.home()))

        self.assertEqual("on_enum_data", mapper(_TestEnum.value2))
        self.assertEqual("on_dict_data", mapper(OrderedDict()))
        self.assertEqual("on_mapping_data", mapper(_TestMapping()))
        self.assertEqual("on_iterable_data", mapper(deque()))
        self.assertEqual("on_iterable_data", mapper(_TestIterable()))

        self.assertEqual("on_dataclass_data", mapper(_TestDataClass))
        self.assertEqual("on_dataclass_data", mapper(_TestDataClass()))

        self.assertEqual("on_module_data", mapper(os))
        self.assertEqual("on_class_data", mapper(_TestClass))
        self.assertEqual("on_unknown_data", mapper(_TestClass()))
        self.assertEqual("on_unknown_data", mapper(object()))
        self.assertEqual("on_unknown_data", mapper(sum))


if __name__ == "__main__":
    main()
