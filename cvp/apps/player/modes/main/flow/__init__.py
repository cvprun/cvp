# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import List, Sequence, Type

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.context.context import Context


@lru_cache
def create_flow_tool_window_types() -> Sequence[Type[BaseWindow]]:
    from cvp.apps.player.modes.main.flow.debug import DebugFlowWindow
    from cvp.apps.player.modes.main.flow.dtypes import DtypeFlowWindow, DtypesFlowWindow
    from cvp.apps.player.modes.main.flow.graphs import GraphsFlowWindow
    from cvp.apps.player.modes.main.flow.history import HistoryFlowWindow
    from cvp.apps.player.modes.main.flow.intro import IntroFlowWindow
    from cvp.apps.player.modes.main.flow.logging import LoggingFlowWindow
    from cvp.apps.player.modes.main.flow.nodes import NodeFlowWindow, NodesFlowWindow
    from cvp.apps.player.modes.main.flow.props import PropsFlowWindow
    from cvp.apps.player.modes.main.flow.tree import TreeFlowWindow

    return (
        DebugFlowWindow,
        DtypeFlowWindow,
        DtypesFlowWindow,
        GraphsFlowWindow,
        HistoryFlowWindow,
        IntroFlowWindow,
        LoggingFlowWindow,
        NodeFlowWindow,
        NodesFlowWindow,
        PropsFlowWindow,
        TreeFlowWindow,
    )


def create_flow_tool_windows(context: Context) -> List[WindowInterface]:
    window_types = create_flow_tool_window_types()
    return list(wt(context) for wt in window_types)
