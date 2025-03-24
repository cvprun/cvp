# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.draw_list.types import DrawList


def create_draw_list_with_shared_data() -> DrawList:
    return DrawList(imgui.get_draw_list_shared_data())
