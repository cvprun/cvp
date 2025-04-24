# -*- coding: utf-8 -*-

from logging import Logger
from typing import Optional, Union

from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.logging import DEBUG, ERROR, INFO, WARNING, convert_level_number


class ToastMixin(BaseContextMixin):
    def toast(
        self,
        message: str,
        level: Optional[Union[int, str]] = None,
        logger: Optional[Logger] = None,
    ):
        if logger is not None:
            logger.log(convert_level_number(level), message)
        return self._msg_queue.append_toast(message, level)

    def toast_error(self, message: str, logger: Optional[Logger] = None):
        return self.toast(message, ERROR, logger=logger)

    def toast_warning(self, message: str, logger: Optional[Logger] = None):
        return self.toast(message, WARNING, logger=logger)

    def toast_info(self, message: str, logger: Optional[Logger] = None):
        return self.toast(message, INFO, logger=logger)

    def toast_debug(self, message: str, logger: Optional[Logger] = None):
        return self.toast(message, DEBUG, logger=logger)
