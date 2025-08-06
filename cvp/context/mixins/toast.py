# -*- coding: utf-8 -*-

from logging import Logger
from typing import Optional, Union

from cvp.context.mixins._base import BaseContextMixin


class ToastMixin(BaseContextMixin):
    def toast(
        self,
        message: Union[BaseException, str],
        level: Optional[Union[int, str]] = None,
        logger: Optional[Logger] = None,
    ):
        return self._msgs.toast(message, level, logger)

    def toast_error(
        self,
        message: Union[BaseException, str],
        logger: Optional[Logger] = None,
        *,
        error: Optional[BaseException] = None,
    ):
        if logger and error and self._config.debug and 2 <= self._config.verbose:
            logger.exception(error)
            logger = None
        return self._msgs.toast_error(message, logger)

    def toast_warning(
        self,
        message: Union[BaseException, str],
        logger: Optional[Logger] = None,
    ):
        return self._msgs.toast_warning(message, logger)

    def toast_info(
        self,
        message: Union[BaseException, str],
        logger: Optional[Logger] = None,
    ):
        return self._msgs.toast_info(message, logger)

    def toast_debug(
        self,
        message: Union[BaseException, str],
        logger: Optional[Logger] = None,
    ):
        return self._msgs.toast_debug(message, logger)
