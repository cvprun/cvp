# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.tab_item import TabItemFlags


class BeginTabItemResult(NamedTuple):
    opened: bool
    value: Optional[bool]

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, (type(None), bool))
        return cls(changed, value)

    def __bool__(self):
        return self.opened


def begin_tab_item(
    label: str,
    opened: Optional[bool] = None,
    flags: Union[TabItemFlags, int] = 0,
):
    if isinstance(flags, TabItemFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    result = imgui.begin_tab_item(label, opened, flags)
    return BeginTabItemResult.from_raw(result)


def end_tab_item() -> None:
    imgui.end_tab_item()
