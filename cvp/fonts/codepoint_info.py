# -*- coding: utf-8 -*-

import unicodedata
from typing import Optional

from cvp.fonts.ttf import TTF


class CodepointInfo:
    def __init__(self, codepoint: int, ttf: Optional[TTF] = None):
        self.codepoint = codepoint
        self.character = chr(codepoint)
        self.category = str()
        self.combining = 0
        self.bidirectional = str()
        self.name = str()
        self.exists = False
        self.filepath = str()
        self.filename = str()
        self.glyph = str()

        try:
            self.category = unicodedata.category(self.character)
            self.combining = unicodedata.combining(self.character)
            self.bidirectional = unicodedata.bidirectional(self.character)
            self.name = unicodedata.name(self.character)
        except ValueError:
            pass

        if ttf is not None:
            self.exists = True
            self.filepath = str(ttf.path)
            self.filename = str(ttf.basename)
            self.glyph = ttf.get_best_camp().get(codepoint, str())

    def __bool__(self):
        return self.exists

    def as_printable_unicode(self) -> str:
        return f"\\U{self.codepoint:08X}"

    def as_unformatted_text(self):
        return (
            f"{self.character}\n"
            f"Codepoint: U+{self.codepoint:06X}\n"
            f"Name: {self.name}\n"
            f"Category: {self.category}\n"
            f"Combining: {self.combining}\n"
            f"Bidirectional: {self.bidirectional}\n"
            f"Glyph: {self.glyph}\n"
            f"Filename: {self.filename}\n"
        )
