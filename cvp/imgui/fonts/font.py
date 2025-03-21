# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# noinspection PyProtectedMember
from imgui.core import _Font
from imgui_bundle import imgui

from cvp.fonts.cached_ttf import CachedTTF
from cvp.fonts.codepoint_info import CodepointInfo
from cvp.gl.texture import Texture


@dataclass
class Font:
    font: _Font
    family: str
    size: int
    block_step: int
    ttfs: List[CachedTTF] = field(default_factory=list)
    blocks: List[Tuple[int, int]] = field(default_factory=list)
    texture: Optional[Texture] = None
    cp_infos: Dict[int, CodepointInfo] = field(default_factory=dict)

    def __str__(self):
        return f"{self.family} ({self.size}px)"

    def __enter__(self):
        imgui.push_font(self.font)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        imgui.pop_font()

    def find_cached_ttf(self, codepoint: int) -> CachedTTF:
        for ttf in self.ttfs:
            if ttf.has_codepoint(codepoint):
                return ttf
        raise ValueError(f"Could not find ttf with codepoint: {codepoint}")

    def get_cached_ttf(self, codepoint: int) -> Optional[CachedTTF]:
        try:
            return self.find_cached_ttf(codepoint)
        except ValueError:
            return None

    def get_codepoint_info(self, codepoint: int) -> CodepointInfo:
        cp_info = self.cp_infos.get(codepoint)
        if cp_info is None:
            ttf = self.get_cached_ttf(codepoint)
            ttf = ttf.ttf if ttf is not None else None
            cp_info = CodepointInfo(codepoint, ttf)
            self.cp_infos[codepoint] = cp_info
        return cp_info

    def close(self) -> None:
        if self.texture is not None:
            self.texture.close()
