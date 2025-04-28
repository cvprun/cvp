# -*- coding: utf-8 -*-

from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.logging import flow_logger as logger


class FlowWorkspaceMixin(BaseContextMixin):
    def open_flow_workspace(self, uuid: str) -> None:
        workspace = self._flows.workspaces.get(uuid)
        if workspace is None:
            self._msgs.toast_error(f"Not found workspace: {uuid}", logger)
            return

        if workspace.opened:
            self._msgs.toast_error(f"The workspace is already open: {uuid}", logger)
            return

        if workspace.open():
            logger.info(f"Workspace opened successfully: {uuid}")
        else:
            self._msgs.toast_error(f"Workspace open failed: {uuid}", logger)

    def close_flow_workspace(self, uuid: str) -> None:
        workspace = self._flows.workspaces.get(uuid)
        if workspace is None:
            self._msgs.toast_error(f"Not found workspace: {uuid}", logger)
            return

        if not workspace.opened:
            self._msgs.toast_error(f"The workspace is already closed: {uuid}", logger)
            return

        try:
            workspace.close()
            logger.info(f"Workspace closed successfully: {uuid}")
        except BaseException as e:
            self._msgs.toast_error(f"Workspace close failed: {e}", logger)
