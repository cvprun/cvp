# -*- coding: utf-8 -*-

from typing import Optional, Union

from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.logging import DEBUG, ERROR, INFO, WARNING


class ToastMixin(BaseContextMixin):
    def toast(self, message: str, level: Optional[Union[int, str]] = None):
        return self._msg_queue.append_toast(message, level)

    def toast_error(self, message: str):
        return self.toast(message, ERROR)

    def toast_warning(self, message: str):
        return self.toast(message, WARNING)

    def toast_info(self, message: str):
        return self.toast(message, INFO)

    def toast_debug(self, message: str):
        return self.toast(message, DEBUG)
