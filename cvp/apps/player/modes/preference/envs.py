# -*- coding: utf-8 -*-

import os
from typing import Optional, Tuple

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.input_text_with_hint import input_text_with_hint
from cvp.imgui.widgets.table_mutable_mapping import TableMutableMapping
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX


class EnvsPreference(BasePreference):
    __cvp_menu_name__ = "Environment Variables"

    _table: TableMutableMapping[str, str]

    def __init__(self, context: Context):
        super().__init__(context)
        self._key_filter = str()
        self._value_filter = str()
        self._table = TableMutableMapping(
            label="EnvTable",
            container=os.environ,
            options=None,
            addable_factory=self.on_addable_factory,
            filter_callback=self.on_filter_callback,
        )

    @staticmethod
    def on_addable_factory(key: str, value: str) -> Optional[Tuple[str, str]]:
        return key, value

    def on_filter_callback(self, key: str, value: str) -> bool:
        if not self._key_filter and not self._value_filter:
            return True

        if self._key_filter and key.find(self._key_filter) != NOT_FOUND_INDEX:
            return True

        if self._value_filter and value.find(self._value_filter) != NOT_FOUND_INDEX:
            return True

        return False

    @override
    def on_process(self) -> None:
        if key_filter := input_text_with_hint(
            label="Key filter",
            hint="Enter a keyword to filter keys",
            value=self._key_filter,
        ):
            self._key_filter = key_filter.value

        if value_filter := input_text_with_hint(
            label="Value filter",
            hint="Enter a keyword to filter values",
            value=self._value_filter,
        ):
            self._value_filter = value_filter.value

        with begin_child_context(
            label="EnvChild",
            size=(imgui.calc_item_width(), 0),
            child_flags=AUTO_RESIZE_Y,
        ):
            self._table.do_process()
