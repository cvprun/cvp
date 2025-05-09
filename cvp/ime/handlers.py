# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.ime.interface import InputHandlerInterface


@lru_cache
def get_all_input_handler_types() -> Sequence[Type[InputHandlerInterface]]:
    from cvp.ime.sources.english import EnglishInputHandler
    from cvp.ime.sources.hangul.dubeolsik.handler import DubeolsikHangulInputHandler

    return EnglishInputHandler, DubeolsikHangulInputHandler
