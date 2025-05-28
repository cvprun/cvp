# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class TerminalCanvasOptions:
    pass


class TerminalCanvas:
    def __init__(self, label: str, options: Optional[TerminalCanvasOptions] = None):
        self._label = label
        self._options = options if options else TerminalCanvasOptions()
