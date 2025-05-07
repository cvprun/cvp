# -*- coding: utf-8 -*-

from typing import Union

from cvp.unicode.hangul.compatibility_jamo import is_hangul_compatibility_jamo_unicode
from cvp.unicode.hangul.jamo import is_hangul_jamo_unicode
from cvp.unicode.hangul.jamo_extended_a import is_hangul_jamo_extended_a_unicode
from cvp.unicode.hangul.jamo_extended_b import is_hangul_jamo_extended_b_unicode
from cvp.unicode.hangul.syllables import is_hangul_syllables_unicode


def is_hangul_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)

    if is_hangul_syllables_unicode(char):
        return True
    elif is_hangul_jamo_unicode(char):
        return True
    elif is_hangul_compatibility_jamo_unicode(char):
        return True
    elif is_hangul_jamo_extended_a_unicode(char):
        return True
    elif is_hangul_jamo_extended_b_unicode(char):
        return True
    else:
        return False
