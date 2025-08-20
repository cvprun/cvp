# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

from cvp.terminal.style import TerminalStyle


class SgrText(NamedTuple):
    text: str
    style: TerminalStyle
    error: Optional[str] = None
