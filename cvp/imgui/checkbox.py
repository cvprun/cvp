# -*- coding: utf-8 -*-

from typing import NamedTuple

from imgui_bundle import imgui


class CheckboxResult(NamedTuple):
    clicked: bool
    state: bool

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        state = result[1]
        assert isinstance(changed, bool)
        assert isinstance(state, bool)
        return cls(changed, state)

    def __bool__(self):
        return self.clicked


def checkbox(label: str, state: bool):
    result = imgui.checkbox(label, state)
    return CheckboxResult.from_raw(result)
