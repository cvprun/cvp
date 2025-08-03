# -*- coding: utf-8 -*-

from functools import reduce
from typing import Callable, List, Optional

from imgui_bundle import imgui

from cvp.imgui.flags.key import KeyFlags, KeyLike
from cvp.imgui.keys.utils import alt_down, ctrl_down, shift_down, super_down


class Shortcut:
    def __init__(
        self,
        key: KeyLike,
        shift: Optional[bool] = None,
        ctrl: Optional[bool] = None,
        alt: Optional[bool] = None,
        meta: Optional[bool] = None,
        repeat=False,
        *,
        label: Optional[str] = None,
        callback: Optional[Callable[[], None]] = None,
    ):
        self._key = key
        self._shift = shift
        self._ctrl = ctrl
        self._alt = alt
        self._meta = meta
        self._repeat = repeat
        self._label = label if label else self.as_shortcut_text()
        self._callback = callback

    @property
    def key(self):
        return self._key

    @property
    def key_flags(self):
        if isinstance(self._key, KeyFlags):
            return self._key
        elif isinstance(self._key, imgui.Key):
            return KeyFlags(self._key.value)
        elif isinstance(self._key, int):
            return KeyFlags(self._key)
        else:
            raise TypeError(f"Unsupported key type: {type(self._key).__name__}")

    @property
    def imgui_key(self):
        if isinstance(self._key, KeyFlags):
            return imgui.Key(self._key.value)
        elif isinstance(self._key, imgui.Key):
            return self._key.value
        elif isinstance(self._key, int):
            return imgui.Key(self._key)
        else:
            raise TypeError(f"Unsupported key type: {type(self._key).__name__}")

    @property
    def key_name(self) -> str:
        # For numbers, the symbol name begins with an underscore
        return self.key_flags.name.removeprefix("_").upper()

    def _as_shortcut_text_parts(self) -> List[str]:
        parts = list()
        if self._shift:
            parts.append("Shift")
        if self._ctrl:
            parts.append("Ctrl")
        if self._alt:
            parts.append("Alt")
        if self._meta:
            parts.append("Meta")
        parts.append(self.key_name)
        return parts

    def as_shortcut_text(self) -> str:
        parts = self._as_shortcut_text_parts()
        assert 1 <= len(parts)
        return reduce(lambda x, y: f"{x}+{y}", parts)

    @property
    def shift(self):
        return self._shift

    @property
    def ctrl(self):
        return self._ctrl

    @property
    def alt(self):
        return self._alt

    @property
    def meta(self):
        return self._meta

    @property
    def repeat(self):
        return self._repeat

    @property
    def label(self):
        return self._label

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
        return imgui.is_key_down(self.imgui_key)

    def is_key_pressed(self) -> bool:
        return imgui.is_key_pressed(self.imgui_key, repeat=self._repeat)

    def is_key_released(self) -> bool:
        return imgui.is_key_released(self.imgui_key)

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

    def __call__(self) -> bool:
        if self.is_pressed() and self._callback is not None:
            self._callback()
            return True
        else:
            return False
