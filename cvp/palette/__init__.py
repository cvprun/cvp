# -*- coding: utf-8 -*-

from functools import lru_cache, reduce
from importlib import import_module
from types import ModuleType
from typing import Dict, Final, List, Optional

from cvp.types.colors import RGB


def _palette_filter(module: ModuleType, key: str) -> bool:
    if not key.isupper():
        return False

    value = getattr(module, key)
    if not isinstance(value, tuple):
        return False

    if len(value) != 3:
        return False

    if not isinstance(value[0], float):
        return False
    if not isinstance(value[1], float):
        return False
    if not isinstance(value[2], float):
        return False

    assert 0 <= value[0] <= 1.0
    assert 0 <= value[1] <= 1.0
    assert 0 <= value[2] <= 1.0
    return True


def _load_palette_from_module(module: ModuleType) -> Dict[str, RGB]:
    keys = list(filter(lambda x: _palette_filter(module, x), dir(module)))
    return {k: getattr(module, k) for k in keys}


@lru_cache
def _module_suffix() -> str:
    return "" if __name__ == "__main__" else __name__ + "."


def _load_palette_from_module_name(module_name: str):
    module = import_module(_module_suffix() + module_name)
    return _load_palette_from_module(module)


_basic: Final[str] = "basic"
_css4: Final[str] = "css4"
_extended: Final[str] = "extended"
_flat: Final[str] = "flat"
_tableau: Final[str] = "tableau"
_vga: Final[str] = "vga"
_xkcd: Final[str] = "xkcd"


@lru_cache
def basic_palette():
    return _load_palette_from_module_name(_basic)


@lru_cache
def css4_palette():
    return _load_palette_from_module_name(_css4)


@lru_cache
def extended_palette():
    return _load_palette_from_module_name(_extended)


@lru_cache
def flat_palette():
    return _load_palette_from_module_name(_flat)


@lru_cache
def tableau_palette():
    return _load_palette_from_module_name(_tableau)


@lru_cache
def vga_palette():
    return _load_palette_from_module_name(_vga)


@lru_cache
def xkcd_palette():
    return _load_palette_from_module_name(_xkcd)


@lru_cache
def global_palette_map() -> Dict[str, Dict[str, RGB]]:
    result = dict()
    result[_basic] = basic_palette()
    result[_css4] = css4_palette()
    result[_extended] = extended_palette()
    result[_flat] = flat_palette()
    result[_tableau] = tableau_palette()
    result[_vga] = vga_palette()
    result[_xkcd] = xkcd_palette()
    return result


@lru_cache
def registered_palette_keys() -> List[str]:
    return list(global_palette_map().keys())


@lru_cache
def registered_color_count() -> int:
    return reduce(lambda x, y: x + len(y), global_palette_map().values(), 0)


def find_named_color(key: str, *, sep=":") -> Optional[RGB]:
    keys = key.split(sep, 1)
    if len(keys) == 2:
        palette_key = keys[0]
        color_key = keys[1]
    else:
        assert len(keys) == 1
        palette_key = _extended
        color_key = keys[0]

    palette_key = palette_key.lower().strip()
    color_key = color_key.upper().strip().replace(" ", "_")

    palette = global_palette_map().get(palette_key)
    return palette.get(color_key) if palette is not None else None
