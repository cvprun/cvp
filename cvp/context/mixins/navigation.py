# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional, Type

from cvp.context.mixins._base import BaseContextMixin


class NavigationMixin(BaseContextMixin):
    def get_opened_window(self, cls: Type, *, suffix: Optional[Any] = None) -> bool:
        return self._config.navigation.get_opened_window(cls, suffix=suffix)

    def set_opened_window(
        self,
        cls: Type,
        value: bool,
        *,
        suffix: Optional[Any] = None,
    ) -> None:
        self._config.navigation.set_opened_window(cls, value, suffix=suffix)

    def get_selected_submenu(self, cls: Type, *, suffix: Optional[Any] = None) -> str:
        return self._config.navigation.get_selected_submenu(cls, suffix=suffix)

    def set_selected_submenu(
        self,
        cls: Type,
        value: str,
        *,
        suffix: Optional[Any] = None,
    ) -> None:
        self._config.navigation.set_selected_submenu(cls, value, suffix=suffix)

    def get_recent_items(self, cls: Type, *, suffix: Optional[Any] = None):
        return self._config.navigation.get_recent_items(cls, suffix=suffix)

    def add_recent_item(
        self,
        cls: Type,
        value: str,
        accessed_at: Optional[datetime] = None,
        *,
        suffix: Optional[Any] = None,
    ) -> None:
        self._config.navigation.add_recent_item(cls, value, accessed_at, suffix=suffix)
