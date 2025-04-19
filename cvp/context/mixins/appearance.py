# -*- coding: utf-8 -*-

from typing import Any, Optional, Type

from cvp.context.mixins._base import BaseContextMixin
from cvp.types.colors import RGBA


class AppearanceMixin(BaseContextMixin):
    def get_selected_submenu(self, cls: Type, *, suffix: Optional[Any] = None) -> str:
        return self._config.appearance.get_selected_submenu(cls, suffix=suffix)

    def set_selected_submenu(
        self,
        cls: Type,
        value: str,
        *,
        suffix: Optional[Any] = None,
    ) -> None:
        self._config.appearance.set_selected_submenu(cls, value, suffix=suffix)

    @property
    def clear_color(self):
        return self._config.appearance.clear_color

    @clear_color.setter
    def clear_color(self, color: RGBA) -> None:
        self._config.appearance.clear_color = color

    @property
    def detail_color(self):
        return self._config.appearance.detail_color

    @detail_color.setter
    def detail_color(self, color: RGBA) -> None:
        self._config.appearance.detail_color = color

    @property
    def success_color(self):
        return self._config.appearance.success_color

    @success_color.setter
    def success_color(self, color: RGBA) -> None:
        self._config.appearance.success_color = color

    @property
    def normal_color(self):
        return self._config.appearance.normal_color

    @normal_color.setter
    def normal_color(self, color: RGBA) -> None:
        self._config.appearance.normal_color = color

    @property
    def warning_color(self):
        return self._config.appearance.warning_color

    @warning_color.setter
    def warning_color(self, color: RGBA) -> None:
        self._config.appearance.warning_color = color

    @property
    def error_color(self):
        return self._config.appearance.error_color

    @error_color.setter
    def error_color(self, color: RGBA) -> None:
        self._config.appearance.error_color = color
