# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/ANSI_escape_code#Fe_Escape_sequences

from typing import Final, Union

FE_ESCAPE_SEQUENCE_BEGIN: Final[int] = 0x40
FE_ESCAPE_SEQUENCE_END: Final[int] = 0x5F


def is_fe_escape_sequence(control_code: Union[int, str]) -> bool:
    if isinstance(control_code, str):
        control_code = ord(control_code)
    assert isinstance(control_code, int)

    return FE_ESCAPE_SEQUENCE_BEGIN <= control_code <= FE_ESCAPE_SEQUENCE_END
