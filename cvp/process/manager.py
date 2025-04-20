# -*- coding: utf-8 -*-

from typing import Dict, Optional, TypeVar

from cvp.logging.logging import logger
from cvp.process.process import Process
from cvp.process.status import ProcessStatusEx

ProcessT = TypeVar("ProcessT", bound=Process)
KeyT = TypeVar("KeyT")


class ProcessManager(Dict[KeyT, ProcessT]):
    def spawnable(self, key: KeyT) -> bool:
        return not self.__contains__(key)

    def stoppable(self, key: KeyT) -> bool:
        if self.__contains__(key):
            return self.__getitem__(key).poll() is None
        else:
            return False

    def removable(self, key: KeyT) -> bool:
        if self.__contains__(key):
            return not self.__getitem__(key).is_alive()
        else:
            return False

    def status(self, key: KeyT) -> ProcessStatusEx:
        if self.__contains__(key):
            return self.__getitem__(key).status()
        else:
            return ProcessStatusEx.not_exists

    def interrupt(self, key: KeyT) -> None:
        self.__getitem__(key).interrupt()

    @staticmethod
    def timeout_as_logging_suffix(timeout: Optional[float] = None) -> str:
        if timeout is not None:
            return f" (timeout={timeout:.03f}s)"
        else:
            return str()

    def removable_pop(self, key: KeyT):
        if not self.removable(key):
            raise ValueError(f"Non-removable process: '{key}'")

        process = self.pop(key)
        logger.info(f"Calls the teardown callback of process {process.pid}")
        process.teardown()
        return process

    def shutdown(self, timeout: Optional[float] = None):
        logger.info("ProcessManager is terminating all processes ...")

        processes = list()
        while bool(self):
            processes.append(self.popitem()[1])

        for proc in processes:
            if proc.poll() is not None:
                continue

            logger.info(f"Interrupt the process ({proc.pid}) ...")
            proc.interrupt()

        for proc in processes:
            try:
                logging_suffix = self.timeout_as_logging_suffix(timeout)
                logger.info(f"Waiting the process ({proc.pid}) ...{logging_suffix}")
                proc.wait(timeout)
            except TimeoutError:
                logger.warning(f"Timeout raised! KILL process ({proc.pid})")
                proc.kill()

        for proc in processes:
            logger.info(f"Calls the teardown callback of process {proc.pid}")
            proc.teardown()

        for proc in processes:
            logger.info(f"The exit code of process ({proc.pid}) is {proc.returncode}")
