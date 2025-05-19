# -*- coding: utf-8 -*-

from OpenGL import GL

from cvp.gl.version import get_version_tuple
from cvp.variables import DEFAULT_MAX_TEXTURE_SIZE


def get_max_texture_size() -> int:
    return int(GL.glGetIntegerv(GL.GL_MAX_TEXTURE_SIZE))


def get_default_max_texture_size() -> int:
    try:
        major, minor, _ = get_version_tuple()
    except:  # noqa
        return DEFAULT_MAX_TEXTURE_SIZE

    assert isinstance(major, int)
    assert isinstance(minor, int)
    version = major, minor

    if (4, 3) <= version:
        return 16384
    elif (3, 0) <= version:
        return 4096
    elif (2, 0) <= version:
        return 2048
    elif (1, 2) <= version:
        return 1024
    elif (1, 0) <= version:
        return 64
    else:
        return DEFAULT_MAX_TEXTURE_SIZE
