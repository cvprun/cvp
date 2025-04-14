# -*- coding: utf-8 -*-

from typing import Optional

from hgtk.text import compose, decompose


class HangulInputHandler:
    def __init__(self, text: Optional[str] = None, composing: Optional[str] = None):
        self._text = text if text else str()
        self._composing = composing if composing else str()

    @staticmethod
    def compose(text: str):
        return compose(text)

    @staticmethod
    def decompose(text: str):
        return decompose(text)
