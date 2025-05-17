# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Final, Iterable, Mapping, Optional, Union

from imgui_bundle import imgui
from numpy import ndarray

from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.table import TableFlags, merge_table_flags
from cvp.imgui.flags.table_column import WIDTH_FIXED, WIDTH_STRETCH, TableColumnFlags
from cvp.inspect.member import get_public_instance_attributes, is_instance_public_member
from cvp.patterns.singleton import singleton
from cvp.types.matcher.interface import TypesMatcherInterface
from cvp.types.matcher.mapper import TypesMatcherMapper
from cvp.types.override import override

DEFAULT_KEY_LABEL: Final[str] = "Key"
DEFAULT_TYPE_LABEL: Final[str] = "Type"
DEFAULT_SIZE_LABEL: Final[str] = "Size"
DEFAULT_VALUE_LABEL: Final[str] = "Value"

DEFAULT_MAX_DEPTH: Final[int] = 3
DEFAULT_MAX_ROWS: Final[int] = 20
DEFAULT_ROWS_PAGE: Final[int] = 10

DEFAULT_TABLE_FLAGS: Final[int] = merge_table_flags(
    TableFlags.sizing_fixed_fit,
    TableFlags.row_bg,
    TableFlags.borders,
    TableFlags.resizable,
    TableFlags.reorderable,
    TableFlags.hideable,
)


@dataclass
class TableAnyOptions:
    table_flags: Union[TableFlags, int] = DEFAULT_TABLE_FLAGS
    table_outer_size: Optional[imgui.ImVec2Like] = None
    table_inner_width: float = 0.0

    key_label: str = DEFAULT_KEY_LABEL
    key_flags: Union[TableColumnFlags, int] = WIDTH_FIXED
    key_init_width_or_weight: float = 0.0
    key_user_id: int = 0
    key_show: bool = True

    type_label: str = DEFAULT_TYPE_LABEL
    type_flags: Union[TableColumnFlags, int] = WIDTH_FIXED
    type_init_width_or_weight: float = 0.0
    type_user_id: int = 0
    type_show: bool = False

    size_label: str = DEFAULT_SIZE_LABEL
    size_flags: Union[TableColumnFlags, int] = WIDTH_FIXED
    size_init_width_or_weight: float = 0.0
    size_user_id: int = 0
    size_show: bool = False

    value_label: str = DEFAULT_VALUE_LABEL
    value_flags: Union[TableColumnFlags, int] = WIDTH_STRETCH
    value_init_width_or_weight: float = 0.0
    value_user_id: int = 0
    value_show: bool = True

    max_depth: int = DEFAULT_MAX_DEPTH
    max_rows: int = DEFAULT_MAX_ROWS
    rows_page: int = DEFAULT_ROWS_PAGE

    table_rows: Dict[int, int] = field(default_factory=dict)

    @property
    def table_flags_integer(self) -> int:
        if isinstance(self.table_flags, TableFlags):
            return int(self.table_flags)
        else:
            assert isinstance(self.table_flags, int)
            return self.table_flags

    @property
    def key_flags_integer(self) -> int:
        if isinstance(self.key_flags, TableColumnFlags):
            return int(self.key_flags)
        else:
            assert isinstance(self.key_flags, int)
            return self.key_flags

    @property
    def type_flags_integer(self) -> int:
        if isinstance(self.type_flags, TableColumnFlags):
            return int(self.type_flags)
        else:
            assert isinstance(self.type_flags, int)
            return self.type_flags

    @property
    def size_flags_integer(self) -> int:
        if isinstance(self.size_flags, TableColumnFlags):
            return int(self.size_flags)
        else:
            assert isinstance(self.size_flags, int)
            return self.size_flags

    @property
    def value_flags_integer(self) -> int:
        if isinstance(self.value_flags, TableColumnFlags):
            return int(self.value_flags)
        else:
            assert isinstance(self.value_flags, int)
            return self.value_flags

    @property
    def table_columns(self) -> int:
        return (
            self.key_show,
            self.type_show,
            self.size_show,
            self.value_show,
        ).count(True)

    def begin_table(self, label: str) -> bool:
        return imgui.begin_table(
            label,
            self.table_columns,
            self.table_flags_integer,
            self.table_outer_size,
            self.table_inner_width,
        )

    def table_setup_column_key(self) -> None:
        if not self.key_show:
            raise ValueError("Table column 'key' is hidden")

        imgui.table_setup_column(
            self.key_label,
            self.key_flags_integer,
            self.key_init_width_or_weight,
            self.key_user_id,
        )

    def table_setup_column_type(self) -> None:
        if not self.type_show:
            raise ValueError("Table column 'type' is hidden")

        imgui.table_setup_column(
            self.type_label,
            self.type_flags_integer,
            self.type_init_width_or_weight,
            self.type_user_id,
        )

    def table_setup_column_size(self) -> None:
        if not self.size_show:
            raise ValueError("Table column 'size' is hidden")

        imgui.table_setup_column(
            self.size_label,
            self.size_flags_integer,
            self.size_init_width_or_weight,
            self.size_user_id,
        )

    def table_setup_column_value(self) -> None:
        if not self.value_show:
            raise ValueError("Table column 'value' is hidden")

        imgui.table_setup_column(
            self.value_label,
            self.value_flags_integer,
            self.value_init_width_or_weight,
            self.value_user_id,
        )


class TableAny(TypesMatcherInterface):
    def __init__(self, label: str, options: Optional[TableAnyOptions] = None):
        self._label = label
        self._options = options if options else TableAnyOptions()
        self._mapper = TypesMatcherMapper.from_default(self)

    @override
    def on_none_data(self, data: None, extra: Any):
        imgui.text("None")

    @override
    def on_bytes_data(self, data: bytes, extra: Any):
        imgui.input_text(f"##{self.on_bytes_data.__name__}", str(data))

    @override
    def on_bytearray_data(self, data: bytearray, extra: Any):
        imgui.input_text(f"##{self.on_bytearray_data.__name__}", str(data))

    @override
    def on_memoryview_data(self, data: memoryview, extra: Any):
        imgui.input_text(f"##{self.on_memoryview_data.__name__}", str(data))

    @override
    def on_complex_data(self, data: complex, extra: Any):
        imgui.input_text(f"##{self.on_complex_data.__name__}", str(data))

    @override
    def on_float_data(self, data: float, extra: Any):
        imgui.input_text(f"##{self.on_float_data.__name__}", str(data))

    @override
    def on_int_data(self, data: int, extra: Any):
        imgui.input_text(f"##{self.on_int_data.__name__}", str(data))

    @override
    def on_bool_data(self, data: bool, extra: Any):
        imgui.input_text(f"##{self.on_bool_data.__name__}", str(data))

    @override
    def on_str_data(self, data: str, extra: Any):
        imgui.input_text(f"##{self.on_str_data.__name__}", data)

    @override
    def on_tuple_data(self, data: tuple, extra: Any):
        self._table_attributes(f"##{self.on_tuple_data.__name__}", data, extra)

    @override
    def on_set_data(self, data: set, extra: Any):
        self._table_attributes(f"##{self.on_set_data.__name__}", data, extra)

    @override
    def on_list_data(self, data: list, extra: Any):
        self._table_attributes(f"##{self.on_list_data.__name__}", data, extra)

    @override
    def on_dict_data(self, data: dict, extra: Any):
        self._table_attributes(f"##{self.on_dict_data.__name__}", data, extra)

    @override
    def on_ndarray_data(self, data: ndarray, extra: Any):
        imgui.input_text(f"##{self.on_ndarray_data.__name__}", f"{data.shape}")

    @override
    def on_datetime_data(self, data: datetime, extra: Any):
        imgui.input_text(
            f"##{self.on_datetime_data.__name__}",
            f"{data:%Y-%m-%d %H-%M-%S}",
        )

    @override
    def on_date_data(self, data: date, extra: Any):
        imgui.input_text(f"##{self.on_date_data.__name__}", f"{data:%Y-%m-%d}")

    @override
    def on_time_data(self, data: time, extra: Any):
        imgui.input_text(f"##{self.on_time_data.__name__}", f"{data:%H-%M-%S}")

    @override
    def on_timedelta_data(self, data: timedelta, extra: Any):
        imgui.input_text(
            f"##{self.on_timedelta_data.__name__}",
            f"{data.total_seconds():.03f}s",
        )

    @override
    def on_path_data(self, data: Path, extra: Any):
        imgui.input_text(f"##{self.on_path_data.__name__}", str(data))

    @override
    def on_enum_data(self, data: Enum, extra: Any):
        self._table_attributes(f"##{self.on_enum_data.__name__}", type(data), extra)

    @override
    def on_mapping_data(self, data: Mapping, extra: Any):
        self._table_attributes(f"##{self.on_mapping_data.__name__}", data, extra)

    @override
    def on_iterable_data(self, data: Iterable, extra: Any):
        self._table_attributes(f"##{self.on_iterable_data.__name__}", data, extra)

    @override
    def on_dataclass_data(self, data: Any, extra: Any):
        self._table_attributes(f"##{self.on_dataclass_data.__name__}", data, extra)

    @override
    def on_module_data(self, data: ModuleType, extra: Any):
        self._table_attributes(f"##{self.on_module_data.__name__}", data, extra)

    @override
    def on_class_data(self, data: Any, extra: Any):
        self._table_attributes(f"##{self.on_class_data.__name__}", data, extra)

    @override
    def on_unknown_data(self, data: Any, extra: Any):
        self._table_attributes(f"##{self.on_unknown_data.__name__}", data, extra)

    def _table_attributes(self, label: str, data: Any, depth: int) -> None:
        if depth <= 0:
            imgui.text(str(data))
            return

        if self._options.begin_table(label):
            show_more_button = False
            try:
                if self._options.key_show:
                    self._options.table_setup_column_key()
                if self._options.type_show:
                    self._options.table_setup_column_type()
                if self._options.size_show:
                    self._options.table_setup_column_size()
                if self._options.value_show:
                    self._options.table_setup_column_value()
                imgui.table_headers_row()

                table_id = imgui.get_item_id()
                max_rows = self._options.table_rows.get(table_id)
                if max_rows is None:
                    self._options.table_rows[table_id] = self._options.max_rows
                    max_rows = self._options.max_rows
                assert isinstance(max_rows, int)

                for i, item in enumerate(get_public_instance_attributes(data)):
                    if max_rows <= i:
                        show_more_button = True
                        break

                    key, value = item
                    if not is_instance_public_member(data, key):
                        continue

                    imgui.table_next_row()

                    column_index = 0
                    if self._options.key_show:
                        imgui.table_set_column_index(column_index)
                        imgui.text(key)
                        column_index += 1

                    if self._options.type_show:
                        imgui.table_set_column_index(column_index)
                        imgui.text(type(value).__name__)
                        column_index += 1

                    if self._options.size_show:
                        imgui.table_set_column_index(column_index)
                        try:
                            imgui.text(str(len(value)))
                        except TypeError:
                            pass
                        column_index += 1

                    if self._options.value_show:
                        imgui.table_set_column_index(column_index)
                        imgui.push_id(key)
                        try:
                            imgui.set_next_item_width(FIT_WIDTH)
                            self._mapper.match_data(value, depth - 1)
                        finally:
                            imgui.pop_id()
                        column_index += 1
            finally:
                imgui.end_table()

            if show_more_button:
                assert table_id is not None
                if imgui.button("More rows"):
                    self._options.table_rows[table_id] += self._options.rows_page

    def do_process(self, data: Any) -> Any:
        return self._mapper.match_data(data, self._options.max_depth)


@singleton
class GlobalTableAnyOptions(Dict[int, TableAnyOptions]):
    pass


def table_any(label: str, data: Any, options: Optional[TableAnyOptions] = None) -> None:
    if options is None:
        global_options = GlobalTableAnyOptions()
        next_id = imgui.get_id(label)
        options = global_options.get(next_id)
        if options is None:
            options = TableAnyOptions()
            global_options.__setitem__(next_id, options)

    assert options is not None
    TableAny(label, options).do_process(data)
