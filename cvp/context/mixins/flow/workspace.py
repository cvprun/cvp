# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.logging import flow_logger as logger


class FlowWorkspaceMixin(BaseContextMixin):
    def opened_flow_workspace(self) -> bool:
        return self._flows.opened

    def open_flow_workspace(self, path: Union[PathLike, str]) -> None:
        try:
            self._flows.open(path)
            self._config.flow.add_recent(str(path))
        except BaseException as e:
            self._msgs.toast_error(f"Workspace open failed: {e}", logger)
        else:
            logger.info("Workspace opened successfully")

    def close_flow_workspace(self) -> None:
        try:
            dirpath = str(self._flows.dirpath) if self._flows.dirpath else None
            self._flows.close()

            assert self._flows.dirpath is None
            assert dirpath is not None

            self._config.flow.add_recent(dirpath)
        except BaseException as e:
            self._msgs.toast_error(f"Workspace close failed: {e}", logger)
        else:
            logger.info("Workspace closed successfully")
