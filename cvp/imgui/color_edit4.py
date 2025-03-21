# -*- coding: utf-8 -*-

from typing import NamedTuple

from imgui_bundle import imgui

from cvp.types.colors import RGBA


class ColorEdit4Result(NamedTuple):
    changed: bool
    color: RGBA

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        color = result[1]
        assert isinstance(changed, bool)
        assert isinstance(color, tuple)
        assert len(color) == 4
        r, g, b, a = color
        assert isinstance(r, float)
        assert isinstance(g, float)
        assert isinstance(b, float)
        assert isinstance(a, float)
        return cls(changed, (r, g, b, a))

    def __bool__(self) -> bool:
        return self.changed

    @property
    def r(self) -> float:
        return self.color[0]

    @property
    def g(self) -> float:
        return self.color[1]

    @property
    def b(self) -> float:
        return self.color[2]

    @property
    def a(self) -> float:
        return self.color[3]


def color_edit4(
    label: str,
    r: float,
    g: float,
    b: float,
    a: float,
    flags=0,
):
    result = imgui.color_edit4(label, r, g, b, a, flags)
    return ColorEdit4Result.from_raw(result)
