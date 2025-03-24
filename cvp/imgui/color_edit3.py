# -*- coding: utf-8 -*-

from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.color_edit import ColorEditFlags
from cvp.types.colors import RGB


class ColorEdit3Result(NamedTuple):
    changed: bool
    color: RGB

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        color = result[1]
        assert isinstance(changed, bool)
        assert isinstance(color, (tuple, list))
        assert len(color) == 3
        r, g, b = color
        assert isinstance(r, float)
        assert isinstance(g, float)
        assert isinstance(b, float)
        return cls(changed, (r, g, b))

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


def color_edit3(
    label: str,
    r: float,
    g: float,
    b: float,
    flags: Union[ColorEditFlags, int] = 0,
):
    if isinstance(flags, ColorEditFlags):
        flags = int(flags)
    assert isinstance(flags, int)
    result = imgui.color_edit3(label, [r, g, b], flags)
    return ColorEdit3Result.from_raw(result)
