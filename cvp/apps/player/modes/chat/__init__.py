# -*- coding: utf-8 -*-

from io import StringIO

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.chat.cache import ChatCache
from cvp.config.sections.appearance import AppMode
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.combo import combo_fitting_items_max_width
from cvp.imgui.fit_size import FIT_SIZE, FIT_WIDTH
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import (
    CTRL_ENTER_FOR_NEW_LINE,
    ENTER_RETURNS_TRUE,
    READ_ONLY,
)
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.input_text_multilingual import input_text_multiline
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.imgui.text_right_align import text_disabled_right_align
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.variables import (
    CHAT_TITLE_NONAME,
    NOT_FOUND_INDEX,
    SIDE_MENU_WIDTH,
)


class ChatMode(BaseMode):
    def __init__(self, context: RendererContext):
        super().__init__(context)
        self._input_text = str()
        self._search = str()
        self._conversation_id = NOT_FOUND_INDEX
        self._title_noname = CHAT_TITLE_NONAME
        self._enter_label = "Enter"

    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.chat

    @property
    def chat_selected_index(self):
        return self.context.config.chat.selected_index

    @chat_selected_index.setter
    def chat_selected_index(self, value: int) -> None:
        self.context.config.chat.selected_index = value

    @property
    def disabled_input(self) -> bool:
        return self.context.get_ollama_chat_status().running

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
        result = combo_fitting_items_max_width(
            "###Models",
            current=self.chat_selected_index,
            items=self.context.chat_model_names,
        )
        if result.changed:
            self.chat_selected_index = result.value

    @staticmethod
    def calc_input_text_size(input_value: str, button_label: str) -> imgui.ImVec2:
        button_size = imgui.calc_text_size(button_label)
        button_width = button_size.x

        frame_padding = imgui.get_style().frame_padding
        item_spacing = imgui.get_style().item_spacing

        input_text_right = button_width + (frame_padding.x * 2) + item_spacing.x
        width = -1 * input_text_right

        line_count = input_value.count("\n") + 1
        text_height = imgui.get_font_size() * line_count
        height = text_height + (frame_padding.y * 2)

        return imgui.ImVec2(width, height)

    def get_input_text_size(self) -> imgui.ImVec2:
        return self.calc_input_text_size(self._input_text, self._enter_label)

    def input_text_multilingual_with_button(self) -> None:
        disabled_input = self.disabled_input

        with style_disable_input_context(cancel=not self.disabled_input):
            input_flags = CTRL_ENTER_FOR_NEW_LINE | ENTER_RETURNS_TRUE
            if disabled_input:
                input_flags |= READ_ONLY

            input_result = input_text_multiline(
                label="###UserInputText",
                value=self._input_text,
                size=self.get_input_text_size(),
                flags=input_flags,
            )

            if not disabled_input:
                self._input_text = input_result.value
                if input_result.changed:
                    self.request_user_input(self._input_text)
                    self._input_text = str()

            imgui.same_line()
            if button(self._enter_label, disabled=disabled_input):
                assert not disabled_input
                self.request_user_input(self._input_text)
                self._input_text = str()

    def request_user_input(self, text: str) -> None:
        self.context.request_chat_stream(
            self._conversation_id,
            self.context.config.chat.selected_server_key,
            self.context.config.chat.selected_model_name,
            text,
        )

    def do_child_process(self, split_x=SIDE_MENU_WIDTH):
        with begin_child_context("Menu", split_x, child_flags=RESIZE_X | BORDERS):
            if imgui.begin_list_box("###MenuList", FIT_SIZE):
                try:
                    if imgui.button(self._title_noname, (FIT_WIDTH, 0)):
                        self._conversation_id = NOT_FOUND_INDEX

                    search_result = input_text_multiline(
                        label="###Search",
                        value=self._search,
                        flags=CTRL_ENTER_FOR_NEW_LINE | ENTER_RETURNS_TRUE,
                    )
                    self._search = search_result.value
                    if search_result.changed:
                        pass

                    imgui.separator()

                    for conv_id, cache in self.context.chat.items():
                        selected = conv_id == self._conversation_id
                        if imgui.selectable(cache.label, selected)[1]:
                            self._conversation_id = conv_id
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if self._conversation_id == NOT_FOUND_INDEX:
                imgui.text(self._title_noname)
            else:
                imgui.text(self.context.chat[self._conversation_id].conversation_title)

            imgui.separator()

            self.combo_models()
            imgui.same_line()
            if imgui.button("Refresh"):
                self.context.refresh_chat_models()

            imgui.separator()

            item_spacing_y = imgui.get_style().item_spacing.y * 2
            history_bottom = -1 * (self.get_input_text_size().y + item_spacing_y)

            with begin_child_context("Main", 0, history_bottom):
                if self._conversation_id == NOT_FOUND_INDEX:
                    text_centered("What can I help with?")
                else:
                    self.do_history(self.context.chat[self._conversation_id])

            imgui.separator()
            self.input_text_multilingual_with_button()

    @staticmethod
    def do_history(cache: ChatCache) -> None:
        for message in cache.messages:
            request = message.load_request()
            imgui.text(request.role)
            imgui.same_line()
            with style_disable_input_context():
                content = request.content if request.content else str()
                imgui.text_wrapped(content.strip())

                created_at = message.created_at.isoformat()
                text_disabled_right_align(created_at)

            streams = cache.streams.get(message.id)
            if not streams:
                continue
            first_stream = streams[0]
            first_chunk = first_stream.load_chunk()
            first_message = first_chunk.message

            buffer = StringIO()
            buffer.write(first_message.content)
            for stream in streams[1:]:
                chunk = stream.load_chunk()
                assert first_message.role == chunk.message.role
                buffer.write(chunk.message.content)

            imgui.text(first_message.role)
            imgui.same_line()
            with style_disable_input_context():
                imgui.text_wrapped(buffer.getvalue().strip())

                created_at = first_stream.created_at.isoformat()
                text_disabled_right_align(created_at)
