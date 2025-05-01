# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final

from imgui_bundle import imgui


@unique
class Cond(IntEnum):
    none = imgui.Cond_.none.value
    always = imgui.Cond_.always.value
    once = imgui.Cond_.once.value
    first_use_ever = imgui.Cond_.first_use_ever.value
    appearing = imgui.Cond_.appearing.value


NONE: Final[int] = int(Cond.none)
ALWAYS: Final[int] = int(Cond.always)
ONCE: Final[int] = int(Cond.once)
FIRST_USE_EVER: Final[int] = int(Cond.first_use_ever)
APPEARING: Final[int] = int(Cond.appearing)
