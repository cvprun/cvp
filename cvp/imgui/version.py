# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Tuple

from imgui_bundle import imgui


@lru_cache
def version() -> Tuple[int, int, int]:
    numbers = list(map(lambda x: int(x.strip()), imgui.get_version().split(".")))
    major = numbers[0] if 1 <= len(numbers) else 0
    minor = numbers[1] if 2 <= len(numbers) else 0
    patch = numbers[2] if 3 <= len(numbers) else 0
    return major, minor, patch
