# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import List, Sequence, Type

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.context.context import Context


@lru_cache
def create_canvas_tool_window_types() -> Sequence[Type[BaseWindow]]:
    from cvp.apps.player.modes.main.canvas.props import PropsCanvasWindow

    return (PropsCanvasWindow,)


def create_canvas_tool_windows(context: Context) -> List[WindowInterface]:
    window_types = create_canvas_tool_window_types()
    return list(wt(context) for wt in window_types)
