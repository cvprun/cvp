# -*- coding: utf-8 -*-

import ctypes

from OpenGL import GL
from imgui_bundle import imgui
from numpy import ndarray

from cvp.renderer.base import BaseOpenGLRenderer

VERTEX_SHADER_SRC = """
#version 330

uniform mat4 ProjMtx;
in vec2 Position;
in vec2 UV;
in vec4 Color;
out vec2 Frag_UV;
out vec4 Frag_Color;

void main() {
    Frag_UV = UV;
    Frag_Color = Color;

    gl_Position = ProjMtx * vec4(Position.xy, 0, 1);
}
"""

FRAGMENT_SHADER_SRC = """
#version 330

uniform sampler2D Texture;
in vec2 Frag_UV;
in vec4 Frag_Color;
out vec4 Out_Color;

void main() {
    Out_Color = Frag_Color * texture(Texture, Frag_UV.st);
}
"""


class ProgrammablePipelineRenderer(BaseOpenGLRenderer):
    """Basic OpenGL integration base class."""

    def __init__(self):
        self._shader_handle = None
        self._vert_handle = None
        self._fragment_handle = None

        self._attrib_location_tex = None
        self._attrib_proj_mtx = None
        self._attrib_location_position = None
        self._attrib_location_uv = None
        self._attrib_location_color = None

        self._vbo_handle = None
        self._elements_handle = None
        self._vao_handle = None

        super(ProgrammablePipelineRenderer, self).__init__()

    def refresh_font_texture(self):
        # save texture state
        last_texture = GL.glGetIntegerv(GL.GL_TEXTURE_BINDING_2D)

        # width, height, pixels = self.io.fonts.get_tex_data_as_rgba32()
        font_matrix = self.io.fonts.get_tex_data_as_rgba32()
        assert isinstance(font_matrix, ndarray)
        width = font_matrix.shape[1]
        height = font_matrix.shape[0]
        pixels = font_matrix.data

        if self._font_texture is not None:
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
        GL.glBindTexture(GL.GL_TEXTURE_2D, last_texture)
        self.io.fonts.clear_tex_data()

    def _create_device_objects(self):
        # save state
        last_texture = GL.glGetIntegerv(GL.GL_TEXTURE_BINDING_2D)
        last_array_buffer = GL.glGetIntegerv(GL.GL_ARRAY_BUFFER_BINDING)

        last_vertex_array = GL.glGetIntegerv(GL.GL_VERTEX_ARRAY_BINDING)

        self._shader_handle = GL.glCreateProgram()
        # note: no need to store shader parts handles after linking
        vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)

        GL.glShaderSource(vertex_shader, VERTEX_SHADER_SRC)
        GL.glShaderSource(fragment_shader, FRAGMENT_SHADER_SRC)
        GL.glCompileShader(vertex_shader)
        GL.glCompileShader(fragment_shader)

        GL.glAttachShader(self._shader_handle, vertex_shader)
        GL.glAttachShader(self._shader_handle, fragment_shader)

        GL.glLinkProgram(self._shader_handle)

        # note: after linking shaders can be removed
        GL.glDeleteShader(vertex_shader)
        GL.glDeleteShader(fragment_shader)

        self._attrib_location_tex = GL.glGetUniformLocation(
            self._shader_handle, "Texture"
        )
        self._attrib_proj_mtx = GL.glGetUniformLocation(self._shader_handle, "ProjMtx")
        self._attrib_location_position = GL.glGetAttribLocation(
            self._shader_handle, "Position"
        )
        self._attrib_location_uv = GL.glGetAttribLocation(self._shader_handle, "UV")
        self._attrib_location_color = GL.glGetAttribLocation(
            self._shader_handle, "Color"
        )

        self._vbo_handle = GL.glGenBuffers(1)
        self._elements_handle = GL.glGenBuffers(1)

        self._vao_handle = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_handle)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vbo_handle)

        GL.glEnableVertexAttribArray(self._attrib_location_position)
        GL.glEnableVertexAttribArray(self._attrib_location_uv)
        GL.glEnableVertexAttribArray(self._attrib_location_color)

        GL.glVertexAttribPointer(
            self._attrib_location_position,
            2,
            GL.GL_FLOAT,
            GL.GL_FALSE,
            imgui.VERTEX_SIZE,
            ctypes.c_void_p(imgui.VERTEX_BUFFER_POS_OFFSET),
        )
        GL.glVertexAttribPointer(
            self._attrib_location_uv,
            2,
            GL.GL_FLOAT,
            GL.GL_FALSE,
            imgui.VERTEX_SIZE,
            ctypes.c_void_p(imgui.VERTEX_BUFFER_UV_OFFSET),
        )
        GL.glVertexAttribPointer(
            self._attrib_location_color,
            4,
            GL.GL_UNSIGNED_BYTE,
            GL.GL_TRUE,
            imgui.VERTEX_SIZE,
            ctypes.c_void_p(imgui.VERTEX_BUFFER_COL_OFFSET),
        )

        # restore state
        GL.glBindTexture(GL.GL_TEXTURE_2D, last_texture)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, last_array_buffer)
        GL.glBindVertexArray(last_vertex_array)

    def render(self, draw_data: imgui.ImDrawData):
        # perf: local for faster access
        io = self.io

        display_width, display_height = io.display_size
        fb_width = int(display_width * io.display_framebuffer_scale[0])
        fb_height = int(display_height * io.display_framebuffer_scale[1])

        if fb_width == 0 or fb_height == 0:
            return

        draw_data.scale_clip_rects(io.display_framebuffer_scale)

        # backup GL state
        # todo: provide cleaner version of this backup-restore code
        common_gl_state_tuple = get_common_gl_state()
        last_program = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
        last_active_texture = GL.glGetIntegerv(GL.GL_ACTIVE_TEXTURE)
        last_array_buffer = GL.glGetIntegerv(GL.GL_ARRAY_BUFFER_BINDING)
        last_element_array_buffer = GL.glGetIntegerv(GL.GL_ELEMENT_ARRAY_BUFFER_BINDING)
        last_vertex_array = GL.glGetIntegerv(GL.GL_VERTEX_ARRAY_BINDING)

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendEquation(GL.GL_FUNC_ADD)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_SCISSOR_TEST)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

        GL.glViewport(0, 0, int(fb_width), int(fb_height))

        ortho_projection = (ctypes.c_float * 16)(  # noqa
            2.0 / display_width,
            0.0,
            0.0,
            0.0,
            0.0,
            2.0 / -display_height,
            0.0,
            0.0,
            0.0,
            0.0,
            -1.0,
            0.0,
            -1.0,
            1.0,
            0.0,
            1.0,
            )

        GL.glUseProgram(self._shader_handle)
        GL.glUniform1i(self._attrib_location_tex, 0)
        GL.glUniformMatrix4fv(self._attrib_proj_mtx, 1, GL.GL_FALSE, ortho_projection)
        GL.glBindVertexArray(self._vao_handle)

        for commands in draw_data.cmd_lists:

            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vbo_handle)
            # todo: check this (sizes)
            GL.glBufferData(
                GL.GL_ARRAY_BUFFER,
                commands.vtx_buffer.size() * imgui.VERTEX_SIZE,
                ctypes.c_void_p(commands.vtx_buffer.data_address()),
                GL.GL_STREAM_DRAW,
                )

            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self._elements_handle)
            # todo: check this (sizes)
            GL.glBufferData(
                GL.GL_ELEMENT_ARRAY_BUFFER,
                commands.idx_buffer.size() * imgui.INDEX_SIZE,
                ctypes.c_void_p(commands.idx_buffer.data_address()),
                GL.GL_STREAM_DRAW,
                )

            # todo: allow to iterate over _CmdList
            for command in commands.cmd_buffer:
                GL.glBindTexture(GL.GL_TEXTURE_2D, command.texture_id)

                # todo: use named tuple
                x, y, z, w = command.clip_rect
                GL.glScissor(int(x), int(fb_height - w), int(z - x), int(w - y))

                if imgui.INDEX_SIZE == 2:
                    gltype = GL.GL_UNSIGNED_SHORT
                else:
                    gltype = GL.GL_UNSIGNED_INT

                GL.glDrawElements(
                    GL.GL_TRIANGLES,
                    command.elem_count,
                    gltype,
                    ctypes.c_void_p(command.idx_offset * imgui.INDEX_SIZE),
                )


        # restore modified GL state
        restore_common_gl_state(common_gl_state_tuple)

        GL.glUseProgram(last_program)
        GL.glActiveTexture(last_active_texture)
        GL.glBindVertexArray(last_vertex_array)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, last_array_buffer)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, last_element_array_buffer)

    def _invalidate_device_objects(self):
        if self._vao_handle > -1:
            GL.glDeleteVertexArrays(1, [self._vao_handle])
        if self._vbo_handle > -1:
            GL.glDeleteBuffers(1, [self._vbo_handle])
        if self._elements_handle > -1:
            GL.glDeleteBuffers(1, [self._elements_handle])
        self._vao_handle = self._vbo_handle = self._elements_handle = 0

        GL.glDeleteProgram(self._shader_handle)
        self._shader_handle = 0

        if self._font_texture > -1:
            GL.glDeleteTextures([self._font_texture])
        self.io.fonts.tex_id = 0
        self._font_texture = 0


class FixedPipelineRenderer(BaseOpenGLRenderer):
    """Basic OpenGL integration base class."""

    def refresh_font_texture(self):
        # save texture state
        # last_texture = GL.glGetIntegerv(GL.GL_TEXTURE_BINDING_2D)
        # width, height, pixels = self.io.fonts.get_tex_data_as_alpha8()
        font_matrix = self.io.fonts.get_tex_data_as_rgba32()
        assert isinstance(font_matrix, ndarray)
        width = font_matrix.shape[1]
        height = font_matrix.shape[0]
        pixels = font_matrix.data

        if self._font_texture is not None:
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
        # GL.glBindTexture(GL.GL_TEXTURE_2D, last_texture)
        self.io.fonts.clear_tex_data()

    def _create_device_objects(self):
        pass

    def render(self, draw_data):
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

            GL.glVertexPointer(
                2,
                GL.GL_FLOAT,
                imgui.VERTEX_SIZE,
                ctypes.c_void_p(
                    commands.vtx_buffer.data_address() + imgui.VERTEX_BUFFER_POS_OFFSET
                ),
            )
            GL.glTexCoordPointer(
                2,
                GL.GL_FLOAT,
                imgui.VERTEX_SIZE,
                ctypes.c_void_p(
                    commands.vtx_buffer.data_address() + imgui.VERTEX_BUFFER_UV_OFFSET
                ),
            )
            GL.glColorPointer(
                4,
                GL.GL_UNSIGNED_BYTE,
                imgui.VERTEX_SIZE,
                ctypes.c_void_p(
                    commands.vtx_buffer.data_address() + imgui.VERTEX_BUFFER_COL_OFFSET
                ),
            )

            for command in commands.cmd_buffer:
                GL.glBindTexture(GL.GL_TEXTURE_2D, command.texture_id)

                x, y, z, w = command.clip_rect
                GL.glScissor(int(x), int(fb_height - w), int(z - x), int(w - y))

                if imgui.INDEX_SIZE == 2:
                    gltype = GL.GL_UNSIGNED_SHORT
                else:
                    gltype = GL.GL_UNSIGNED_INT

                GL.glDrawElements(
                    GL.GL_TRIANGLES,
                    command.elem_count,
                    gltype,
                    ctypes.c_void_p(command.idx_offset * imgui.INDEX_SIZE),
                )


        restore_common_gl_state(common_gl_state_tuple)

        GL.glDisableClientState(GL.GL_COLOR_ARRAY)
        GL.glDisableClientState(GL.GL_TEXTURE_COORD_ARRAY)
        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix()
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glPopMatrix()
        GL.glPopAttrib()

    def _invalidate_device_objects(self):
        if self._font_texture > -1:
            GL.glDeleteTextures([self._font_texture])
        self.io.fonts.texture_id = 0
        self._font_texture = 0


def get_common_gl_state():
    """
    Backups the current OpenGL state
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
    return (
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


def restore_common_gl_state(common_gl_state_tuple):
    """
    Takes a tuple after calling function `get_common_gl_state`,
    to set the given OpenGL state back as it was before rendering the UI
    """
    (
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
    ) = common_gl_state_tuple

    GL.glBindTexture(GL.GL_TEXTURE_2D, last_texture)
    GL.glBlendEquationSeparate(last_blend_equation_rgb, last_blend_equation_alpha)
    GL.glBlendFunc(last_blend_src, last_blend_dst)

    GL.glPolygonMode(GL.GL_FRONT_AND_BACK, last_front_and_back_polygon_mode)

    if last_enable_blend:
        GL.glEnable(GL.GL_BLEND)
    else:
        GL.glDisable(GL.GL_BLEND)

    if last_enable_cull_face:
        GL.glEnable(GL.GL_CULL_FACE)
    else:
        GL.glDisable(GL.GL_CULL_FACE)

    if last_enable_depth_test:
        GL.glEnable(GL.GL_DEPTH_TEST)
    else:
        GL.glDisable(GL.GL_DEPTH_TEST)

    if last_enable_scissor_test:
        GL.glEnable(GL.GL_SCISSOR_TEST)
    else:
        GL.glDisable(GL.GL_SCISSOR_TEST)

    GL.glScissor(
        last_scissor_box[0],
        last_scissor_box[1],
        last_scissor_box[2],
        last_scissor_box[3],
    )
    GL.glViewport(
        last_viewport[0], last_viewport[1], last_viewport[2], last_viewport[3]
    )
