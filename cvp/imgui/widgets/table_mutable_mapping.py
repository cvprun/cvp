# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    Callable,
    Dict,
    Final,
    Generic,
    MutableMapping,
    NamedTuple,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from imgui_bundle import imgui

from cvp.assets.fonts.mdi import CHECK, CLOSE, DELETE, PLUS
from cvp.imgui.button import button
from cvp.imgui.calc_button_size import calc_button_size
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.style_var import ITEM_SPACING
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS, TableFlags
from cvp.imgui.flags.table_column import WIDTH_FIXED, WIDTH_STRETCH, TableColumnFlags
from cvp.imgui.input_float import input_float
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.patterns.singleton import singleton
from cvp.types.override import override

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

DEFAULT_KEY_LABEL: Final[str] = "Key"
DEFAULT_VALUE_LABEL: Final[str] = "Value"
DEFAULT_ACTIONS_LABEL: Final[str] = "Actions"


class TableMutableMappingResult(NamedTuple, Generic[_KT, _VT]):
    changed: bool
    key: _KT
    value: _VT

    def __bool__(self):
        return self.changed


@dataclass
class TableMutableMappingOptions:
    table_flags: Union[TableFlags, int] = DEFAULT_TABLE_FLAGS
    table_outer_size: Optional[imgui.ImVec2Like] = None
    table_inner_width: float = 0.0

    key_label: str = DEFAULT_KEY_LABEL
    key_flags: Union[TableColumnFlags, int] = WIDTH_STRETCH
    key_init_width_or_weight: float = 0.0
    key_user_id: int = 0
    key_show: bool = True

    value_label: str = DEFAULT_VALUE_LABEL
    value_flags: Union[TableColumnFlags, int] = WIDTH_STRETCH
    value_init_width_or_weight: float = 0.0
    value_user_id: int = 0
    value_show: bool = True

    actions_label: str = DEFAULT_ACTIONS_LABEL
    actions_flags: Union[TableColumnFlags, int] = WIDTH_FIXED
    actions_init_width_or_weight: Optional[float] = None
    actions_user_id: int = 0
    actions_show: bool = True
    action_button_spacing: float = 1.0

    removable: bool = True

    adding: bool = False
    temp_key: str = field(default_factory=str)
    temp_val: str = field(default_factory=str)

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
    def value_flags_integer(self) -> int:
        if isinstance(self.value_flags, TableColumnFlags):
            return int(self.value_flags)
        else:
            assert isinstance(self.value_flags, int)
            return self.value_flags

    @property
    def actions_flags_integer(self) -> int:
        if isinstance(self.actions_flags, TableColumnFlags):
            return int(self.actions_flags)
        else:
            assert isinstance(self.actions_flags, int)
            return self.actions_flags

    @property
    def table_columns(self) -> int:
        return (
            self.key_show,
            self.value_show,
            self.actions_show,
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

    def table_setup_column_value(self) -> None:
        if not self.value_show:
            raise ValueError("Table column 'value' is hidden")

        imgui.table_setup_column(
            self.value_label,
            self.value_flags_integer,
            self.value_init_width_or_weight,
            self.value_user_id,
        )

    def calc_actions_column_width(self) -> float:
        result = imgui.get_style().cell_padding.x * 2.0
        result += calc_button_size(PLUS).x
        result += self.action_button_spacing
        result += calc_button_size(CLOSE).x
        return result

    def table_setup_column_actions(self) -> None:
        if not self.actions_show:
            raise ValueError("Table column 'actions' is hidden")

        flags = self.actions_flags_integer
        init_width_or_weight = self.actions_init_width_or_weight

        if init_width_or_weight is None:
            if self.actions_flags_integer & WIDTH_FIXED:
                init_width_or_weight = self.calc_actions_column_width()
            else:
                init_width_or_weight = 0.0
        assert init_width_or_weight is not None

        imgui.table_setup_column(
            self.actions_label,
            flags,
            init_width_or_weight,
            self.actions_user_id,
        )


class TableMutableMappingInterface(Generic[_KT, _VT], ABC):
    @abstractmethod
    def on_input_value(self, key: _KT, value: _VT) -> TableMutableMappingResult:
        raise NotImplementedError


class TableMutableMapping(TableMutableMappingInterface[_KT, _VT]):
    def __init__(
        self,
        label: str,
        container: MutableMapping[_KT, _VT],
        options: Optional[TableMutableMappingOptions] = None,
        addable_factory: Optional[Callable[[str, str], Tuple[_KT, _VT]]] = None,
    ):
        self._label = label
        self._container = container
        self._addable_factory = addable_factory
        self._options = options if options else TableMutableMappingOptions()

    @property
    def options(self):
        return self._options

    @override
    def on_input_value(self, key: _KT, value: _VT) -> TableMutableMappingResult:
        changed = False

        imgui.set_next_item_width(FIT_WIDTH)
        if isinstance(value, str):
            if item_result := input_text(f"##Item.{key}", value):
                changed = True
                value = item_result.value
        elif isinstance(value, int):
            if item_result := input_int(f"##Item.{key}", value):
                changed = True
                value = item_result.value
        elif isinstance(value, float):
            if item_result := input_float(f"##Item.{key}", value):
                changed = True
                value = item_result.value
        else:
            imgui.text(str(value))
            item_typename = type(value).__name__
            hovered_tooltip_text(f"The {item_typename} class does not support editing")

        return TableMutableMappingResult(changed, key, value)

    def do_process(self) -> Optional[TableMutableMappingResult]:
        changed_result: Optional[TableMutableMappingResult] = None

        if self._options.begin_table(self._label):
            try:
                self._options.table_setup_column_key()
                self._options.table_setup_column_value()
                self._options.table_setup_column_actions()
                imgui.table_headers_row()

                remove_key: Optional[_KT] = None

                for key, value in self._container.items():
                    imgui.table_next_row()

                    imgui.table_set_column_index(0)
                    imgui.set_next_item_width(FIT_WIDTH)
                    imgui.text(str(key))

                    imgui.table_set_column_index(1)
                    if result := self.on_input_value(key, value):
                        changed_result = result

                    if self._options.removable:
                        imgui.table_set_column_index(2)
                        if button(f"{DELETE}###Del.{key}"):
                            remove_key = key
                        hovered_tooltip_text(f"Delete the item at {key}")

                if self._addable_factory is not None and self._options.adding:
                    temp_key = self._options.temp_key
                    temp_val = self._options.temp_val

                    imgui.table_next_row()
                    imgui.table_set_column_index(0)
                    imgui.set_next_item_width(FIT_WIDTH)
                    if key_result := input_text("##TempKey", temp_key):
                        self._options.temp_key = key_result.value

                    imgui.table_set_column_index(1)
                    imgui.set_next_item_width(FIT_WIDTH)
                    if val_result := input_text("##TempVal", temp_val):
                        self._options.temp_val = val_result.value

                    imgui.table_set_column_index(2)
                    has_temp_key = self._options.temp_key in self._container
                    action_button_spacing = self._options.action_button_spacing

                    imgui.push_style_var_x(ITEM_SPACING, action_button_spacing)
                    try:
                        if button(f"{CHECK}###TempOk", disabled=has_temp_key):
                            key, value = self._addable_factory(
                                self._options.temp_key,
                                self._options.temp_val,
                            )
                            assert key not in self._container
                            self._container[key] = value
                            self._options.temp_key = str()
                            self._options.temp_val = str()
                            self._options.adding = False

                        if has_temp_key:
                            hovered_tooltip_text(f"Key '{temp_key}' already exists")
                        else:
                            hovered_tooltip_text(f"Click to add item at '{temp_key}'")

                        imgui.same_line()
                        if button(f"{CLOSE}###TempCancel"):
                            self._options.adding = False
                    finally:
                        imgui.pop_style_var()

                if remove_key is not None:
                    self._container.pop(remove_key)
            finally:
                imgui.end_table()

            if self._addable_factory is not None and not self._options.adding:
                if imgui.button(PLUS):
                    self._options.adding = True
                hovered_tooltip_text("Add a new element")

        if changed_result is not None and changed_result.changed:
            self._container[changed_result.key] = changed_result.value

        return changed_result


@singleton
class GlobalTableMutableMappingOptions(Dict[int, TableMutableMappingOptions]):
    pass


def table_mutable_mapping(
    label: str,
    container: MutableMapping[_KT, _VT],
    options: Optional[TableMutableMappingOptions] = None,
    *,
    addable_factory: Optional[Callable[[str, str], Tuple[_KT, _VT]]] = None,
    removable: Optional[bool] = True,
    show_key: Optional[bool] = True,
    show_value: Optional[bool] = True,
):
    if options is None:
        global_options = GlobalTableMutableMappingOptions()
        next_id = imgui.get_id(label)
        options = global_options.get(next_id)
        if options is None:
            options = TableMutableMappingOptions()
            global_options.__setitem__(next_id, options)

    if removable is not None:
        options.removable = removable
    if show_key is not None:
        options.key_show = show_key
    if show_value is not None:
        options.value_show = show_value

    table = TableMutableMapping(label, container, options, addable_factory)
    return table.do_process()
