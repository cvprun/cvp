# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Binary-to-text_encoding

import base64
import quopri
import sys
import urllib.parse
from enum import StrEnum, auto, unique
from functools import partial
from typing import Callable, Dict, Final, Union


@unique
class BinaryToText(StrEnum):
    base85 = auto()
    base64 = auto()  # https://en.wikipedia.org/wiki/Base64
    base32 = auto()
    base16 = auto()
    ascii85 = auto()
    z85 = auto()
    mime = auto()  # https://en.wikipedia.org/wiki/MIME
    percent = auto()  # https://en.wikipedia.org/wiki/Percent-encoding
    quoted_printable = auto()  # https://en.wikipedia.org/wiki/Quoted-printable


# fmt:off
if (3, 13) <= sys.version_info:
    _z85encode = base64.z85encode  # noqa
    _z85decode = base64.z85decode  # noqa
else:
    def _z85encode(_):
        raise NotImplementedError("Added in python version 3.13")

    def _z85decode(_):
        raise NotImplementedError("Added in python version 3.13")
# fmt:on


def _mime_encode(_):
    raise NotImplementedError


def _mime_decode(_):
    raise NotImplementedError


def _percent_encode(bs: Union[bytes, bytearray]) -> bytes:
    return urllib.parse.quote_from_bytes(bs).encode(encoding="utf-8")


def _percent_decode(bs: Union[str, bytes, bytearray]) -> bytes:
    return urllib.parse.unquote_to_bytes(bs)


_BINARY_TO_TEXT_ENCODING_FUNCS: Final[Dict[BinaryToText, Callable]] = {
    BinaryToText.base85: partial(base64.b85encode, pad=False),
    BinaryToText.base64: partial(base64.b64encode, altchars=None),
    BinaryToText.base32: base64.b32encode,
    BinaryToText.base16: base64.b16encode,
    BinaryToText.ascii85: base64.a85encode,
    BinaryToText.z85: _z85encode,
    BinaryToText.mime: _mime_encode,
    BinaryToText.percent: _percent_encode,
    BinaryToText.quoted_printable: partial(quopri.encodestring, header=False),
}

_BINARY_TO_TEXT_DECODING_FUNCS: Final[Dict[BinaryToText, Callable]] = {
    BinaryToText.base85: base64.b85decode,
    BinaryToText.base64: partial(base64.b64decode, altchars=None, validate=False),
    BinaryToText.base32: base64.b32encode,
    BinaryToText.base16: base64.b16encode,
    BinaryToText.ascii85: base64.a85decode,
    BinaryToText.z85: _z85decode,
    BinaryToText.mime: _mime_decode,
    BinaryToText.percent: _percent_decode,
    BinaryToText.quoted_printable: partial(quopri.decodestring, header=False),
}


def binary_to_text_encoding(method: BinaryToText, data: bytes, encoding="utf-8") -> str:
    result = _BINARY_TO_TEXT_ENCODING_FUNCS[method](data)
    assert isinstance(result, bytes)
    return str(result, encoding=encoding)


def binary_to_text_decoding(method: BinaryToText, data: str) -> bytes:
    result = _BINARY_TO_TEXT_DECODING_FUNCS[method](data)
    assert isinstance(result, bytes)
    return result
