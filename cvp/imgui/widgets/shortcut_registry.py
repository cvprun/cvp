# -*- coding: utf-8 -*-

from typing import Callable, Dict, Optional

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

    def make(self, label: str, callback: Optional[Callable[[], None]] = None):
        return self._Builder(self, label, callback)

    def do_process(self) -> bool:
        for shortcut in self.values():
            if shortcut():
                return True
        return False
