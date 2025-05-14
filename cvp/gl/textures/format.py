# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from functools import lru_cache
from types import MappingProxyType

from OpenGL import GL


@unique
class TextureFormat(StrEnum):
    color_index = auto()
    red = auto()
    green = auto()
    blue = auto()
    alpha = auto()
    rgb = auto()
    rgba = auto()
    luminance = auto()
    luminance_alpha = auto()


@lru_cache
def texture_format_mapping() -> MappingProxyType[TextureFormat, GL.Constant]:
    return MappingProxyType(
        {
            TextureFormat.color_index: GL.GL_COLOR_INDEX,
            TextureFormat.red: GL.GL_RED,
            TextureFormat.green: GL.GL_GREEN,
            TextureFormat.blue: GL.GL_BLUE,
            TextureFormat.alpha: GL.GL_ALPHA,
            TextureFormat.rgb: GL.GL_RGB,
            TextureFormat.rgba: GL.GL_RGBA,
            TextureFormat.luminance: GL.GL_LUMINANCE,
            TextureFormat.luminance_alpha: GL.GL_LUMINANCE_ALPHA,
        }
    )


@lru_cache
def texture_format_channels_mapping() -> MappingProxyType[TextureFormat, int]:
    return MappingProxyType(
        {
            TextureFormat.color_index: 1,
            TextureFormat.red: 1,
            TextureFormat.green: 1,
            TextureFormat.blue: 1,
            TextureFormat.alpha: 1,
            TextureFormat.rgb: 3,
            TextureFormat.rgba: 4,
            TextureFormat.luminance: 1,
            TextureFormat.luminance_alpha: 2,
        }
    )
