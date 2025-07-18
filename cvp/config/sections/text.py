# -*- coding: utf-8 -*-

from dataclasses import dataclass
from encodings import normalize_encoding

from cvp.encoding.errors import CodecErrorHandling


@dataclass
class TextConfig:
    default_encoding: str = "utf-8"
    default_error_handling: str = "strict"

    @property
    def normalize_default_encoding(self) -> str:
        return normalize_encoding(self.default_encoding)

    @property
    def default_codec_error_handling(self) -> CodecErrorHandling:
        try:
            return CodecErrorHandling(self.default_error_handling)
        except:  # noqa
            return CodecErrorHandling.strict
