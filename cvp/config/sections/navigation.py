# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, NamedTuple, NewType, Optional, Type, Union

from cvp.itertools.find_index import find_index
from cvp.variables import MODULE_PATH_SEPARATOR, NOT_FOUND_INDEX

CategoryKey = NewType("CategoryKey", str)


class RecentItem(NamedTuple):
    value: str
    accessed_at: str


@dataclass
class NavigationConfig:
    selected_submenus: Dict[CategoryKey, str] = field(default_factory=dict)
    recent_items: Dict[CategoryKey, List[RecentItem]] = field(default_factory=dict)

    @staticmethod
    def generate_category_key(
        cls: Type,
        *,
        suffix: Optional[Any] = None,
        separator=MODULE_PATH_SEPARATOR,
    ) -> CategoryKey:
        prefix = cls.__module__ + separator + cls.__name__
        key = prefix + separator + str(suffix) if suffix is not None else prefix
        return CategoryKey(key)

    def get_selected_submenu(self, cls: Type, *, suffix: Optional[Any] = None) -> str:
        category_key = self.generate_category_key(cls, suffix=suffix)
        return self.selected_submenus.get(category_key, str())

    def set_selected_submenu(
        self,
        cls: Type,
        value: str,
        *,
        suffix: Optional[Any] = None,
    ) -> None:
        category_key = self.generate_category_key(cls, suffix=suffix)
        self.selected_submenus[category_key] = value

    def find_recent_index(
        self,
        cls: Type,
        value: str,
        *,
        suffix: Optional[Any] = None,
    ) -> int:
        category_key = self.generate_category_key(cls, suffix=suffix)
        items = self.recent_items.get(category_key)
        if not items:
            return NOT_FOUND_INDEX

        return find_index(items, key=lambda x: x == value)

    def get_recent_items(
        self,
        cls: Type,
        *,
        suffix: Optional[Any] = None,
    ) -> List[RecentItem]:
        category_key = self.generate_category_key(cls, suffix=suffix)
        items = self.recent_items.get(category_key)
        if not items:
            items = list()
            self.recent_items[category_key] = items
        assert isinstance(items, list)
        return items

    def add_recent_item(
        self,
        cls: Type,
        value: str,
        accessed_at: Optional[Union[datetime, str]] = None,
        *,
        suffix: Optional[Any] = None,
    ) -> None:
        if accessed_at is None:
            accessed_at = datetime.now().astimezone().isoformat()
        elif isinstance(accessed_at, datetime):
            accessed_at = accessed_at.isoformat()
        assert isinstance(accessed_at, str)

        category_key = self.generate_category_key(cls, suffix=suffix)
        items = self.recent_items.get(category_key)
        if not items:
            self.recent_items[category_key] = [RecentItem(value, accessed_at)]
            return

        assert isinstance(items, list)
        index = self.find_recent_index(cls, value, suffix=suffix)
        if index != NOT_FOUND_INDEX:
            assert 0 <= index < len(items)
            items.pop(index)

        items.append(RecentItem(value, accessed_at))
