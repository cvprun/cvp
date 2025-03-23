# -*- coding: utf-8 -*-

from typing import List

from cvp.fonts.ranges import CodepointRange, flatten_ranges


def create_glyph_ranges(ranges: List[CodepointRange]) -> List[int]:
    if ranges:
        # [IMPORTANT]
        # The NULL character is a special character used as a termination character
        # and should not be used.
        if ranges[0].begin == 0:
            if ranges[0].end == 0:
                # If the range is 0x00 to 0x00, remove the element.
                ranges = ranges[1:]
            else:
                assert ranges[0].begin + 1 <= ranges[0].end
                first_element = CodepointRange(ranges[0].begin + 1, ranges[0].end)
                ranges = [first_element] + ranges[1:]

    glyph_ranges = flatten_ranges(ranges)
    assert len(glyph_ranges) % 2 == 0

    # GlyphRanges must be terminated with a NULL (0) element.
    glyph_ranges.append(0)

    return glyph_ranges
