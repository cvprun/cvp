# -*- coding: utf-8 -*-

import encodings
from dataclasses import dataclass, field
from typing import List

from cvp.encoding.errors import CodecErrorHandling


@dataclass
class TextConfig:
    encoding: str = "utf-8"
    errors: str = "strict"
    tabs_order: List[str] = field(default_factory=list)

    @property
    def normalize_encoding(self) -> str:
        return encodings.normalize_encoding(self.encoding)

    @property
    def codec_error_handling(self) -> CodecErrorHandling:
        try:
            return CodecErrorHandling(self.errors)
        except:  # noqa
            return CodecErrorHandling.strict
