# -*- coding: utf-8 -*-

from ctypes import c_void_p

from imgui_bundle import imgui
from OpenGL import GL

from cvp.gl.common_state import get_common_gl_state, restore_common_gl_state
from cvp.gl.textures.stash import stash_current_texture
from cvp.imgui.fonts.get_fonts import get_tex_data_as_raw_rgba32
from cvp.renderer.base.base import BaseRenderer
from cvp.types.override import override


class FixedPipelineRenderer(BaseRenderer):
    """Basic OpenGL integration base class."""

    @override
    def refresh_font_texture(self) -> None:
        with stash_current_texture():
            width, height, pixels = get_tex_data_as_raw_rgba32(self.io.fonts)

            if self._font_texture:
                GL.glDeleteTextures([self._font_texture])

            self._font_texture = GL.glGenTextures(1)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self._font_texture)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexImage2D(
                GL.GL_TEXTURE_2D,
                0,
                GL.GL_RGBA,
                width,
                height,
                0,
                GL.GL_RGBA,
                GL.GL_UNSIGNED_BYTE,
                pixels,
            )

            self.io.fonts.tex_id = self._font_texture
            self.io.fonts.clear_tex_data()

    @override
    def render(self, draw_data: imgui.ImDrawData) -> None:
        # perf: local for faster access
        io = self.io

        display_width, display_height = io.display_size
        fb_width = int(display_width * io.display_framebuffer_scale[0])
        fb_height = int(display_height * io.display_framebuffer_scale[1])

        if fb_width == 0 or fb_height == 0:
            return

        draw_data.scale_clip_rects(io.display_framebuffer_scale)

        # note: we are using fixed pipeline for cocos2d/pyglet
        # todo: consider porting to programmable pipeline
        # backup GL state
        common_gl_state_tuple = get_common_gl_state()

        GL.glPushAttrib(GL.GL_ENABLE_BIT | GL.GL_COLOR_BUFFER_BIT | GL.GL_TRANSFORM_BIT)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_SCISSOR_TEST)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_TEXTURE_COORD_ARRAY)
        GL.glEnableClientState(GL.GL_COLOR_ARRAY)
        GL.glEnable(GL.GL_TEXTURE_2D)

        GL.glViewport(0, 0, int(fb_width), int(fb_height))
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glPushMatrix()
        GL.glLoadIdentity()
        GL.glOrtho(0, io.display_size.x, io.display_size.y, 0.0, -1.0, 1.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix()
        GL.glLoadIdentity()

        for commands in draw_data.cmd_lists:
            idx_buffer = commands.idx_buffer.data_address()

            GL.glVertexPointer(
                2,
                GL.GL_FLOAT,
                imgui.VERTEX_SIZE,
                c_void_p(
                    commands.vtx_buffer.data_address() + imgui.VERTEX_BUFFER_POS_OFFSET
                ),
            )
            GL.glTexCoordPointer(
                2,
                GL.GL_FLOAT,
                imgui.VERTEX_SIZE,
                c_void_p(
                    commands.vtx_buffer.data_address() + imgui.VERTEX_BUFFER_UV_OFFSET
                ),
            )
            GL.glColorPointer(
                4,
                GL.GL_UNSIGNED_BYTE,
                imgui.VERTEX_SIZE,
                c_void_p(
                    commands.vtx_buffer.data_address() + imgui.VERTEX_BUFFER_COL_OFFSET
                ),
            )

            for command in commands.cmd_buffer:
                GL.glBindTexture(GL.GL_TEXTURE_2D, command.texture_id)

                x = command.clip_rect.x
                y = command.clip_rect.y
                z = command.clip_rect.z
                w = command.clip_rect.w
                GL.glScissor(int(x), int(fb_height - w), int(z - x), int(w - y))

                if imgui.INDEX_SIZE == 2:
                    gltype = GL.GL_UNSIGNED_SHORT
                else:
                    gltype = GL.GL_UNSIGNED_INT

                GL.glDrawElements(
                    GL.GL_TRIANGLES,
                    command.elem_count,
                    gltype,
                    c_void_p(idx_buffer),
                )
                idx_buffer += command.elem_count * imgui.INDEX_SIZE

        restore_common_gl_state(common_gl_state_tuple)

        GL.glDisableClientState(GL.GL_COLOR_ARRAY)
        GL.glDisableClientState(GL.GL_TEXTURE_COORD_ARRAY)
        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix()
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glPopMatrix()
        GL.glPopAttrib()

    @override
    def _invalidate_device_objects(self) -> None:
        if self._font_texture:
            GL.glDeleteTextures([self._font_texture])
        self._font_texture = 0
        self.io.fonts.tex_id = 0
