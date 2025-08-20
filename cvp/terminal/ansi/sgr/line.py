# -*- coding: utf-8 -*-

from typing import Iterable, List, Optional

from cvp.terminal.ansi.sgr.text import SgrText


class SgrLine(List[SgrText]):
    def __init__(self, lineno: int, __iterable: Optional[Iterable[SgrText]] = None):
        super().__init__(__iterable or ())
        self.lineno = lineno
