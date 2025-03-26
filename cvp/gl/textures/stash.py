# -*- coding: utf-8 -*-

from contextlib import contextmanager

from OpenGL import GL


@contextmanager
def stash_current_texture():
    """
    Context manager that saves the currently bound GL_TEXTURE_2D texture,
    yields its ID, and restores it after the context exits.

    This is useful when temporarily binding a different texture and wanting
    to ensure the previous texture binding is restored afterward.
    """

    latest_texture = GL.glGetIntegerv(GL.GL_TEXTURE_BINDING_2D)
    latest_texture = int(latest_texture)
    try:
        yield latest_texture
    finally:
        GL.glBindTexture(GL.GL_TEXTURE_2D, latest_texture)
