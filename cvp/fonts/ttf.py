# -*- coding: utf-8 -*-

import os
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Dict, List, Optional, Union

from fontTools.ttLib import TTFont

from cvp.fonts.opentype.tables.name import (
    FONT_FAMILY_NAME_ID,
    FONT_SUBFAMILY_NAME_ID,
    WINDOWS_PLATFORM_ID,
    NameRecord,
)
from cvp.fonts.ranges import BlockRange, CodepointRange, read_ranges
from cvp.variables import CODEPOINT_RANGES_EXTENSION, UNICODE_SINGLE_BLOCK_SIZE


class TTF:
    def __init__(self, path: Path, ttf: TTFont):
        self._path = path
        self._ttfont = ttf

    @classmethod
    def from_filepath(cls, path: Union[str, PathLike[str]]):
        path = path if isinstance(path, Path) else Path(path)
        assert isinstance(path, Path)
        return cls(path, TTFont(path))

    def close(self) -> None:
        self._ttfont.close()

    @property
    def path(self):
        return self._path

    @property
    def basename(self):
        return os.path.basename(self._path)

    @property
    def ttfont(self):
        return self._ttfont

    @property
    def cmap(self):
        """Character to Glyph Index Mapping Table"""
        return self._ttfont["cmap"]

    @property
    def head(self):
        """Font Header Table"""
        return self._ttfont["head"]

    @property
    def hhea(self):
        """Horizontal Header Table"""
        return self._ttfont["hhea"]

    @property
    def hmtx(self):
        """Horizontal Metrics Table"""
        return self._ttfont["hmtx"]

    @property
    def name(self):
        """Naming Table"""
        return self._ttfont["name"]

    @property
    def os2(self):
        """OS/2 and Windows Metrics Table"""
        return self._ttfont["OS/2"]

    @property
    def vhea(self):
        """Vertical Header Table"""
        return self._ttfont["vhea"]

    @property
    def vmtx(self):
        """Vertical Metrics Table"""
        return self._ttfont["vmtx"]

    @property
    def fvar(self):
        """Font Variations Table"""
        return self._ttfont["fvar"]

    @property
    def units_per_em(self) -> Optional[int]:
        """Units per em square (typically 1000 or 2048)"""
        try:
            return self.head.unitsPerEm
        except AttributeError:
            return None

    @property
    def ascent(self) -> Optional[int]:
        """Vertical ascent value (usually for top baseline alignment)"""
        try:
            return self.hhea.ascent
        except AttributeError:
            return None

    @property
    def descent(self) -> Optional[int]:
        """Vertical descent value (usually negative, for bottom alignment)"""
        try:
            return self.hhea.descent
        except AttributeError:
            return None

    @property
    def line_gap(self) -> Optional[int]:
        """Additional space between lines"""
        try:
            return self.hhea.lineGap
        except AttributeError:
            return None

    @property
    def typo_ascender(self) -> Optional[int]:
        """Typographic ascender height"""
        try:
            return self.os2.sTypoAscender
        except AttributeError:
            return None

    @property
    def typo_descender(self) -> Optional[int]:
        """Typographic descender depth"""
        try:
            return self.os2.sTypoDescender
        except AttributeError:
            return None

    @property
    def typo_line_gap(self) -> Optional[int]:
        """Typographic line gap"""
        try:
            return self.os2.sTypoLineGap
        except AttributeError:
            return None

    @property
    def x_height(self) -> Optional[int]:
        """Height of lowercase 'x'"""
        try:
            return self.os2.sxHeight
        except AttributeError:
            return None

    @property
    def cap_height(self) -> Optional[int]:
        """Height of capital 'H'"""
        try:
            return self.os2.sCapHeight
        except AttributeError:
            return None

    @property
    def names(self):
        result = list()
        for record in self.name.names:
            item = NameRecord(
                record.platformID,
                record.platEncID,
                record.langID,
                record.nameID,
                record.toUnicode(),
            )
            result.append(item)
        return result

    @property
    def font_family_name(self):
        for record in self.name.names:
            if record.platformID != WINDOWS_PLATFORM_ID:
                continue
            if record.nameID != FONT_FAMILY_NAME_ID:
                continue
            return record.toUnicode()
        return str()

    @property
    def font_subfamily_name(self):
        for record in self.name.names:
            if record.platformID != WINDOWS_PLATFORM_ID:
                continue
            if record.nameID != FONT_SUBFAMILY_NAME_ID:
                continue
            return record.toUnicode()
        return str()

    @property
    def is_monospace(self) -> bool:
        return self.os2.panose.bProportion == 9

    @property
    def is_variable(self) -> bool:
        return "fvar" in self._ttfont

    def get_glyph_order(self) -> List[str]:
        return self.ttfont.getGlyphOrder()

    def get_best_camp(self) -> Dict[int, str]:
        return self._ttfont.getBestCmap()

    def get_glyph_mtx(self) -> Dict[int, str]:
        return self._ttfont.getBestCmap()

    def validate_monospace(self):
        widths = set(self.hmtx[name][0] for name in self.get_glyph_order())
        if 0 == len(widths):
            raise ValueError("Glyph does not exist")
        if 1 < len(widths):
            raise ValueError("Font is not monospace")

    def get_character_map(self) -> Dict[int, str]:
        items = self.cmap.getBestCmap().items()
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
