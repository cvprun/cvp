# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import List, Sequence, Type

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.context.context import Context


@lru_cache
def create_canvas_tool_window_types() -> Sequence[Type[BaseWindow]]:
    from cvp.apps.player.modes.main.canvas.history import HistoryCanvasWindow
    from cvp.apps.player.modes.main.canvas.options import OptionsCanvasWindow
    from cvp.apps.player.modes.main.canvas.props import PropsCanvasWindow
    from cvp.apps.player.modes.main.canvas.timeline import TimelineCanvasWindow
    from cvp.apps.player.modes.main.canvas.tools import ToolsCanvasWindow

    return (
        HistoryCanvasWindow,
        OptionsCanvasWindow,
        PropsCanvasWindow,
        TimelineCanvasWindow,
        ToolsCanvasWindow,
    )


def create_canvas_tool_windows(context: Context) -> List[WindowInterface]:
    window_types = create_canvas_tool_window_types()
    return list(wt(context) for wt in window_types)
