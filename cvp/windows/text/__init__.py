# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.config.sections.text import TextWindowConfig
from cvp.imgui.flags.input_text import ALLOW_TAB_INPUT
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
        self._size = 0, 0
        self._flags = ALLOW_TAB_INPUT

    @override
    def on_process(self) -> None:
        changed, text_content = imgui.input_text_multiline(
            self._label,
            self._content,
            self._size,
            self._flags,
        )
        assert isinstance(changed, bool)
        assert isinstance(text_content, str)
        if changed:
            self._content = text_content
        self.on_popup_menu()

    def on_popup_menu(self):
        if imgui.begin_popup_context_window():
            try:
                imgui.separator()
                if menu_item("Close"):
                    self.opened = False
            finally:
                imgui.end_popup()
