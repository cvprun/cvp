# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.config.sections.flow.logs import Logs


def calc_log_names_combo_width(logs: Logs) -> float:
    level_name_lens = list(map(lambda x: len(x), logs.level_names))
    level_name = logs.level_names[level_name_lens.index(max(level_name_lens))]
    max_text_width = imgui.calc_text_size(level_name)[0]
    padding_width = imgui.get_style().item_spacing[0] * 2
    return max_text_width + padding_width + logs.dropdown_width
