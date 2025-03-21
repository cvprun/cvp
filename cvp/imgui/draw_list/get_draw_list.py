# -*- coding: utf-8 -*-

# noinspection PyProtectedMember
from imgui.core import _DrawList
from imgui_bundle import imgui


def get_window_draw_list():
    draw_list = imgui.get_window_draw_list()
    assert isinstance(draw_list, _DrawList)
    return draw_list


def get_foreground_draw_list():
    draw_list = imgui.get_foreground_draw_list()
    assert isinstance(draw_list, _DrawList)
    return draw_list
