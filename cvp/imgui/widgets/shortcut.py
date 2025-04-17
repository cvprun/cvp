# -*- coding: utf-8 -*-

from functools import reduce
from typing import List, Optional

from imgui_bundle import imgui

from cvp.imgui.keys.utils import alt_down, ctrl_down, shift_down, super_down


class Shortcut:
    def __init__(
        self,
        key: imgui.Key,
        shift: Optional[bool] = None,
        ctrl: Optional[bool] = None,
        alt: Optional[bool] = None,
        meta: Optional[bool] = None,
        *,
        repeat=False,
    ):
        self._key = key
        self._shift = shift
        self._ctrl = ctrl
        self._alt = alt
        self._meta = meta
        self._repeat = repeat
        self._label = self.as_shortcut_text()

    def as_shortcut_text_parts(self) -> List[str]:
        parts = list()
        if self._shift:
            parts.append("Shift")
        if self._ctrl:
            parts.append("Ctrl")
        if self._alt:
            parts.append("Alt")
        if self._meta:
            parts.append("Meta")

        # For numbers, the symbol name begins with an underscore
        parts.append(self._key.name.removeprefix("_").upper())
        return parts

    def as_shortcut_text(self) -> str:
        parts = self.as_shortcut_text_parts()
        assert 1 <= len(parts)
        return reduce(lambda x, y: f"{x}+{y}", parts)

    def is_mod_down(self) -> bool:
        if self._shift is not None and self._shift != shift_down():
            return False
        if self._ctrl is not None and self._ctrl != ctrl_down():
            return False
        if self._alt is not None and self._alt != alt_down():
            return False
        if self._meta is not None and self._meta != super_down():
            return False
        return True

    def is_key_down(self) -> bool:
        return imgui.is_key_down(self._key)

    def is_key_pressed(self) -> bool:
        return imgui.is_key_pressed(self._key, repeat=self._repeat)

    def is_key_released(self) -> bool:
        return imgui.is_key_released(self._key)

    def is_down(self) -> bool:
        return self.is_mod_down() and self.is_key_down()

    def is_pressed(self) -> bool:
        return self.is_mod_down() and self.is_key_pressed()

    def is_released(self) -> bool:
        return self.is_mod_down() and self.is_key_released()

    def __bool__(self):
        return self.is_pressed()

    def __str__(self):
        return self._label
