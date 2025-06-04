# -*- coding: utf-8 -*-

from typing import List, NamedTuple, Optional

from imgui_bundle import imgui

from cvp.assets.fonts import mdi
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS
from cvp.imgui.flags.table_column import WIDTH_FIXED, WIDTH_STRETCH
from cvp.imgui.input_int import input_int
from cvp.patterns.temp import TempValue
from cvp.psutil.process.rlimit import ResourceLimits, ResourceLimitTuple
from cvp.variables import NOT_FOUND_INDEX


class RlimitEditResult(NamedTuple):
    changed: bool
    value: ResourceLimits
    keys: List[int]

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 3
        changed = result[0]
        value = result[1]
        keys = result[2]
        assert isinstance(changed, bool)
        assert isinstance(value, ResourceLimits)
        assert isinstance(keys, list)
        return cls(changed, value, keys)

    def __bool__(self):
        return self.changed


def rlimit_edit(
    label: str,
    rlimit: TempValue[ResourceLimits],
    width: Optional[float] = None,
    *,
    top_title: Optional[str] = None,
    right_title: Optional[str] = None,
    border=False,
    no_commit=False,
) -> RlimitEditResult:
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

        tablename = ResourceLimits.__name__
        columns = len(ResourceLimitTuple._fields)
        imgui.begin_table(
            tablename,
            columns,
            flags=DEFAULT_TABLE_FLAGS,
            outer_size=(FIT_WIDTH, 0),
        )
        try:
            imgui.table_setup_column("Constants", WIDTH_FIXED)
            imgui.table_setup_column("Name", WIDTH_FIXED)
            imgui.table_setup_column("Soft", WIDTH_STRETCH)
            imgui.table_setup_column("Hard", WIDTH_STRETCH)
            imgui.table_headers_row()

            update_resource = NOT_FOUND_INDEX
            update_name = str()
            update_soft = 0
            update_hard = 0

            for limit in rlimit.temp.values():
                imgui.table_next_row()

                imgui.table_set_column_index(0)
                imgui.text(str(limit.resource))

                imgui.table_set_column_index(1)
                imgui.text(str(limit.name))

                imgui.table_set_column_index(2)
                imgui.set_next_item_width(FIT_WIDTH)
                if soft := input_int(f"##Soft.{limit.resource}", limit.soft):
                    update_resource = limit.resource
                    update_name = limit.name
                    update_soft = soft.value
                    update_hard = limit.hard

                imgui.table_set_column_index(3)
                imgui.set_next_item_width(FIT_WIDTH)
                if hard := input_int(f"##Hard.{limit.resource}", limit.hard):
                    update_resource = limit.resource
                    update_name = limit.name
                    update_soft = limit.soft
                    update_hard = hard.value

            if update_resource != NOT_FOUND_INDEX:
                rlimit.temp[update_resource] = ResourceLimitTuple(
                    update_resource,
                    update_name,
                    update_soft,
                    update_hard,
                )
        finally:
            imgui.end_table()

        if button(f"{mdi.CLOSE} Cancel", disabled=not rlimit.changed):
            rlimit.reset(use_deepcopy=True)

        imgui.same_line()
        if button(f"{mdi.CHECK} Commit", disabled=not rlimit.changed):
            changed_keys = list()
            for key, item in rlimit.temp.items():
                if item != rlimit.value[key]:
                    changed_keys.append(key)
            assert 1 <= len(changed_keys)
            if not no_commit:
                rlimit.commit(use_deepcopy=True)
            return RlimitEditResult(True, rlimit.value, changed_keys)

    if right_title:
        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text(right_title)

    return RlimitEditResult(False, rlimit.value, list())
