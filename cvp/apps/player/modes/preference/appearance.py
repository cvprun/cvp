# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.containers.immutable_list import ImmutableList
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.theme import THEME_NAMES, apply_theme_with_name
from cvp.logging.logging import logger
from cvp.renderer.context import Context
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX


class AppearancePreference(BasePreference):
    __cvp_menu_name__ = "Appearance"

    def __init__(self, context: Context):
        super().__init__(context)
        self._theme_names = ImmutableList(THEME_NAMES)

    @property
    def appearance_theme(self) -> str:
        return self.context.config.appearance.theme

    @appearance_theme.setter
    def appearance_theme(self, value: str) -> None:
        self.context.config.appearance.theme = value

    @property
    def theme_index(self) -> int:
        try:
            return self._theme_names.index(self.appearance_theme)
        except ValueError:
            return NOT_FOUND_INDEX

    @override
    def do_process(self) -> None:
        theme_result = imgui.combo("Theme", self.theme_index, self._theme_names)
        theme_changed, theme_index = theme_result
        assert isinstance(theme_changed, bool)
        assert isinstance(theme_index, int)

        if theme_changed and 0 <= theme_index < len(self._theme_names):
            try:
                theme_name = self._theme_names[theme_index]
                apply_theme_with_name(theme_name)
            except BaseException as e:
                logger.error(f"Changed theme error: {e}")
            else:
                logger.info(f"Changed theme: '{theme_name}'")
                self.appearance_theme = theme_name

        imgui.show_font_selector("Font")

        if color_result := color_edit4("Clear Color", *self.context.clear_color):
            self.context.clear_color = color_result.color

        if color_result := color_edit4("Detail Color", *self.context.detail_color):
            self.context.detail_color = color_result.color

        if color_result := color_edit4("Success Color", *self.context.success_color):
            self.context.success_color = color_result.color

        if color_result := color_edit4("Normal Color", *self.context.normal_color):
            self.context.normal_color = color_result.color

        if color_result := color_edit4("Warning Color", *self.context.warning_color):
            self.context.warning_color = color_result.color

        if color_result := color_edit4("Error Color", *self.context.error_color):
            self.context.error_color = color_result.color
