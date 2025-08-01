# -*- coding: utf-8 -*-

import encodings
from dataclasses import dataclass

from cvp.encoding.errors import CodecErrorHandling
from cvp.variables import DEFAULT_STRING_ENCODING, DEFAULT_STRING_ERRORS


@dataclass
class EncodingConfig:
    encoding: str = DEFAULT_STRING_ENCODING
    errors: str = DEFAULT_STRING_ERRORS

    @property
    def normalize_encoding(self) -> str:
        return encodings.normalize_encoding(self.encoding)

    @property
    def codec_error_handling(self) -> CodecErrorHandling:
        try:
            return CodecErrorHandling(self.errors)
        except:  # noqa
            return CodecErrorHandling.strict

    @codec_error_handling.setter
    def codec_error_handling(self, value: CodecErrorHandling) -> None:
        self.errors = str(value)

    def encode(self, value: str) -> bytes:
        return value.encode(self.encoding, self.errors)

    def decode(self, value: bytes) -> str:
        return value.decode(self.encoding, self.errors)
