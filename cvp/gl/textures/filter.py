# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from functools import lru_cache
from types import MappingProxyType

from OpenGL import GL


@unique
class TextureFilter(StrEnum):
    nearest = auto()
    linear = auto()
    nearest_mipmap_nearest = auto()
    linear_mipmap_nearest = auto()
    nearest_mipmap_linear = auto()
    linear_mipmap_linear = auto()


@lru_cache
def texture_filter_mapping() -> MappingProxyType[TextureFilter, GL.Constant]:
    return MappingProxyType(
        {
            TextureFilter.nearest: GL.GL_NEAREST,
            TextureFilter.linear: GL.GL_LINEAR,
            TextureFilter.nearest_mipmap_nearest: GL.GL_NEAREST_MIPMAP_NEAREST,
            TextureFilter.linear_mipmap_nearest: GL.GL_LINEAR_MIPMAP_NEAREST,
            TextureFilter.nearest_mipmap_linear: GL.GL_NEAREST_MIPMAP_LINEAR,
            TextureFilter.linear_mipmap_linear: GL.GL_LINEAR_MIPMAP_LINEAR,
        }
    )
