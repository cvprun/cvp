# -*- coding: utf-8 -*-

from imgui_bundle import imgui_color_text_edit

from cvp.text.item import TextItem


class TextEditor:
    def __init__(self, item: TextItem):
        self._item = item

        self._editor = imgui_color_text_edit.TextEditor()
        self._language = imgui_color_text_edit.TextEditor.LanguageDefinition()
        self._python_lang = imgui_color_text_edit.TextEditor.LanguageDefinition.python()
        self._editor.set_text("")
        self._editor.set_language_definition(self._python_lang)
        self._editor.set_palette(imgui_color_text_edit.TextEditor.get_dark_palette())

    def set_text(self, text: str) -> None:
        self._editor.set_text(text)

    def do_process(self) -> None:
        self._editor.render("Editor")
