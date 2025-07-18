# -*- coding: utf-8 -*-
# https://docs.python.org/ko/3.13/library/codecs.html#error-handlers

from enum import StrEnum, auto, unique


@unique
class CodecErrorHandling(StrEnum):

    # The following error handlers can be used with all
    # Python Standard Encodings codecs:

    strict = auto()
    ignore = auto()
    replace_ = "replace"
    backslashreplace = auto()
    surrogateescape = auto()

    # The following error handlers are only applicable to encoding
    # (within text encodings):

    xmlcharrefreplace = auto()
    namereplace = auto()

    # In addition, the following error handler is specific to the given codecs:

    surrogatepass = auto()
