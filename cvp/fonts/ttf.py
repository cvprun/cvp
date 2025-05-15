# -*- coding: utf-8 -*-

import os
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Dict, List, Optional, Union

from fontTools.ttLib import TTFont

from cvp.fonts.ranges import BlockRange, CodepointRange, read_ranges
from cvp.variables import CODEPOINT_RANGES_EXTENSION, UNICODE_SINGLE_BLOCK_SIZE


class TTF:
    def __init__(self, path: Path, ttf: TTFont):
        self._path = path
        self._ttf = ttf

    @classmethod
    def from_filepath(cls, path: Union[str, PathLike[str]]):
        path = path if isinstance(path, Path) else Path(path)
        assert isinstance(path, Path)
        return cls(path, TTFont(path))

    @property
    def path(self):
        return self._path

    @property
    def basename(self):
        return os.path.basename(self._path)

    @property
    def ttf(self):
        return self._ttf

    def close(self) -> None:
        self._ttf.close()

    def get_best_camp(self) -> Dict[int, str]:
        return self._ttf.getBestCmap()

    def get_character_map(self) -> Dict[int, str]:
        items = self._ttf["cmap"].getBestCmap().items()
        return {codepoint: glyph_name for codepoint, glyph_name in items}

    def get_codepoints(self, *, sorting=False, reverse=False) -> List[int]:
        result = list(self.get_character_map().keys())
        if sorting:
            result.sort(reverse=reverse)
        return result

    def get_glyph_ranges(self) -> List[CodepointRange]:
        result = list()

        begin: Optional[int] = None
        end: Optional[int] = None

        for codepoint in self.get_codepoints(sorting=True):
            if begin is None:
                assert end is None
                begin = codepoint
                end = codepoint
                continue

            assert end is not None
            if end + 1 == codepoint:
                end = codepoint
                continue

            assert end + 2 <= codepoint
            result.append(CodepointRange(begin, end))
            begin = codepoint
            end = codepoint

        if begin is not None:
            assert end is not None
            result.append(CodepointRange(begin, end))

        return result

    def get_block_ranges(self, step=UNICODE_SINGLE_BLOCK_SIZE) -> List[BlockRange]:
        result = set()
        for cp_range in self.get_glyph_ranges():
            for block_range in cp_range.as_blocks(step):
                result.add(block_range)
        return list(sorted(result, key=lambda x: x[0]))

    def get_default_ranges_path(self) -> Path:
        return Path(os.path.splitext(self.path)[0] + CODEPOINT_RANGES_EXTENSION)

    def write_ranges(self, path: Union[str, PathLike[str]]) -> int:
        path = path if isinstance(path, Path) else Path(path)
        assert isinstance(path, Path)
        buffer = StringIO()
        for begin, end in self.get_glyph_ranges():
            buffer.write(f"0x{begin:06x} 0x{end:06x}\n")
        return path.write_text(buffer.getvalue())

    def write_default_ranges(self) -> int:
        return self.write_ranges(self.get_default_ranges_path())

    def read_default_ranges(self) -> List[CodepointRange]:
        return read_ranges(self.get_default_ranges_path())

    def write_glyphs(self, path: Union[str, PathLike[str]]) -> int:
        path = path if isinstance(path, Path) else Path(path)
        assert isinstance(path, Path)
        buffer = StringIO()
        for codepoint, glyph_name in self.get_character_map().items():
            buffer.write(f"0x{codepoint:06x} {glyph_name}\n")
        return path.write_text(buffer.getvalue())

    def write_glyphs_python(self, path: Union[str, PathLike[str]]) -> int:
        path = path if isinstance(path, Path) else Path(path)
        assert isinstance(path, Path)
        symbols = set()
        buffer = StringIO()
        buffer.write("# -*- coding: utf-8 -*-\n\n")
        for codepoint, glyph_name in self.get_character_map().items():
            symbol = glyph_name.upper().replace("-", "_")
            assert symbol.isidentifier()
            symbol_base = symbol
            symbol_index = 1
            while symbol in symbols:
                symbol = f"{symbol_base}_{symbol_index}"
                symbol_index += 1
            symbols.add(symbol)
            buffer.write(f'{symbol} = "\\U{codepoint:08x}"\n')
        return path.write_text(buffer.getvalue())
