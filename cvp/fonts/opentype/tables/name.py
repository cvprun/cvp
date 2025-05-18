# -*- coding: utf-8 -*-
# https://learn.microsoft.com/en-us/typography/opentype/spec/name

from types import MappingProxyType
from typing import Final, NamedTuple, Optional

FONT_FAMILY_NAME_ID: Final[int] = 1
FONT_SUBFAMILY_NAME_ID: Final[int] = 2

NAME_IDS: Final[MappingProxyType[int, str]] = MappingProxyType(
    {
        0: "Copyright notice",
        1: "Font Family name",
        2: "Font Subfamily name",  # e.g. Bold
        3: "Unique font identifier",
        4: "Full font name",
        5: "Version string",
        6: "PostScript name for the font",
        7: "Trademark",
        8: "Manufacturer Name",
        9: "Designer",
        10: "Description",
        11: "URL of Vendor",
        12: "URL of Designer",
        13: "License Description",
        14: "License Info URL",
        15: "Reserved",
        16: "Typographic Family name",
        17: "Typographic Subfamily name",
        18: "Compatible Full",  # Macintosh only
        19: "Sample text",
        20: "PostScript CID findfont name",
        21: "WWS Family Name",
        22: "WWS Subfamily Name",
        23: "Light Background Palette",
        24: "Dark Background Palette",
        25: "Variations PostScript Name Prefix",
    }
)

UNICODE_PLATFORM_ID: Final[int] = 0
MACINTOSH_PLATFORM_ID: Final[int] = 1
WINDOWS_PLATFORM_ID: Final[int] = 3

PLATFORM_IDS: Final[MappingProxyType[int, str]] = MappingProxyType(
    {
        UNICODE_PLATFORM_ID: "Unicode",
        MACINTOSH_PLATFORM_ID: "Macintosh",
        WINDOWS_PLATFORM_ID: "Windows",
    }
)

UNICODE_PLATFORM_ENCODING_IDS: Final[MappingProxyType[int, str]] = MappingProxyType(
    {
        0: "Unicode 1.0 semantics",
        1: "Unicode 1.1 semantics",
        2: "ISO/IEC 10646 semantics",
        3: "Unicode 2.0 and onwards semantics, Unicode BMP only",
        4: "Unicode 2.0 and onwards semantics, Unicode full repertoire",
    }
)

MACINTOSH_PLATFORM_ENCODING_IDS: Final[MappingProxyType[int, str]] = MappingProxyType(
    {
        0: "Roman",
        1: "Japanese",
        2: "Chinese (Traditional)",
        3: "Korean",
        4: "Arabic",
        5: "Hebrew",
        6: "Greek",
        7: "Russian",
        8: "RSymbol",
        9: "Devanagari",
        10: "Gurmukhi",
        11: "Gujarati",
        12: "Odia",
        13: "Bangla",
        14: "Tamil",
        15: "Telugu",
        16: "Kannada",
        17: "Malayalam",
        18: "Sinhalese",
        19: "Burmese",
        20: "Khmer",
        21: "Thai",
        22: "Laotian",
        23: "Georgian",
        24: "Armenian",
        25: "Chinese (Simplified)",
        26: "Tibetan",
        27: "Mongolian",
        28: "Geez",
        29: "Slavic",
        30: "Vietnamese",
        31: "Sindhi",
        32: "Uninterpreted",
    }
)

# Macintosh language IDs
# For information on Macintosh platform-specific language IDs,
# consult Apple’s TrueType Reference Manual.
# https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html

WINDOWS_PLATFORM_ENCODING_IDS: Final[MappingProxyType[int, str]] = MappingProxyType(
    {
        0: "Symbol",
        1: "Unicode BMP",
        2: "ShiftJIS",
        3: "PRC",
        4: "Big5",
        5: "Wansung",
        6: "Johab",
        7: "Reserved",
        8: "Reserved",
        9: "Reserved",
        10: "Unicode full repertoire",
    }
)


class NameRecord(NamedTuple):
    # uint16   | platformID   | Platform ID.
    # uint16   | encodingID   | Platform-specific encoding ID.
    # uint16   | languageID   | Language ID.
    # uint16   | nameID       | Name ID.
    # uint16   | length       | String length (in bytes).
    # Offset16 | stringOffset | String offset from start of storage area (in bytes).

    platform_id: int
    encoding_id: int
    language_id: int
    name_id: int
    value: str

    @property
    def platform(self) -> Optional[str]:
        """
        Other platform IDs have been defined for use only in the 'cmap' table.
        """
        return PLATFORM_IDS.get(self.platform_id)

    @property
    def encoding(self) -> Optional[str]:
        if self.platform_id == UNICODE_PLATFORM_ID:
            return UNICODE_PLATFORM_ENCODING_IDS.get(self.encoding_id)
        elif self.platform_id == MACINTOSH_PLATFORM_ID:
            return MACINTOSH_PLATFORM_ENCODING_IDS.get(self.encoding_id)
        elif self.platform_id == WINDOWS_PLATFORM_ID:
            return WINDOWS_PLATFORM_ENCODING_IDS.get(self.encoding_id)
        else:
            return None

    @property
    def name_description(self) -> Optional[str]:
        return NAME_IDS.get(self.name_id)

    def __repr__(self):
        return (
            f"<{type(self).__name__}"
            f" Platform={self.platform_id}"
            f",Encoding={self.encoding_id}"
            f",Language={self.language_id}"
            f",NameID={self.name_id}"
            f",Value={self.value}"
            ">"
        )
