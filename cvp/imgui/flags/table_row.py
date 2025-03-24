# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class TableRowFlags(IntFlag):
    none = imgui.TableRowFlags_.none.value
    headers = imgui.TableRowFlags_.headers.value


NONE: Final[int] = int(TableRowFlags.none)
HEADERS: Final[int] = int(TableRowFlags.headers)


def merge_table_row_flags(*flags: Union[TableRowFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
