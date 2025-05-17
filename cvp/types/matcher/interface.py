# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable, Mapping

from numpy import ndarray


class TypesMatcherInterface(ABC):
    @abstractmethod
    def on_none_data(self, data: None, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_bytes_data(self, data: bytes, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_bytearray_data(self, data: bytearray, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_memoryview_data(self, data: memoryview, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_complex_data(self, data: complex, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_float_data(self, data: float, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_int_data(self, data: int, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_bool_data(self, data: bool, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_str_data(self, data: str, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_tuple_data(self, data: tuple, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_set_data(self, data: set, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_list_data(self, data: list, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_dict_data(self, data: dict, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_ndarray_data(self, data: ndarray, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_datetime_data(self, data: datetime, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_date_data(self, data: date, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_time_data(self, data: time, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_timedelta_data(self, data: timedelta, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_path_data(self, data: Path, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_enum_data(self, data: Enum, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_mapping_data(self, data: Mapping, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_iterable_data(self, data: Iterable, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_dataclass_data(self, data: Any, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_module_data(self, data: ModuleType, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_class_data(self, data: Any, extra: Any):
        raise NotImplementedError

    @abstractmethod
    def on_unknown_data(self, data: Any, extra: Any):
        raise NotImplementedError
