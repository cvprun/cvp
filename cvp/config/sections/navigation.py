# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, NamedTuple, NewType, Optional, Type, Union

from cvp.itertools.find_index import find_index
from cvp.variables import INFINITE, MODULE_PATH_SEPARATOR, NOT_FOUND_INDEX

CategoryKey = NewType("CategoryKey", str)


class RecentItem(NamedTuple):
    value: str
    accessed_at: str


@dataclass
class NavigationConfig:
    selected_submenus: Dict[CategoryKey, str] = field(default_factory=dict)

    recent_items: Dict[CategoryKey, List[RecentItem]] = field(default_factory=dict)
    recent_max: Dict[CategoryKey, int] = field(default_factory=dict)

    @staticmethod
    def generate_category_key(
        cls: Type,
        *,
        suffix: Optional[Any] = None,
        separator=MODULE_PATH_SEPARATOR,
    ) -> CategoryKey:
        prefix_text = cls.__module__ + separator + cls.__name__
        if suffix is not None:
            return CategoryKey(prefix_text + separator + str(suffix))
        else:
            return CategoryKey(prefix_text)

    def get_selected_submenu(self, cls: Type, *, suffix: Optional[Any] = None) -> str:
        category_key = self.generate_category_key(cls, suffix=suffix)
        return self.selected_submenus.get(category_key, str())

    def set_selected_submenu(self, cls: Type, value: str, *, suffix=None) -> None:
        category_key = self.generate_category_key(cls, suffix=suffix)
        self.selected_submenus[category_key] = value

    def has_selected_submenu(self, cls: Type, *, suffix=None) -> bool:
        return self.generate_category_key(cls, suffix=suffix) in self.selected_submenus

    def clear_selected_submenu(self, cls: Type, *, suffix=None) -> None:
        category_key = self.generate_category_key(cls, suffix=suffix)
        if category_key in self.selected_submenus:
            del self.selected_submenus[category_key]

    def get_recent_max(self, cls: Type, *, suffix: Optional[Any] = None) -> int:
        category_key = self.generate_category_key(cls, suffix=suffix)
        return self.recent_max.get(category_key, INFINITE)

    def set_recent_max(self, cls: Type, value: int, *, suffix=None) -> None:
        category_key = self.generate_category_key(cls, suffix=suffix)
        self.recent_max[category_key] = value

    def set_recent_infinite(self, cls: Type, *, suffix=None) -> None:
        self.set_recent_max(cls, INFINITE, suffix=suffix)

    def find_recent_index(self, cls: Type, value: str, *, suffix=None) -> int:
        category_key = self.generate_category_key(cls, suffix=suffix)
        items = self.recent_items.get(category_key)
        if items:
            return find_index(items, key=lambda x: x.value == value)
        else:
            return NOT_FOUND_INDEX

    def get_recent_items(self, cls: Type, *, suffix=None) -> List[RecentItem]:
        category_key = self.generate_category_key(cls, suffix=suffix)
        items = self.recent_items.get(category_key)
        if not items:
            items = list()
            self.recent_items[category_key] = items
        assert isinstance(items, list)
        return items

    def get_recent_values(self, cls: Type, *, suffix=None) -> List[str]:
        items = self.get_recent_items(cls, suffix=suffix)
        return [item.value for item in items]

    def add_recent_item(
        self,
        cls: Type,
        value: str,
        accessed_at: Optional[Union[datetime, str]] = None,
        *,
        suffix=None,
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

        recent_max = self.get_recent_max(cls, suffix=suffix)
        if recent_max < 0:
            pass
        elif recent_max == 0:
            if items:
                items.clear()
            return
        else:
            assert 0 < recent_max
            while recent_max <= len(items):
                items.pop(0)

        index = self.find_recent_index(cls, value, suffix=suffix)
        if index != NOT_FOUND_INDEX:
            assert 0 <= index < len(items)
            items.pop(index)

        items.append(RecentItem(value, accessed_at))
