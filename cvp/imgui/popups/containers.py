# -*- coding: utf-8 -*-

from typing import Any, Iterable, List, Optional, Tuple

from cvp.imgui.popups.interface import PopupInterface


class PopupList(List[PopupInterface[Any]]):
    def __init__(self, *popups: PopupInterface[Any]):
        super().__init__(popups)

    @classmethod
    def from_iterable(cls, popups: Iterable[PopupInterface[Any]]):
        return cls(*popups)

    def do_process(self) -> Optional[Tuple[PopupInterface[Any], Any]]:
        for popup in self:
            result = popup.on_process()
            if result is not None:
                return popup, result
        return None
