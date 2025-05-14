# -*- coding: utf-8 -*-

from typing import Final, Tuple, TypeAlias

_X: TypeAlias = int
_Y: TypeAlias = int

PointI: TypeAlias = Tuple[_X, _Y]

_Width: TypeAlias = int
_Height: TypeAlias = int

SizeI: TypeAlias = Tuple[_Width, _Height]

_X1: TypeAlias = int  # Left
_X2: TypeAlias = int  # Right
_Y1: TypeAlias = int  # Top
_Y2: TypeAlias = int  # Bottom

RectI: TypeAlias = Tuple[_X1, _Y1, _X2, _Y2]

EMPTY_POINT_I: Final[PointI] = 0, 0
EMPTY_SIZE_I: Final[SizeI] = 0, 0
EMPTY_RECT_I: Final[RectI] = 0, 0, 0, 0

ONE_POINT_I: Final[PointI] = 1, 1
ONE_SIZE_I: Final[SizeI] = 1, 1
ONE_RECT_I: Final[RectI] = 1, 1, 1, 1
