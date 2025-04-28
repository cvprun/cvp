# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Union

from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.logging import flow_logger as logger


class FlowWorkspaceMixin(BaseContextMixin):
    def opened_flow_workspace(self) -> bool:
        return self._flows.opened

    def open_flow_workspace(self, path: Union[PathLike, str]) -> None:
        try:
            self._flows.open(path)
            recent_value = str(Path(path).resolve())
            self._config.navigation.add_recent_item(type(self), recent_value)
        except BaseException as e:
            self._msgs.toast_error(f"Workspace open failed: {e}", logger)
        else:
            logger.info("Workspace opened successfully")

    def close_flow_workspace(self) -> None:
        try:
            dirpath = Path(self._flows.dirpath) if self._flows.dirpath else None
            self._flows.close()

            assert self._flows.dirpath is None
            assert isinstance(dirpath, Path)
            recent_value = str(dirpath.resolve())

            self._config.navigation.add_recent_item(type(self), recent_value)
        except BaseException as e:
            self._msgs.toast_error(f"Workspace close failed: {e}", logger)
        else:
            logger.info("Workspace closed successfully")

    def get_flow_workspace_recent_items(self):
        return self._config.navigation.get_recent_items(type(self))
