# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.config.sections.flow import RecentItem
from cvp.context.context import Context
from cvp.flow.workspace import FlowWorkspace
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.child import AUTO_RESIZE_X, AUTO_RESIZE_Y, BORDERS
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.logging.logging import flow_logger as logger
from cvp.types.override import override


class IntroFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Intro"

    _RECENT_ITEM_SPLIT_X: Final[float] = FIT_WIDTH
    _RECENT_ITEM_CHILD_FLAGS: Final[int] = AUTO_RESIZE_Y | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def config(self):
        return self.context.config.flow_aui

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def open_workspace(self, uuid: str) -> None:
        workspace = self.flows.workspaces.get(uuid)
        if workspace is None:
            self.context.toast_error(f"Not found workspace: {uuid}", logger)
            return

        if workspace.opened:
            self.context.toast_error(f"The workspace is already open: {uuid}", logger)
            return

        if workspace.open():
            logger.info(f"Workspace opened successfully: {uuid}")
        else:
            self.context.toast_error(f"Workspace open failed: {uuid}", logger)

    def close_workspace(self, uuid: str) -> None:
        workspace = self.flows.workspaces.get(uuid)
        if workspace is None:
            self.context.toast_error(f"Not found workspace: {uuid}", logger)
            return

        if not workspace.opened:
            self.context.toast_error(f"The workspace is already closed: {uuid}", logger)
            return

        try:
            workspace.close()
            logger.info(f"Workspace closed successfully: {uuid}")
        except BaseException as e:
            self.context.toast_error(f"Workspace close failed: {e}", logger)

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            if imgui.button("New workspace"):
                self.context.flows.create_new_workspace()

            if imgui.button("Reload workspace"):
                self.context.flows.workspaces.read_all_config_files(raise_errors=False)

            imgui.separator()

            imgui.text("Recent workspace")
            for recent in self.config.recent:
                self.do_recent_process(recent)

            imgui.separator()

            imgui.text("Loaded workspaces")
            for workspace in self.flows.workspaces.values():
                self.do_workspace_process(workspace)

    def do_recent_process(self, recent: RecentItem) -> None:
        workspace = self.context.flows.workspaces.get(recent.uuid)
        if workspace is not None:
            self.do_workspace_process(workspace)
        else:
            imgui.text_colored(self.error_color, f"Not found workspace: {recent.uuid}")

    def do_workspace_process(self, workspace: FlowWorkspace) -> None:
        with begin_child_context(
            f"Workspace##{workspace.uuid}",
            size=(self._RECENT_ITEM_SPLIT_X, 0),
            child_flags=self._RECENT_ITEM_CHILD_FLAGS,
        ):
            with begin_child_context("Left", child_flags=AUTO_RESIZE_X | AUTO_RESIZE_Y):
                imgui.text(workspace.name)

                with style_disable_input_context():
                    imgui.text(workspace.uuid)

            imgui.same_line()

            avail_size = imgui.get_content_region_avail()
            imgui.begin_horizontal("Horizontal", size=(avail_size.x, 0))
            try:
                imgui.spring()
                if imgui.button("Open", size=(0, avail_size.y)):
                    workspace.open()
            finally:
                imgui.end_horizontal()
