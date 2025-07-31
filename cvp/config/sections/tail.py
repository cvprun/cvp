# -*- coding: utf-8 -*-

import encodings
from dataclasses import dataclass

from cvp.encoding.errors import CodecErrorHandling
from cvp.variables import INFINITE


@dataclass
class TailConfig:
    encoding: str = "utf-8"
    errors: str = "strict"
    lines: int = INFINITE

    @property
    def normalize_encoding(self) -> str:
        return encodings.normalize_encoding(self.encoding)

    @property
    def codec_error_handling(self) -> CodecErrorHandling:
        try:
            return CodecErrorHandling(self.errors)
        except:  # noqa
            return CodecErrorHandling.strict
