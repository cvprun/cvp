# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final

from imgui_bundle import imgui


@unique
class Condition(IntEnum):
    none = imgui.Cond_.none.value
    always = imgui.Cond_.always.value
    once = imgui.Cond_.once.value
    first_use_ever = imgui.Cond_.first_use_ever.value
    appearing = imgui.Cond_.appearing.value


NONE: Final[int] = int(Condition.none)
ALWAYS: Final[int] = int(Condition.always)
ONCE: Final[int] = int(Condition.once)
FIRST_USE_EVER: Final[int] = int(Condition.first_use_ever)
APPEARING: Final[int] = int(Condition.appearing)
