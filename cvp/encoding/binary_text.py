# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Binary-to-text_encoding

from enum import StrEnum, auto, unique


@unique
class BinaryToTextEncodingMethod(StrEnum):
    base64 = auto()  # https://en.wikipedia.org/wiki/Base64
    mime = auto()  # https://en.wikipedia.org/wiki/MIME
    percent = auto()  # https://en.wikipedia.org/wiki/Percent-encoding
    quoted = auto()  # https://en.wikipedia.org/wiki/Quoted-printable
