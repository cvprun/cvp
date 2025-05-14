# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from functools import lru_cache
from types import MappingProxyType

from OpenGL import GL


@unique
class TextureDataType(StrEnum):
    unsigned_byte = auto()
    byte = auto()
    bitmap = auto()
    unsigned_short = auto()
    short = auto()
    unsigned_int = auto()
    int = auto()
    float = auto()


@lru_cache
def texture_data_type_mapping() -> MappingProxyType[TextureDataType, GL.Constant]:
    return MappingProxyType(
        {
            TextureDataType.unsigned_byte: GL.GL_UNSIGNED_BYTE,
            TextureDataType.byte: GL.GL_BYTE,
            TextureDataType.bitmap: GL.GL_BITMAP,
            TextureDataType.unsigned_short: GL.GL_UNSIGNED_SHORT,
            TextureDataType.short: GL.GL_SHORT,
            TextureDataType.unsigned_int: GL.GL_UNSIGNED_INT,
            TextureDataType.int: GL.GL_INT,
            TextureDataType.float: GL.GL_FLOAT,
        }
    )
