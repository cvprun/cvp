# -*- coding: utf-8 -*-

from typing import Generic, TypeVar

from cvp.context.context import Context
from cvp.logging.loggers import logger
from cvp.patterns.proxy import ValueProxy, ValueT

ErrorT = TypeVar("ErrorT", bound=BaseException)


class AutoFixerError(Generic[ValueT], Exception):
    def __init__(self, path: str, value: ValueT):
        super().__init__(
            f"Due to AutoFixer, '{path}' was automatically corrected to {value}"
        )


class AutoFixer(Generic[ValueT, ErrorT]):
    """A Retriever class that checks and restores configuration information."""

    def __init__(
        self,
        context: Context,
        config_proxy: ValueProxy[ValueT],
        config_section_path: str,
        not_exists_value: ValueT,
        update_value: ValueT,
    ):
        self._context = context
        self._config_proxy = config_proxy
        self._config_section_path = config_section_path
        self._not_exists_value = not_exists_value
        self._update_value = update_value

    def run(self, error: ErrorT) -> None:
        logger.warning(
            f"Please modify the value of '{self._config_section_path}'"
            f" to {self._update_value} of the"
            f" '{str(self._context.home.cvp_yml)}' file and try again."
        )

        if self._context.config.context.auto_fixer:
            # If the user changed the value directly, it should not be modified.
            # Therefore, the initial value is specified and checked in case
            # the user did not change the value.
            if self._config_proxy.get() is self._not_exists_value:
                try:
                    self._config_proxy.set(self._update_value)
                    self._context.save_config()
                except BaseException as e:
                    logger.error(e)
                else:
                    raise AutoFixerError[ValueT](
                        self._config_section_path, self._update_value
                    ) from error

        raise RuntimeError(
            f"An issue has occurred with the '{self._config_section_path}' features"
        ) from error
