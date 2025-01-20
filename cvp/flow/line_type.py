# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final, Sequence

from cvp.types.enum.normalize.string import index2string, string2index


@unique
class LineType(StrEnum):
    linear = auto()
    bezier_cubic = auto()


LINE_TYPE_INDEX2NAME = index2string(LineType)
LINE_TYPE_NAME2INDEX = string2index(LineType)
LINE_TYPE_NAMES: Final[Sequence[str]] = tuple(LINE_TYPE_INDEX2NAME.values())
