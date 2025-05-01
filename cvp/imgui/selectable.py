# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.selectable import SelectableFlags


class SelectableResult(NamedTuple):
    clicked: bool
    selected: bool

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        selected = result[1]
        assert isinstance(changed, bool)
        assert isinstance(selected, bool)
        return cls(changed, selected)

    def __bool__(self):
        return self.clicked


def selectable(
    label: str,
    selected=False,
    flags: Union[SelectableFlags, int] = 0,
    size: Optional[imgui.ImVec2Like] = None,
):
    if isinstance(flags, SelectableFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    result = imgui.selectable(label, selected, flags, size)
    return SelectableResult.from_raw(result)
