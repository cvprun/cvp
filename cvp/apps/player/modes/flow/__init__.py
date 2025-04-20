# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.flow._base import BaseFlowWindow, FlowWindowInterface
from cvp.context.context import Context
from cvp.imgui.dockspace import dockspace_over_viewport_context
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.msgs.msg import Msg
from cvp.types.override import override


@lru_cache
def create_flow_window_types() -> Sequence[Type[BaseFlowWindow]]:
    from cvp.apps.player.modes.flow.dtypes import DtypesFlowWindow

    return (DtypesFlowWindow,)


def create_flow_window(context: Context) -> OrderedDict[str, FlowWindowInterface]:
    win_types = create_flow_window_types()
    return OrderedDict({wt.get_window_name(): wt(context) for wt in win_types})


class FlowMode(BaseMode):
    __cvp_mode_name__ = "Flow"

    def __init__(self, context: Context):
        super().__init__(context)
        self._windows = create_flow_window(context)
        self._viewport_flags = ROOT_STATIC_VIEWPORT_FLAGS

    @override
    def on_main_menu(self) -> None:
        pass

    @override
    def do_event(self, event: Event) -> bool:
        return False

    @override
    def do_msg(self, msg: Msg) -> bool:
        return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @override
    def do_process(self) -> None:
        with dockspace_over_viewport_context() as dockspace_id:
            assert isinstance(dockspace_id, int)
            assert 0 <= dockspace_id

        for window in self._windows.values():
            window.do_process()
