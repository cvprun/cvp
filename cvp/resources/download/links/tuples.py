# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Sequence, Tuple, Union
from urllib.parse import ParseResult

from cvp.hashfunc.checksum import Checksum


class ExtractPair(NamedTuple):
    archive_path: str
    extract_path: str


class LinkInfo(NamedTuple):
    url: Union[str, ParseResult]
    paths: Sequence[Union[Tuple[str, str], ExtractPair]]
    checksum: Optional[Union[str, Tuple[str, str], Checksum]]
