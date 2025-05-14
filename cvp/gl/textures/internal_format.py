# -*- coding: utf-8 -*-
# https://learn.microsoft.com/en-us/windows/win32/opengl/glteximage2d

from enum import StrEnum, auto, unique
from functools import lru_cache
from types import MappingProxyType
from typing import Union

from OpenGL import GL


@unique
class TextureInternalFormat(StrEnum):
    n1 = auto()
    n2 = auto()
    n3 = auto()
    n4 = auto()
    alpha = auto()
    alpha4 = auto()
    alpha8 = auto()
    alpha12 = auto()
    alpha16 = auto()
    luminance = auto()
    luminance4 = auto()
    luminance8 = auto()
    luminance12 = auto()
    luminance16 = auto()
    luminance_alpha = auto()
    luminance4_alpha4 = auto()
    luminance6_alpha2 = auto()
    luminance8_alpha8 = auto()
    luminance12_alpha4 = auto()
    luminance12_alpha12 = auto()
    luminance16_alpha16 = auto()
    intensity = auto()
    intensity4 = auto()
    intensity8 = auto()
    intensity12 = auto()
    intensity16 = auto()
    r3_g3_b2 = auto()
    rgb = auto()
    rgb4 = auto()
    rgb5 = auto()
    rgb8 = auto()
    rgb10 = auto()
    rgb12 = auto()
    rgb16 = auto()
    rgba = auto()
    rgba2 = auto()
    rgba4 = auto()
    rgb5_a1 = auto()
    rgba8 = auto()
    rgb10_a2 = auto()
    rgba12 = auto()
    rgba16 = auto()


_MappingType = MappingProxyType[TextureInternalFormat, Union[int, GL.Constant]]


@lru_cache
def texture_internal_format_mapping() -> _MappingType:
    return MappingProxyType(
        {
            TextureInternalFormat.n1: 1,
            TextureInternalFormat.n2: 2,
            TextureInternalFormat.n3: 3,
            TextureInternalFormat.n4: 4,
            TextureInternalFormat.alpha: GL.GL_ALPHA,
            TextureInternalFormat.alpha4: GL.GL_ALPHA4,
            TextureInternalFormat.alpha8: GL.GL_ALPHA8,
            TextureInternalFormat.alpha12: GL.GL_ALPHA12,
            TextureInternalFormat.alpha16: GL.GL_ALPHA16,
            TextureInternalFormat.luminance: GL.GL_LUMINANCE,
            TextureInternalFormat.luminance4: GL.GL_LUMINANCE4,
            TextureInternalFormat.luminance8: GL.GL_LUMINANCE8,
            TextureInternalFormat.luminance12: GL.GL_LUMINANCE12,
            TextureInternalFormat.luminance16: GL.GL_LUMINANCE16,
            TextureInternalFormat.luminance_alpha: GL.GL_LUMINANCE_ALPHA,
            TextureInternalFormat.luminance4_alpha4: GL.GL_LUMINANCE4_ALPHA4,
            TextureInternalFormat.luminance6_alpha2: GL.GL_LUMINANCE6_ALPHA2,
            TextureInternalFormat.luminance8_alpha8: GL.GL_LUMINANCE8_ALPHA8,
            TextureInternalFormat.luminance12_alpha4: GL.GL_LUMINANCE12_ALPHA4,
            TextureInternalFormat.luminance12_alpha12: GL.GL_LUMINANCE12_ALPHA12,
            TextureInternalFormat.luminance16_alpha16: GL.GL_LUMINANCE16_ALPHA16,
            TextureInternalFormat.intensity: GL.GL_INTENSITY,
            TextureInternalFormat.intensity4: GL.GL_INTENSITY4,
            TextureInternalFormat.intensity8: GL.GL_INTENSITY8,
            TextureInternalFormat.intensity12: GL.GL_INTENSITY12,
            TextureInternalFormat.intensity16: GL.GL_INTENSITY16,
            TextureInternalFormat.r3_g3_b2: GL.GL_R3_G3_B2,
            TextureInternalFormat.rgb: GL.GL_RGB,
            TextureInternalFormat.rgb4: GL.GL_RGB4,
            TextureInternalFormat.rgb5: GL.GL_RGB5,
            TextureInternalFormat.rgb8: GL.GL_RGB8,
            TextureInternalFormat.rgb10: GL.GL_RGB10,
            TextureInternalFormat.rgb12: GL.GL_RGB12,
            TextureInternalFormat.rgb16: GL.GL_RGB16,
            TextureInternalFormat.rgba: GL.GL_RGBA,
            TextureInternalFormat.rgba2: GL.GL_RGBA2,
            TextureInternalFormat.rgba4: GL.GL_RGBA4,
            TextureInternalFormat.rgb5_a1: GL.GL_RGB5_A1,
            TextureInternalFormat.rgba8: GL.GL_RGBA8,
            TextureInternalFormat.rgb10_a2: GL.GL_RGB10_A2,
            TextureInternalFormat.rgba12: GL.GL_RGBA12,
            TextureInternalFormat.rgba16: GL.GL_RGBA16,
        }
    )
