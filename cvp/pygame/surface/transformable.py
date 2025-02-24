# -*- coding: utf-8 -*-

from abc import ABC
from typing import Literal, Optional, Sequence, Union

from pygame import transform as pg_transform
from pygame.surface import Surface
from pygame.typing import RectLike

from cvp.pygame.surface._property import SurfacePropertyInterface
from cvp.pygame.types import ColorValue, SequenceProtocol

SmoothscaleBackendLiteral = Literal["GENERIC", "SSE2", "NEON"]


class Transformable(SurfacePropertyInterface, ABC):
    def transform_flip(self, flip_x: bool, flip_y: bool):
        return pg_transform.flip(self.surface, flip_x, flip_y)

    def transform_scale(
        self,
        size: Sequence[float],
        dest_surface: Optional[Surface] = None,
    ):
        assert isinstance(size, SequenceProtocol)
        return pg_transform.scale(self.surface, size, dest_surface)

    def transform_scale_by(
        self,
        factor: Union[float, Sequence[float]],
        dest_surface: Optional[Surface] = None,
    ):
        assert isinstance(factor, float) or isinstance(factor, SequenceProtocol)
        return pg_transform.scale_by(self.surface, factor, dest_surface)

    def transform_rotate(self, angle: float):
        return pg_transform.rotate(self.surface, angle)

    def transform_rotozoom(self, angle: float, scale: float):
        return pg_transform.rotozoom(self.surface, angle, scale)

    def transform_scale2x(self, dest_surface: Optional[Surface] = None):
        return pg_transform.scale2x(self.surface, dest_surface)

    def transform_smoothscale(
        self,
        size: Sequence[float],
        dest_surface: Optional[Surface] = None,
    ):
        assert isinstance(size, SequenceProtocol)
        return pg_transform.smoothscale(self.surface, size, dest_surface)

    def transform_smoothscale_by(
        self,
        factor: Union[float, Sequence[float]],
        dest_surface: Optional[Surface] = None,
    ):
        assert isinstance(factor, float) or isinstance(factor, SequenceProtocol)
        return pg_transform.smoothscale_by(self.surface, factor, dest_surface)

    @staticmethod
    def transform_get_smoothscale_backend() -> str:
        return pg_transform.get_smoothscale_backend()

    @staticmethod
    def transform_set_smoothscale_backend(backend: SmoothscaleBackendLiteral):
        return pg_transform.set_smoothscale_backend(backend)

    def transform_chop(self, rect: RectLike):
        return pg_transform.chop(self.surface, rect)

    def transform_laplacian(self, dest_surface: Optional[Surface] = None):
        return pg_transform.laplacian(self.surface, dest_surface)

    def transform_box_blur(
        self,
        radius: int,
        repeat_edge_pixels=True,
        dest_surface: Optional[Surface] = None,
    ):
        return pg_transform.box_blur(
            self.surface,
            radius,
            repeat_edge_pixels,
            dest_surface,
        )

    def transform_gaussian_blur(
        self,
        radius: int,
        repeat_edge_pixels=True,
        dest_surface: Optional[Surface] = None,
    ):
        return pg_transform.gaussian_blur(
            self.surface,
            radius,
            repeat_edge_pixels,
            dest_surface,
        )

    @staticmethod
    def transform_average_surfaces(
        surfaces: Sequence[Surface],
        dest_surface: Optional[Surface] = None,
        palette_colors: Union[bool, int] = 1,
    ):
        assert isinstance(surfaces, SequenceProtocol)
        return pg_transform.average_surfaces(
            surfaces,
            dest_surface,
            palette_colors,
        )

    def transform_average_color(self, rect: RectLike, consider_alpha=False):
        return pg_transform.average_color(self.surface, rect, consider_alpha)

    def transform_invert(self, dest_surface: Optional[Surface] = None):
        return pg_transform.invert(self.surface, dest_surface)

    def transform_grayscale(self, dest_surface: Optional[Surface] = None):
        return pg_transform.grayscale(self.surface, dest_surface)

    def transform_threshold(
        self,
        dest_surface: Optional[Surface] = None,
        search_color: Optional[ColorValue] = None,
        threshold: ColorValue = (0, 0, 0, 0),
        set_color: Optional[ColorValue] = (0, 0, 0, 0),
        set_behavior=1,
        search_surf: Optional[Surface] = None,
        inverse_set=False,
    ):
        return pg_transform.threshold(
            dest_surface,
            self.surface,
            search_color,
            threshold,
            set_color,
            set_behavior,
            search_surf,
            inverse_set,
        )
