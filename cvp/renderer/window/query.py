# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.flags import focused, hovered


class WindowQuery:
    def __init__(self):
        self._expanded = False
        self._opened = False
        self._appearing = False
        self._focused = False
        self._hovered = False
        self._x = 0.0
        self._y = 0.0
        self._w = 0.0
        self._h = 0.0

    def update(self, expanded: bool, opened: bool):
        self._expanded = expanded
        self._opened = opened
        self._appearing = imgui.is_window_appearing()
        self._focused = imgui.is_window_focused(focused.ROOT_AND_CHILD_WINDOWS)
        self._hovered = imgui.is_window_hovered(hovered.ROOT_AND_CHILD_WINDOWS)
        self._x, self._y = imgui.get_window_pos()
        self._w, self._h = imgui.get_window_size()

    @property
    def expanded(self):
        return self._expanded

    @property
    def opened(self):
        return self._opened

    @property
    def appearing(self):
        return self._appearing

    @property
    def focused(self):
        return self._focused

    @property
    def hovered(self):
        return self._hovered

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def position(self):
        return self._x, self._y

    @property
    def size(self):
        return self._w, self._h

    @property
    def roi(self):
        return self._x, self._y, self._x + self._w, self._y + self._h
