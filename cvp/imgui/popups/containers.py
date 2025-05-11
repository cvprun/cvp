# -*- coding: utf-8 -*-

from typing import Any, List, Optional, Tuple

from cvp.imgui.popups.interface import PopupInterface


class PopupList(List[PopupInterface[Any]]):
    def do_process(self) -> Optional[Tuple[PopupInterface[Any], Any]]:
        for popup in self:
            result = popup.do_process()
            if result is not None:
                return popup, result
        return None
