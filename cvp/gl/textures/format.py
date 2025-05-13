# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from OpenGL import GL


@unique
class TextureFormat(StrEnum):
    rgb = auto()
    rgba = auto()
    alpha = auto()
    luminance = auto()
    luminance_alpha = auto()
    depth = auto()


def create_texture_format_mapping():
    return {
        TextureFormat.rgb: GL.GL_RGB,
        TextureFormat.rgba: GL.GL_RGBA,
        TextureFormat.alpha: GL.GL_ALPHA,
        TextureFormat.luminance: GL.GL_LUMINANCE,
        TextureFormat.luminance_alpha: GL.GL_LUMINANCE_ALPHA,
        TextureFormat.depth: GL.GL_DEPTH_COMPONENT,
    }


def create_texture_channels_mapping():
    return {
        TextureFormat.rgb: 3,
        TextureFormat.rgba: 4,
        TextureFormat.alpha: 1,
        TextureFormat.luminance: 1,
        TextureFormat.luminance_alpha: 2,
        TextureFormat.depth: 1,
    }
