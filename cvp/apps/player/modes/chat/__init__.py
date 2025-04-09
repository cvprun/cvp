# -*- coding: utf-8 -*-

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.chat.cache import ChatCache
from cvp.config.sections.appearance import AppMode
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.flags.combo import WIDTH_FIT_PREVIEW
from cvp.imgui.combo import combo
from cvp.imgui.footer_height_to_reserve import footer_height_to_reserve
from cvp.imgui.input_text_multilingual import input_text_multilingual
from cvp.imgui.input_text_multilingual_with_button import (
    input_text_multilingual_with_button,
)
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
    FULL_WIDTH,
    NOT_FOUND_INDEX,
)


class ChatMode(BaseMode):
    def __init__(self, context: RendererContext):
        super().__init__(context)
        self._input_text = str()
        self._search = str()
        self._conversation_id = NOT_FOUND_INDEX

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
    def chat_selected_index(self):
        return self.context.config.chat.selected_index

    @chat_selected_index.setter
    def chat_selected_index(self, value: int) -> None:
        self.context.config.chat.selected_index = value

    @override
    def do_process(self) -> None:
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()
        finally:
            imgui.pop_style_var()

    def combo_models(self) -> None:
        model_names = self.context.chat_model_names
        selected_index = self.chat_selected_index

        if 0 <= selected_index < len(model_names):
            preview_value = model_names[selected_index]
        else:
            preview_value = str()

        if imgui.begin_combo("###Models", preview_value, WIDTH_FIT_PREVIEW):
            try:
                for i, model_name in enumerate(model_names):
                    is_selected = selected_index == i
                    if imgui.selectable(model_name, is_selected)[0]:
                        self.chat_selected_index = i

                    # Set the initial focus when opening the combo
                    # (scrolling + keyboard navigation focus)
                    if is_selected:
                        imgui.set_item_default_focus()
            finally:
                imgui.end_combo()

    def do_child_process(
        self,
        menu_label=DEFAULT_MENU_LABEL,
        main_label=DEFAULT_MAIN_LABEL,
        split_x=DEFAULT_MENU_WIDTH,
    ):
        with begin_child_context(menu_label, split_x, child_flags=RESIZE_X | BORDERS):
            if imgui.begin_list_box("###MenuList", FULL_SIZE):
                try:
                    if imgui.button("New chat", (FULL_WIDTH, 0)):
                        self._conversation_id = NOT_FOUND_INDEX

                    search_result = input_text_multilingual(
                        label="###Search",
                        value=self._search,
                        size=(-1 * imgui.FLT_MIN, 0.0),
                        hint="Search chats",
                    )
                    if search_result.changed:
                        self._search = search_result.value

                    imgui.separator()

                    for conv_id, cache in self.context.chat.items():
                        selected = conv_id == self._conversation_id
                        if imgui.selectable(cache.label, selected)[1]:
                            self._conversation_id = conv_id
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context(main_label):
            self.combo_models()
            imgui.same_line()
            if imgui.button("Refresh"):
                self.context.refresh_chat_models()

            imgui.separator()

            history_bottom = -1 * footer_height_to_reserve()

            with begin_child_context(main_label, 0, history_bottom):
                if self._conversation_id == NOT_FOUND_INDEX:
                    text_centered("What can I help with?")
                else:
                    self.do_history(self.context.chat[self._conversation_id])

            imgui.separator()

            input_result, button_result = input_text_multilingual_with_button(
                label="###InputText",
                value=self._input_text,
                button_label="Enter",
                input_flags=ENTER_RETURNS_TRUE,
                input_hint="Ask anything",
            )
            self._input_text = input_result.value
            if input_result.changed:
                self._input_text = str()
            if button_result:
                self._input_text = str()

    def do_history(self, cache: ChatCache) -> None:
        if cache.is_unrequested:
            self.context.chat.refresh_messages(cache.id)

        for msg in cache.messages:
            request = msg.request if msg.request else str()
            imgui.bullet_text(request)
