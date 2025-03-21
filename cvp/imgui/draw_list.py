# -*- coding: utf-8 -*-

# noinspection PyProtectedMember
from imgui.core import _DrawList as DrawList
from imgui_bundle import imgui


def create_empty_draw_list():
    return DrawList()


def get_window_draw_list():
    draw_list = imgui.get_window_draw_list()
    assert isinstance(draw_list, DrawList)
    return draw_list


def get_foreground_draw_list():
    draw_list = imgui.get_foreground_draw_list()
    assert isinstance(draw_list, DrawList)
    return draw_list
