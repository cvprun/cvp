# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def get_window_draw_list():
    return imgui.get_window_draw_list()


def get_foreground_draw_list():
    return imgui.get_foreground_draw_list()
