# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import PROCESS_TEARDOWN_TIMEOUT, PROCESS_UPDATE_INTERVAL


@dataclass
class ProcessConfig:
    update_interval: float = PROCESS_UPDATE_INTERVAL
    teardown_timeout: float = PROCESS_TEARDOWN_TIMEOUT
