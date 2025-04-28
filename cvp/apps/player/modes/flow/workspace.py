# -*- coding: utf-8 -*-

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.types.override import override


class WorkspaceFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Workspace"

    def __init__(self, context: Context, uuid: str):
        super().__init__(context)
        self._uuid = uuid

    @property
    def config(self):
        return self.context.config.flow_aui

    @property
    def workspace(self):
        return self.context.flows.workspaces[self._uuid]

    @override
    def get_window_name(self) -> str:
        if workspace_name := self.workspace.name:
            return workspace_name
        else:
            return self.__cvp_flow_window_name__

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            self.do_workspace_process()

    def do_workspace_process(self) -> None:
        pass
