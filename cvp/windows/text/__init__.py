# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.config.sections.text import TextWindowConfig
from cvp.imgui.menu_item_ex import menu_item
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override


class TextWindow(WindowBase[TextWindowConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.text_window,
            title="Text Editor",
            closable=True,
            flags=None,
            modifiable_title=True,
        )
        self._label = "##TextEditor"
        self._content = ""
        self._length = -1
        self._width = 0
        self._height = 0
        self._flags = imgui.INPUT_TEXT_ALLOW_TAB_INPUT

    @override
    def on_process(self) -> None:
        changed, text_content = imgui.input_text_multiline(
            self._label,
            self._content,
            self._length,
            self._width,
            self._height,
            self._flags,
        )
        assert isinstance(changed, bool)
        assert isinstance(text_content, str)
        if changed:
            self._content = text_content
        self.on_popup_menu()

    def on_popup_menu(self):
        if not imgui.begin_popup_context_window().opened:
            return

        try:
            imgui.separator()
            if menu_item("Close"):
                self.opened = False
        finally:
            imgui.end_popup()
