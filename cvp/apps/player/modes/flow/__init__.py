# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from imgui_bundle import imgui
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
    from cvp.apps.player.modes.flow.catalog import CatalogFlowWindow
    from cvp.apps.player.modes.flow.debug import DebugFlowWindow
    from cvp.apps.player.modes.flow.history import HistoryFlowWindow
    from cvp.apps.player.modes.flow.logging import LoggingFlowWindow
    from cvp.apps.player.modes.flow.props import PropsFlowWindow
    from cvp.apps.player.modes.flow.tree import TreeFlowWindow

    return (
        CatalogFlowWindow,
        DebugFlowWindow,
        HistoryFlowWindow,
        LoggingFlowWindow,
        PropsFlowWindow,
        TreeFlowWindow,
    )


def create_flow_window(context: Context) -> OrderedDict[str, FlowWindowInterface]:
    win_types = create_flow_window_types()
    return OrderedDict({wt.get_window_name(): wt(context) for wt in win_types})


def initialize_dock_layout(dockspace_id: int) -> None:
    from cvp.apps.player.modes.flow.catalog import CatalogFlowWindow
    from cvp.apps.player.modes.flow.debug import DebugFlowWindow
    from cvp.apps.player.modes.flow.history import HistoryFlowWindow
    from cvp.apps.player.modes.flow.logging import LoggingFlowWindow
    from cvp.apps.player.modes.flow.props import PropsFlowWindow
    from cvp.apps.player.modes.flow.tree import TreeFlowWindow

    imgui.internal.dock_builder_remove_node(dockspace_id)
    imgui.internal.dock_builder_add_node(dockspace_id)

    split = imgui.internal.dock_builder_split_node(dockspace_id, imgui.Dir.left, 0.1)
    dock_left = split.id_at_dir
    dock_main_right = split.id_at_opposite_dir

    split = imgui.internal.dock_builder_split_node(dock_main_right, imgui.Dir.left, 0.8)
    dock_main = split.id_at_dir
    dock_right = split.id_at_opposite_dir

    split = imgui.internal.dock_builder_split_node(dock_left, imgui.Dir.up, 0.6)
    dock_left_top = split.id_at_dir
    dock_left_bottom = split.id_at_opposite_dir

    split = imgui.internal.dock_builder_split_node(dock_main, imgui.Dir.down, 0.1)
    dock_main_bottom = split.id_at_dir
    # dock_main_top = split.id_at_opposite_dir

    split = imgui.internal.dock_builder_split_node(dock_right, imgui.Dir.up, 0.6)
    dock_right_top = split.id_at_dir
    dock_right_bottom = split.id_at_opposite_dir

    catalog_name = CatalogFlowWindow.get_window_name()
    debug_name = DebugFlowWindow.get_window_name()
    history_name = HistoryFlowWindow.get_window_name()
    logging_name = LoggingFlowWindow.get_window_name()
    props_name = PropsFlowWindow.get_window_name()
    tree_name = TreeFlowWindow.get_window_name()

    imgui.internal.dock_builder_dock_window(tree_name, dock_left_top)
    imgui.internal.dock_builder_dock_window(catalog_name, dock_left_bottom)

    imgui.internal.dock_builder_dock_window(logging_name, dock_main_bottom)
    imgui.internal.dock_builder_dock_window(debug_name, dock_main_bottom)

    imgui.internal.dock_builder_dock_window(props_name, dock_right_top)
    imgui.internal.dock_builder_dock_window(history_name, dock_right_bottom)

    imgui.internal.dock_builder_finish(dockspace_id)


class FlowMode(BaseMode):
    __cvp_mode_name__ = "Flow"

    def __init__(self, context: Context):
        super().__init__(context)
        self._windows = create_flow_window(context)
        self._viewport_flags = ROOT_STATIC_VIEWPORT_FLAGS
        self._initialized_dock_layout = False

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
            if not self._initialized_dock_layout:
                initialize_dock_layout(dockspace_id)
                self._initialized_dock_layout = True

        for window in self._windows.values():
            window.do_process()
