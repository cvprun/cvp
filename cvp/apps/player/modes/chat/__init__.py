# -*- coding: utf-8 -*-

from typing import Final, List

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import CHAT
from cvp.chat.cache import ChatCache
from cvp.chat.ids import INVALID_CONVERSATION_ID
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.calc_input_text_with_button_size import calc_input_multiline_text_size
from cvp.imgui.combo import combo_fitting_items_max_width
from cvp.imgui.fit_size import FIT_SIZE, FIT_WIDTH
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import (
    CTRL_ENTER_FOR_NEW_LINE,
    ENTER_RETURNS_TRUE,
    READ_ONLY,
)
from cvp.imgui.input_text_multiline import input_text_multiline
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.spinner import spinner
from cvp.imgui.text_centered import text_centered
from cvp.imgui.text_right_align import text_disabled_right_align
from cvp.ollama.ollama import OllamaKey
from cvp.types.override import override
from cvp.variables import (
    CHAT_TITLE_NONAME,
    NOT_FOUND_INDEX,
    OLLAMA_MODEL_NAME_SEPARATOR,
)


class ChatMode(BaseMode):
    __cvp_mode_name__ = "Chat"
    __cvp_mode_icon__ = CHAT

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
        self._input_text = str()
        self._search = str()
        self._conversation_id = INVALID_CONVERSATION_ID
        self._title_noname = CHAT_TITLE_NONAME
        self._enter_label = "Enter"

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def combo_models(
        self,
        *,
        separator=OLLAMA_MODEL_NAME_SEPARATOR,
        double_hash="##",
    ) -> None:
        selected_server_key = self.context.config.chat.selected_server_key
        selected_model_name = self.context.config.chat.selected_model_name
        selected_index = NOT_FOUND_INDEX

        combo_names: List[str] = list()

        for key, ollama in self.context.ollamas.items():
            for model_name in ollama.model_names:
                if key == selected_server_key and model_name == selected_model_name:
                    selected_index = len(combo_names)
                combo_item = ollama.name + separator + model_name + double_hash + key
                combo_names.append(combo_item)

        result = combo_fitting_items_max_width("Model", selected_index, combo_names)
        if result.changed:
            selected_index = result.value
            selected_combo_item = combo_names[selected_index]

            item_label, item_key = selected_combo_item.split(double_hash, maxsplit=1)
            self.context.config.chat.selected_server_key = item_key

            _, model_name = item_label.split(separator, maxsplit=1)
            self.context.config.chat.selected_model_name = model_name

    def get_input_text_size(self) -> imgui.ImVec2:
        return calc_input_multiline_text_size(self._input_text, self._enter_label)

    def input_text_multilingual_with_button(self) -> None:
        disabled_input = self.context.get_ollama_chat_status().running

        with style_disable_input_context(cancel=not disabled_input):
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
                    self.request_chat_completion()

            imgui.same_line()
            if button(self._enter_label, disabled=disabled_input):
                assert not disabled_input
                self.request_chat_completion()

    def request_chat_completion(self) -> None:
        try:
            chat_config = self.context.config.chat
            server_key = OllamaKey(chat_config.selected_server_key)
            model_name = chat_config.selected_model_name

            self._conversation_id = self.context.request_ollama_chat_stream(
                conversation_id=self._conversation_id,
                server_key=server_key,
                model_name=model_name,
                content=self._input_text,
                images=None,
                stream=True,
            )
        finally:
            self._input_text = str()

    def do_child_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("###MenuList", FIT_SIZE):
                try:
                    if imgui.button(self._title_noname, (FIT_WIDTH, 0)):
                        self._conversation_id = INVALID_CONVERSATION_ID

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
            if self._conversation_id == INVALID_CONVERSATION_ID:
                imgui.text(self._title_noname)
            else:
                imgui.text(self.context.chat[self._conversation_id].conversation_title)

            imgui.separator()

            self.combo_models()

            imgui.separator()

            item_spacing_y = imgui.get_style().item_spacing.y * 2
            history_bottom = -1 * (self.get_input_text_size().y + item_spacing_y)

            with begin_child_context("Main", size=(0, history_bottom)):
                if self._conversation_id == INVALID_CONVERSATION_ID:
                    text_centered("What can I help with?")
                else:
                    self.do_history(self.context.chat[self._conversation_id])

            imgui.separator()
            self.input_text_multilingual_with_button()

    def do_history(self, cache: ChatCache) -> None:
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

            imgui.text(first_message.role)
            imgui.same_line()

            with style_disable_input_context():
                response_message = cache.get_merged_response_message(message.id)
                response_content = response_message.content
                assert response_content is not None
                imgui.text_wrapped(response_content)

                last_stream = streams[-1]
                last_created_at = last_stream.created_at.isoformat()
                text_disabled_right_align(last_created_at)

        if self.context.get_ollama_chat_status().running:
            spinner("Running")
