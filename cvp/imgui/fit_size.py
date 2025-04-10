# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.types.shapes import Size

FIT_WIDTH: Final[float] = -1 * imgui.FLT_MIN
FIT_HEIGHT: Final[float] = -1 * imgui.FLT_MIN
FIT_SIZE: Final[Size] = FIT_WIDTH, FIT_HEIGHT
