# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType
from typing import Final, Optional

from imgui_bundle import imgui, imgui_color_text_edit

from cvp.text.item import TextItem


def _create_palette_map():
    return {
        "Mariana": imgui_color_text_edit.TextEditor.get_mariana_palette(),
        "Dark": imgui_color_text_edit.TextEditor.get_dark_palette(),
        "Light": imgui_color_text_edit.TextEditor.get_light_palette(),
        "RetroBlue": imgui_color_text_edit.TextEditor.get_retro_blue_palette(),
    }


def _create_languages():
    return [
        imgui_color_text_edit.TextEditor.LanguageDefinition.c_plus_plus(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.hlsl(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.glsl(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.python(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.c(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.sql(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.angel_script(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.lua(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.c_sharp(),
        imgui_color_text_edit.TextEditor.LanguageDefinition.json(),
    ]


@lru_cache
def palette_map():
    return MappingProxyType(_create_palette_map())


@lru_cache
def language_map():
    return MappingProxyType({lang.m_name: lang for lang in _create_languages()})


class TextEditor:

    PALETTE_MAP = palette_map()
    LANGUAGE_MAP = language_map()

    DEFAULT_PALETTE: Final[str] = "Mariana"
    DEFAULT_LANGUAGE: Final[str] = "Python"

    def __init__(self, item: TextItem, text: Optional[str] = None):
        self._item = item
        self._editor = imgui_color_text_edit.TextEditor()
        self._editor.set_language_definition(self._get_language(self._item.language))
        self._editor.set_palette(self._get_palette(self._item.palette))

        if text is None:
            text = str()
        assert isinstance(text, str)

        self._editor.set_text(text)
        self._initial_text = text
        self._modified = False

    @classmethod
    def _get_palette(cls, name: str):
        try:
            return cls.PALETTE_MAP[name]
        except:  # noqa
            return cls.PALETTE_MAP[cls.DEFAULT_PALETTE]

    @classmethod
    def _get_language(cls, name: str):
        try:
            return cls.LANGUAGE_MAP[name]
        except:  # noqa
            return cls.LANGUAGE_MAP[cls.DEFAULT_LANGUAGE]

    @property
    def language_name(self) -> str:
        return self._editor.get_language_definition_name()

    @language_name.setter
    def language_name(self, value: str) -> None:
        self._editor.set_language_definition(self._get_language(value))
        self._item.language = value

    @property
    def palette_name(self) -> str:
        return self._item.palette

    @palette_name.setter
    def palette_name(self, value: str) -> None:
        self._editor.set_palette(self.PALETTE_MAP[value])
        self._item.palette = value

    @property
    def palette(self):
        return self._editor.get_palette()

    @property
    def initial_text(self) -> str:
        return self._initial_text

    @initial_text.setter
    def initial_text(self, text: str) -> None:
        self._initial_text = text

    @property
    def encoding(self) -> str:
        return self._item.encoding

    @property
    def errors(self) -> str:
        return self._item.errors

    @property
    def label(self) -> str:
        return self._item.get_label(modified=self.modified)

    @property
    def text(self) -> str:
        return self._editor.get_text()

    @text.setter
    def text(self, text: str) -> None:
        self._editor.set_text(text)

    @property
    def has_path(self) -> bool:
        return bool(self._item.path)

    @property
    def path(self) -> str:
        return self._item.path

    @path.setter
    def path(self, value: str) -> None:
        self._item.path = value

    @property
    def uuid(self) -> str:
        return self._item.uuid

    @property
    def encoded_text(self) -> bytes:
        return self.text.encode(self.encoding, self.errors)

    @property
    def modified(self) -> bool:
        return self._modified

    def commit(self) -> None:
        self._initial_text = self._editor.get_text()
        self._modified = False
        self._editor.set_text(self._initial_text)

    @property
    def show_tabs(self) -> bool:
        return self._editor.is_showing_short_tab_glyphs()

    @show_tabs.setter
    def show_tabs(self, value: bool) -> None:
        self._editor.set_show_short_tab_glyphs(value)

    @property
    def show_whitespaces(self) -> bool:
        return self._editor.is_showing_whitespaces()

    @show_whitespaces.setter
    def show_whitespaces(self, value: bool) -> None:
        self._editor.set_show_whitespaces(value)

    @property
    def readonly(self) -> bool:
        return self._editor.is_read_only()

    @readonly.setter
    def readonly(self, value: bool) -> None:
        self._editor.set_read_only(value)

    @property
    def line(self) -> int:
        return self._editor.get_cursor_position().m_line

    @property
    def column(self) -> int:
        return self._editor.get_cursor_position().m_column

    def can_undo(self) -> bool:
        return self._editor.can_undo()

    def can_redo(self) -> bool:
        return self._editor.can_redo()

    def undo(self, steps=1) -> None:
        self._editor.undo(steps)

    def redo(self, steps=1) -> None:
        self._editor.redo(steps)

    def copy(self) -> None:
        self._editor.copy()

    def cut(self) -> None:
        self._editor.cut()

    def paste(self) -> None:
        self._editor.paste()

    def delete(self, word_mode=False) -> None:
        self._editor.delete(word_mode)

    @property
    def has_selection(self) -> bool:
        return self._editor.has_selection()

    def select_all(self) -> None:
        self._editor.select_all()

    def render(
        self,
        title: Optional[str] = None,
        parent_is_focused=False,
        size: Optional[imgui.ImVec2Like] = None,
        border=False,
    ) -> bool:
        if title is None:
            if self.uuid:
                title = type(self).__name__ + "###" + self.uuid
            else:
                title = type(self).__name__
        assert isinstance(title, str)
        return self._editor.render(title, parent_is_focused, size, border)

    def do_process(self) -> None:
        if not self._modified:
            if self._editor.is_text_changed():
                self._modified = self._initial_text != self._editor.get_text()
        self.render()
