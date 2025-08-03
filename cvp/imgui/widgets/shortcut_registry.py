# -*- coding: utf-8 -*-

from typing import Callable, Dict, Optional

from cvp.imgui.menu_item import MenuItemResult, menu_item
from cvp.imgui.widgets.shortcut import Shortcut
from cvp.imgui.widgets.shortcut_builder import ShortcutBuilder
from cvp.types.override import override


class ShortcutRegistry(Dict[str, Shortcut]):

    class _Builder(ShortcutBuilder):
        def __init__(
            self,
            registry: "ShortcutRegistry",
            label: str,
            callback: Optional[Callable[[], None]] = None,
        ):
            super().__init__(label=label, callback=callback)
            self._registry = registry

        @override
        def build(self) -> Shortcut:
            item = super().build()
            self._registry[item.label] = item
            return item

    def get_shortcut_label(self, key: str) -> str:
        return self.__getitem__(key).label

    def build(self, label: str, callback: Optional[Callable[[], None]] = None):
        return self._Builder(self, label, callback)

    def do_process(self) -> bool:
        for shortcut in self.values():
            if shortcut.__call__():
                return True
        return False

    def menu_item(
        self,
        label: str,
        selected=False,
        enabled=True,
        *,
        key: Optional[str] = None,
        check_keyboard_shortcut=False,
    ) -> MenuItemResult:
        if not key:
            key = label
        assert isinstance(key, str)

        shortcut = self.__getitem__(key)

        menu_result = menu_item(
            label=label,
            selected=selected,
            shortcut=shortcut.as_shortcut_text(),
            enabled=enabled,
        )

        clicked = menu_result.clicked
        if not clicked and check_keyboard_shortcut:
            clicked = shortcut.__call__()

        return MenuItemResult(clicked=clicked, state=menu_result.state)
