# -*- coding: utf-8 -*-

import os
from functools import lru_cache

from cvp.assets import get_assets_dir


@lru_cache
def get_swaggers_dir() -> str:
    return os.path.join(get_assets_dir(), "swaggers")


@lru_cache
def get_swaggers_mediamtx_path() -> str:
    return os.path.join(get_swaggers_dir(), "mediamtx.json")
