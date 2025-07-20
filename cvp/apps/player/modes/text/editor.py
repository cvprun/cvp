# -*- coding: utf-8 -*-

from imgui_bundle import imgui_color_text_edit

from cvp.context.context import Context
from cvp.imgui.tab_container import TabItem
from cvp.text.item import TextKey


class TextEditorTab(TabItem):
    def __init__(self, context: Context, key: TextKey):
        super().__init__(callback=self.do_process)
        self._context = context
        self._key = key

        self._editor = imgui_color_text_edit.TextEditor()
        self._language = imgui_color_text_edit.TextEditor.LanguageDefinition()
        self._python_lang = imgui_color_text_edit.TextEditor.LanguageDefinition.python()
        self._editor.set_text("")
        self._editor.set_language_definition(self._python_lang)
        self._editor.set_palette(imgui_color_text_edit.TextEditor.get_dark_palette())

    def do_process(self) -> None:
        self._editor.render("Editor")
