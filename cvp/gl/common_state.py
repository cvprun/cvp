# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Any, NamedTuple

from OpenGL import GL


class GlCommonState(NamedTuple):
    last_texture: Any
    last_viewport: Any
    last_enable_blend: Any
    last_enable_cull_face: Any
    last_enable_depth_test: Any
    last_enable_scissor_test: Any
    last_scissor_box: Any
    last_blend_src: Any
    last_blend_dst: Any
    last_blend_equation_rgb: Any
    last_blend_equation_alpha: Any
    last_front_and_back_polygon_mode: Any


def get_common_gl_state() -> GlCommonState:
    """
    Backups the current OpenGL state.

    Returns a tuple of results for glGet / glIsEnabled calls

    NOTE: when adding more backuped state in the future,
    make sure to update function `restore_common_gl_state`
    """

    last_texture = GL.glGetIntegerv(GL.GL_TEXTURE_BINDING_2D)
    last_viewport = GL.glGetIntegerv(GL.GL_VIEWPORT)
    last_enable_blend = GL.glIsEnabled(GL.GL_BLEND)
    last_enable_cull_face = GL.glIsEnabled(GL.GL_CULL_FACE)
    last_enable_depth_test = GL.glIsEnabled(GL.GL_DEPTH_TEST)
    last_enable_scissor_test = GL.glIsEnabled(GL.GL_SCISSOR_TEST)
    last_scissor_box = GL.glGetIntegerv(GL.GL_SCISSOR_BOX)
    last_blend_src = GL.glGetIntegerv(GL.GL_BLEND_SRC)
    last_blend_dst = GL.glGetIntegerv(GL.GL_BLEND_DST)
    last_blend_equation_rgb = GL.glGetIntegerv(GL.GL_BLEND_EQUATION_RGB)
    last_blend_equation_alpha = GL.glGetIntegerv(GL.GL_BLEND_EQUATION_ALPHA)
    last_front_and_back_polygon_mode, _ = GL.glGetIntegerv(GL.GL_POLYGON_MODE)

    return GlCommonState(
        last_texture,
        last_viewport,
        last_enable_blend,
        last_enable_cull_face,
        last_enable_depth_test,
        last_enable_scissor_test,
        last_scissor_box,
        last_blend_src,
        last_blend_dst,
        last_blend_equation_rgb,
        last_blend_equation_alpha,
        last_front_and_back_polygon_mode,
    )


def restore_common_gl_state(state: GlCommonState) -> None:
    """
    Takes a tuple after calling function `get_common_gl_state`,
    to set the given OpenGL state back as it was before rendering the UI
    """

    GL.glBindTexture(GL.GL_TEXTURE_2D, state.last_texture)
    GL.glBlendEquationSeparate(
        state.last_blend_equation_rgb,
        state.last_blend_equation_alpha,
    )
    GL.glBlendFunc(state.last_blend_src, state.last_blend_dst)

    GL.glPolygonMode(GL.GL_FRONT_AND_BACK, state.last_front_and_back_polygon_mode)

    if state.last_enable_blend:
        GL.glEnable(GL.GL_BLEND)
    else:
        GL.glDisable(GL.GL_BLEND)

    if state.last_enable_cull_face:
        GL.glEnable(GL.GL_CULL_FACE)
    else:
        GL.glDisable(GL.GL_CULL_FACE)

    if state.last_enable_depth_test:
        GL.glEnable(GL.GL_DEPTH_TEST)
    else:
        GL.glDisable(GL.GL_DEPTH_TEST)

    if state.last_enable_scissor_test:
        GL.glEnable(GL.GL_SCISSOR_TEST)
    else:
        GL.glDisable(GL.GL_SCISSOR_TEST)

    GL.glScissor(
        state.last_scissor_box[0],
        state.last_scissor_box[1],
        state.last_scissor_box[2],
        state.last_scissor_box[3],
    )

    GL.glViewport(
        state.last_viewport[0],
        state.last_viewport[1],
        state.last_viewport[2],
        state.last_viewport[3],
    )


@contextmanager
def common_gl_state_context():
    common_gl_state_tuple = get_common_gl_state()
    try:
        yield common_gl_state_tuple
    finally:
        restore_common_gl_state(common_gl_state_tuple)
