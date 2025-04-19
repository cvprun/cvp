# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import PROCESS_TEARDOWN_TIMEOUT


@dataclass
class ProcessConfig:
    teardown_timeout: float = PROCESS_TEARDOWN_TIMEOUT
