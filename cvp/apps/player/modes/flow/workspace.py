# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.flags.focused import ROOT_AND_CHILD_WINDOWS
from cvp.patterns.delta import Delta
from cvp.types.override import override


class WorkspaceFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Workspace"

    def __init__(self, context: Context, uuid: str):
        super().__init__(context)
        self._uuid = uuid
        self._focusing = Delta.from_single_value(False)

    @property
    def workspace(self):
        return self.context.flows.workspaces[self._uuid]

    @property
    def opened(self):
        return self.workspace.opened

    @override
    def get_window_name(self) -> str:
        if workspace_name := self.workspace.name:
            return workspace_name
        else:
            return self.__cvp_flow_window_name__

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            self._focusing.update(imgui.is_window_focused(ROOT_AND_CHILD_WINDOWS))
            if self._focusing.changed and self._focusing.value:
                self.context.flows.set_focused_workspaces(self._uuid)

            self.do_workspace_process()

    def do_workspace_process(self) -> None:
        pass
