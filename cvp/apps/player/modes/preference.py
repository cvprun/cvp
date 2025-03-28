# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Callable

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.containers.immutable_list import ImmutableList
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.imgui.theme import THEME_NAMES, apply_theme_with_name
from cvp.logging.logging import logger
from cvp.msgs.msg import Msg
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.variables import (
    DEFAULT_MAIN_LABEL,
    DEFAULT_MENU_LABEL,
    DEFAULT_MENU_WIDTH,
    FULL_SIZE,
    NOT_FOUND_INDEX,
)


class PreferenceMode(BaseMode):
    _menus: OrderedDict[str, Callable[[], None]]

    def __init__(self, context: RendererContext):
        super().__init__(context)

        self._theme_names = ImmutableList(THEME_NAMES)

        self._menus = OrderedDict()
        self._menus["Appearance"] = self.on_appearance

    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.preference

    @override
    def on_main_menu(self) -> None:
        pass

    @override
    def do_event(self, event: Event) -> bool:
        return False

    @override
    def do_msg(self, msg: Msg) -> bool:
        return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @property
    def selected(self) -> str:
        return self.context.config.preference_manager.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.context.config.preference_manager.selected = value

    @override
    def do_process(self) -> None:
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()
        finally:
            imgui.pop_style_var()

    def do_child_process(
        self,
        menu_label=DEFAULT_MENU_LABEL,
        main_label=DEFAULT_MAIN_LABEL,
        split_x=DEFAULT_MENU_WIDTH,
    ):
        with begin_child_context(menu_label, split_x, child_flags=RESIZE_X | BORDERS):
            if imgui.begin_list_box("###MenuList", FULL_SIZE):
                try:
                    for key in self._menus.keys():
                        if imgui.selectable(key, key == self.selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context(main_label):
            if main_callback := self._menus.get(self.selected):
                imgui.text(self.selected)
                imgui.separator()

                main_callback()
            else:
                text_centered("Please select a item")

    # ----------------------------------------------------------------------------------
    # [Appearance] ---------------------------------------------------------------------

    @property
    def theme(self) -> str:
        return self.context.config.appearance.theme

    @theme.setter
    def theme(self, value: str) -> None:
        self.context.config.appearance.theme = value

    @property
    def theme_index(self) -> int:
        try:
            return self._theme_names.index(self.theme)
        except ValueError:
            return NOT_FOUND_INDEX

    def on_appearance(self) -> None:
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
                self.theme = theme_name

        imgui.show_font_selector("Font")
