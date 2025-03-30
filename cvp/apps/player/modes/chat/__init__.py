# -*- coding: utf-8 -*-

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.footer_height_to_reserve import footer_height_to_reserve
from cvp.imgui.input_text_ko import input_text_ko
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.msgs.msg import Msg
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.variables import (
    DEFAULT_MAIN_LABEL,
    DEFAULT_MENU_LABEL,
    DEFAULT_MENU_WIDTH,
    FULL_SIZE,
)


class ChatMode(BaseMode):
    def __init__(self, context: RendererContext):
        super().__init__(context)
        self._input_text = str()

    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.chat

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
    def chat_ollama_url(self) -> str:
        return self.context.config.chat.ollama_url

    @chat_ollama_url.setter
    def chat_ollama_url(self, value: str) -> None:
        self.context.config.chat.ollama_url = value

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
                    text_centered("Please select a item")
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context(main_label):
            history_bottom = -1 * footer_height_to_reserve()

            with begin_child_context(main_label, 0, history_bottom):
                text_centered("Please select a item")

            imgui.separator()

            enter_text = "Enter"
            enter_text_size = imgui.calc_text_size(enter_text)
            enter_text_width = enter_text_size.x
            frame_padding = imgui.get_style().frame_padding
            frame_padding_x = frame_padding.x
            item_spacing = imgui.get_style().item_spacing
            item_spacing_x = item_spacing.x

            input_text_right = enter_text_width + (frame_padding_x * 2) + item_spacing_x
            imgui.set_next_item_width(-1 * input_text_right)
            text_result = input_text_ko(
                "###InputText",
                self._input_text,
                flags=ENTER_RETURNS_TRUE,
            )
            text_changed = text_result[0]
            self._input_text = text_result[1]
            if text_changed:
                self._input_text = str()

            imgui.same_line()
            if imgui.button(enter_text):
                pass
