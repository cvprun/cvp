# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from functools import lru_cache
from types import MappingProxyType

from OpenGL import GL


@unique
class TextureWrap(StrEnum):
    clamp = auto()
    repeat = auto()
    mirrored_repeat = auto()
    clamp_to_edge = auto()
    clamp_to_border = auto()


@lru_cache
def texture_wrap_mapping() -> MappingProxyType[TextureWrap, GL.Constant]:
    return MappingProxyType(
        {
            TextureWrap.clamp: GL.GL_CLAMP,
            TextureWrap.repeat: GL.GL_REPEAT,
            TextureWrap.mirrored_repeat: GL.GL_MIRRORED_REPEAT,
            TextureWrap.clamp_to_edge: GL.GL_CLAMP_TO_EDGE,
            TextureWrap.clamp_to_border: GL.GL_CLAMP_TO_BORDER,
        }
    )
