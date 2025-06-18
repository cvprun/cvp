# -*- coding: utf-8 -*-

from time import sleep

from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.loggers import logger
from cvp.service.item import ServiceKey


class ServiceMixin(BaseContextMixin):
    def handle_exited_process(self, key: ServiceKey) -> None:
        request = self._services.evaluate_restart_policy(key)
        if request is not None:
            code = request.code
            policy = str(request.policy)
            delay = request.delay
            logger.info(f"Service will be restarted ({code=} {policy=} {delay=:.02f}s)")
            self.submit_thread(self.on_restart_process, key, delay)
        else:
            logger.info("Service has terminated.")

    def handle_restart_process(self, key: ServiceKey) -> None:
        logger.info(f"Restarting service: {key=}")
        try:
            self._services.spawn(key)
            logger.info(f"Service restart initiated: {key=}")
        except BaseException as e:
            logger.error(f"Failed to restart service {key}: {e}")
            raise

    def on_restart_process(self, key: ServiceKey, delay: float) -> None:
        if 0.0 < delay:
            logger.debug(f"Waiting {delay:.02f}s before restart: {key=}")
            sleep(delay)

        logger.debug(f"Sending restart message: {key=}")
        self._msgs.process_restart(key)
