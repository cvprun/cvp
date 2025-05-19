# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from functools import lru_cache
from types import MappingProxyType

from OpenGL import GL


@unique
class TextureMinFilter(StrEnum):
    """
    Texture Minification Filter
    """

    nearest = auto()
    linear = auto()

    nearest_mipmap_nearest = auto()
    nearest_mipmap_linear = auto()

    linear_mipmap_nearest = auto()
    linear_mipmap_linear = auto()


@unique
class TextureMagFilter(StrEnum):
    """
    Texture Magnification Filter
    """

    nearest = auto()
    linear = auto()


@lru_cache
def texture_min_filter_mapping() -> MappingProxyType[TextureMinFilter, GL.Constant]:
    return MappingProxyType(
        {
            TextureMinFilter.nearest: GL.GL_NEAREST,
            TextureMinFilter.linear: GL.GL_LINEAR,
            TextureMinFilter.nearest_mipmap_nearest: GL.GL_NEAREST_MIPMAP_NEAREST,
            TextureMinFilter.nearest_mipmap_linear: GL.GL_NEAREST_MIPMAP_LINEAR,
            TextureMinFilter.linear_mipmap_nearest: GL.GL_LINEAR_MIPMAP_NEAREST,
            TextureMinFilter.linear_mipmap_linear: GL.GL_LINEAR_MIPMAP_LINEAR,
        }
    )


@lru_cache
def texture_mag_filter_mapping() -> MappingProxyType[TextureMagFilter, GL.Constant]:
    return MappingProxyType(
        {
            TextureMagFilter.nearest: GL.GL_NEAREST,
            TextureMagFilter.linear: GL.GL_LINEAR,
        }
    )
