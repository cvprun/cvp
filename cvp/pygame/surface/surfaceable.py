# -*- coding: utf-8 -*-

from abc import ABC
from typing import Iterable, Optional, Sequence, Tuple, Union

from pygame.display import Info
from pygame.surface import Surface
from pygame.typing import RectLike

from cvp.pygame.literals import ViewKind
from cvp.pygame.surface._property import SurfacePropertyInterface
from cvp.pygame.types import ColorValue, Coordinate, SequenceProtocol

BlitSequence = Iterable[
    Union[
        Tuple[Surface, Union[Coordinate, RectLike]],
        Tuple[Surface, Union[Coordinate, RectLike], Union[RectLike, int]],
        Tuple[Surface, Union[Coordinate, RectLike], RectLike, int],
    ]
]


class Surfaceable(SurfacePropertyInterface, ABC):
    @staticmethod
    def surface_get_current_display_size():
        display_info = Info()
        return display_info.current_w, display_info.current_h

    @staticmethod
    def surface_from_empty(flags=0):
        return Surface((0, 0), flags)

    @staticmethod
    def surface_from_current_display_size():
        return Surface(Surfaceable.surface_get_current_display_size())

    @staticmethod
    def surface_from_args(
        size: Coordinate,
        flags=0,
        depth=0,
        masks: Optional[ColorValue] = None,
    ):
        return Surface(size, flags, depth, masks)

    @staticmethod
    def surface_from_surface(size: Coordinate, flags=0, *, surface: Surface):
        return Surface(size, flags, surface)

    def surface_blit(
        self,
        source: Surface,
        dest: RectLike,
        area: Optional[RectLike] = None,
        special_flags=0,
    ):
        return self.surface.blit(source, dest, area, special_flags)

    def surface_blits(
        self,
        blit_sequence: BlitSequence,
        doreturn: Union[int, bool] = 1,
    ):
        return self.surface.blits(blit_sequence, doreturn)

    def surface_fblits(
        self,
        blit_sequence: Iterable[Tuple[Surface, Union[Coordinate, RectLike]]],
        special_flags=0,
    ):
        return self.surface.fblits(blit_sequence, special_flags)

    def surface_convert(self):
        return self.surface.convert()

    def surface_convert_with_surface(self, surface: Surface):
        return self.surface.convert(surface)

    def surface_convert_with_depth(self, depth: int, flags=0):
        return self.surface.convert(depth, flags)

    def surface_convert_with_masks(self, masks: ColorValue, flags=0):
        return self.surface.convert(masks, flags)

    def surface_convert_alpha(self):
        return self.surface.convert_alpha()

    def surface_copy(self):
        return self.surface.copy()

    def surface_fill(
        self,
        color: ColorValue,
        rect: Optional[RectLike] = None,
        special_flags=0,
    ):
        return self.surface.fill(color, rect, special_flags)

    def surface_scroll(self, dx=0, dy=0):
        return self.surface.scroll(dx, dy)

    def surface_set_colorkey(self, color: ColorValue, flags=0):
        return self.surface.set_colorkey(color, flags)

    def surface_set_none_colorkey(self):
        return self.surface.set_colorkey(None)

    def surface_get_colorkey(self):
        return self.surface.get_colorkey()

    def surface_set_alpha(self, value: int, flags=0):
        return self.surface.set_alpha(value, flags)

    def surface_set_none_alpha(self):
        return self.surface.set_alpha(None)

    def surface_get_alpha(self):
        return self.surface.get_alpha()

    def surface_lock(self):
        return self.surface.lock()

    def surface_unlock(self):
        return self.surface.unlock()

    def surface_mustlock(self):
        return self.surface.mustlock()

    def surface_get_locked(self):
        return self.surface.get_locked()

    def surface_get_locks(self):
        return self.surface.get_locks()

    def surface_get_at(self, x_y: Coordinate):
        return self.surface.get_at(x_y)

    def surface_set_at(self, x_y: Coordinate, color: ColorValue):
        return self.surface.set_at(x_y, color)

    def surface_get_at_mapped(self, x_y: Coordinate):
        return self.surface.get_at_mapped(x_y)

    def surface_get_palette(self):
        return self.surface.get_palette()

    def surface_get_palette_at(self, index: int):
        return self.surface.get_palette_at(index)

    def surface_set_palette(self, palette: Sequence[ColorValue]):
        assert isinstance(palette, SequenceProtocol)
        return self.surface.set_palette(palette)

    def surface_set_palette_at(self, index: int, color: ColorValue):
        return self.surface.set_palette_at(index, color)

    def surface_map_rgb(self, color: ColorValue):
        return self.surface.map_rgb(color)

    def surface_unmap_rgb(self, mapped_int: int):
        return self.surface.unmap_rgb(mapped_int)

    def surface_set_clip(self, rect: Optional[RectLike]):
        return self.surface.set_clip(rect)

    def surface_get_clip(self):
        return self.surface.get_clip()

    def surface_subsurface(self, rect: RectLike):
        return self.surface.subsurface(rect)

    def surface_subsurface_with_coords(
        self,
        left_top: Coordinate,
        width_height: Coordinate,
    ):
        return self.surface.subsurface(left_top, width_height)

    def surface_subsurface_with_raws(
        self,
        left: float,
        top: float,
        width: float,
        height: float,
    ):
        return self.surface.subsurface(left, top, width, height)

    def surface_get_parent(self):
        return self.surface.get_parent()

    def surface_get_abs_parent(self):
        return self.surface.get_abs_parent()

    def surface_get_offset(self):
        return self.surface.get_offset()

    def surface_get_abs_offset(self):
        return self.surface.get_abs_offset()

    def surface_get_size(self):
        return self.surface.get_size()

    def surface_get_width(self):
        return self.surface.get_width()

    def surface_get_height(self):
        return self.surface.get_height()

    def surface_get_rect(self, **kwargs):
        return self.surface.get_rect(**kwargs)

    def surface_get_frect(self, **kwargs):
        return self.surface.get_frect(**kwargs)

    def surface_get_bitsize(self):
        return self.surface.get_bitsize()

    def surface_get_bytesize(self):
        return self.surface.get_bytesize()

    def surface_get_flags(self):
        return self.surface.get_flags()

    def surface_get_pitch(self):
        return self.surface.get_pitch()

    def surface_get_masks(self):
        return self.surface.get_masks()

    def surface_set_masks(self, color: ColorValue):
        return self.surface.set_masks(color)

    def surface_get_shifts(self):
        return self.surface.get_shifts()

    def surface_set_shifts(self, color: ColorValue):
        return self.surface.set_shifts(color)

    def surface_get_losses(self):
        return self.surface.get_losses()

    def surface_get_bounding_rect(self, min_alpha=1):
        return self.surface.get_bounding_rect(min_alpha)

    def surface_get_view(self, kind: ViewKind = "2"):
        return self.surface.get_view(kind)

    def surface_get_buffer(self):
        return self.surface.get_buffer()

    def surface_get_blendmode(self):
        return self.surface.get_blendmode()

    def surface_premul_alpha(self):
        return self.surface.premul_alpha()
