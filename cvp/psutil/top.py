# -*- coding: utf-8 -*-

from typing import Dict

from psutil import AccessDenied, NoSuchProcess, process_iter

from cvp.psutil.process.state import ProcessState


def query_all_process_infos() -> Dict[int, ProcessState]:
    result = dict()
    for proc in process_iter():
        try:
            result[proc.pid] = ProcessState.from_process(proc)
        except (AccessDenied, NoSuchProcess):
            continue
    return result
