# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import List, NamedTuple

from imgui_bundle import imgui


@unique
class SortDirection(IntEnum):
    ascending = 1  # Ascending = 0->9, A->Z etc.
    descending = 2  # Descending = 9->0, Z->A etc.


class TableSortSpec(NamedTuple):
    column: int
    order: int
    direction: SortDirection
    user_id: int


def sort_specs_by_order(
    sort_specs: imgui.TableSortSpecs,
    *,
    reverse=False,
) -> List[TableSortSpec]:
    result = list()

    for spec_index in range(sort_specs.specs_count):
        spec = sort_specs.get_specs(spec_index)

        if spec.sort_direction == imgui.SortDirection.ascending:
            direction = SortDirection.ascending
        elif spec.sort_direction == imgui.SortDirection.descending:
            direction = SortDirection.descending
        else:
            assert False, "Inaccessible sort direction"

        item = TableSortSpec(
            spec.column_index,
            spec.sort_order,
            direction,
            spec.column_user_id,
        )
        result.append(item)

    result.sort(key=lambda x: x.order, reverse=reverse)
    return result
