# -*- coding: utf-8 -*-

from typing import Callable, Final, Iterable, List, NamedTuple, Optional, Tuple, Union

from imgui_bundle import imgui

MenuCallable = Callable[[], None]


class MenuItem(NamedTuple):
    name: str
    callback: Optional[MenuCallable]
    enabled: bool


MenuItemLike = Union[
    MenuItem,
    str,
    Tuple[str],
    Tuple[str, Optional[MenuCallable]],
    Tuple[str, Optional[MenuCallable], bool],
]


def normalize_menu_items(*items: MenuItemLike) -> List[MenuItem]:
    result = list()

    for item in items:
        if isinstance(item, MenuItem):
            result.append(item)
        elif isinstance(item, str):
            result.append(MenuItem(item, None, True))
        elif isinstance(item, (tuple, list)):
            name = str(item[0]) if 1 <= len(item) else str()
            callback = item[1] if 2 <= len(item) else None
            enabled = bool(item[2]) if 3 <= len(item) else True
            result.append(MenuItem(name, callback, enabled))
        else:
            raise ValueError(f"Invalid menu item type: '{type(item).__name__}'")

    return result


class MenuList(List[MenuItem]):
    SEPARATOR_PREFIX: Final[str] = "--"

    def __init__(self, *items: MenuItemLike, separator_prefix=SEPARATOR_PREFIX):
        super().__init__(normalize_menu_items(*items))
        self._separator_prefix = separator_prefix

    @classmethod
    def from_iterable(
        cls,
        items: Iterable[MenuItemLike],
        *,
        separator_prefix=SEPARATOR_PREFIX,
    ):
        return cls(*items, separator_prefix=separator_prefix)

    def do_process(self) -> None:
        for menu in self:
            name = menu.name
            callback = menu.callback
            enabled = menu.enabled

            if name and name.startswith(self._separator_prefix):
                imgui.separator()
                continue

            if callback is None:
                imgui.begin_menu(name, enabled=False)
                continue

            if imgui.begin_menu(name, enabled):
                try:
                    callback()
                finally:
                    imgui.end_menu()
