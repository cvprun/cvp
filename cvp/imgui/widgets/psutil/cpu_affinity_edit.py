# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import List, NamedTuple, Optional, Sequence

from imgui_bundle import imgui

from cvp.assets.fonts import mdi
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.flags.table_column import WIDTH_STRETCH
from cvp.patterns.temp import TempValue
from cvp.variables import NOT_FOUND_INDEX


class CpuAffinityEditResult(NamedTuple):
    changed: bool
    value: List[int]

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, list)
        return cls(changed, value)

    def __bool__(self):
        return self.changed


def cpu_affinity_edit(
    label: str,
    cpu_indexes: Sequence[int],
    cpu_affinity: TempValue[List[int]],
    width: Optional[float] = None,
    columns=8,
    *,
    top_title: Optional[str] = None,
    right_title: Optional[str] = None,
    border=False,
    no_commit=False,
) -> CpuAffinityEditResult:
    if width is None:
        width = imgui.calc_item_width()
    assert isinstance(width, float)

    with begin_child_context(
        label=label,
        size=(width, 0),
        child_flags=AUTO_RESIZE_Y | (BORDERS if border else 0),
    ):
        if top_title:
            imgui.text(top_title)
            imgui.separator()

        imgui.begin_table("CpuAffinityTable", columns, outer_size=(FIT_WIDTH, 0))
        try:
            for column_index in range(columns):
                imgui.table_setup_column(f"##Column{column_index}", WIDTH_STRETCH)

            update_cpu_index = NOT_FOUND_INDEX
            update_cpu_state = False

            for cpu_index in cpu_indexes:
                imgui.table_next_column()

                has_cpu = cpu_index in cpu_affinity.temp
                if check := checkbox(f"CPU{cpu_index}", has_cpu):
                    update_cpu_index = cpu_index
                    update_cpu_state = check.state

            if update_cpu_index != NOT_FOUND_INDEX:
                if update_cpu_state:
                    cpu_affinity.temp.append(update_cpu_index)
                    cpu_affinity.temp.sort()
                else:
                    cpu_affinity.temp.remove(update_cpu_index)
        finally:
            imgui.end_table()

        if button("Select ALL"):
            cpu_affinity.temp = list(cpu_indexes)

        imgui.same_line()
        if button("Unselect ALL"):
            cpu_affinity.temp = list()

        imgui.same_line()
        if button(f"{mdi.CLOSE} Cancel", disabled=not cpu_affinity.changed):
            cpu_affinity.reset(use_deepcopy=True)

        imgui.same_line()
        if button(f"{mdi.CHECK} Commit", disabled=not cpu_affinity.changed):
            if not no_commit:
                cpu_affinity.commit(use_deepcopy=True)

            return CpuAffinityEditResult(True, deepcopy(cpu_affinity.value))

    if right_title:
        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text(right_title)

    return CpuAffinityEditResult(False, deepcopy(cpu_affinity.value))
