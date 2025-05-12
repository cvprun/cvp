# -*- coding: utf-8 -*-

from typing import List


def parse_integer_ranges(text: str) -> List[int]:
    result = list()
    for part in text.split(","):
        if "-" in part:
            start, end = part.split("-")
            result.extend(list(range(int(start), int(end) + 1)))
        else:
            result.append(int(part))
    return list(result)
