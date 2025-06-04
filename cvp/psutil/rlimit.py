# -*- coding: utf-8 -*-
# https://psutil.readthedocs.io/en/latest/#process-resources-constants

from functools import lru_cache
from types import MappingProxyType
from typing import Dict, Final, NamedTuple

import psutil


# noinspection PyUnresolvedReferences, SpellCheckingInspection
def _create_rlimit_key_names() -> Dict[int, str]:
    result = {
        psutil.RLIMIT_AS: "AS",
        psutil.RLIMIT_CORE: "CORE",
        psutil.RLIMIT_CPU: "CPU",
        psutil.RLIMIT_DATA: "DATA",
        psutil.RLIMIT_FSIZE: "FSIZE",
        psutil.RLIMIT_MEMLOCK: "MEMLOCK",
        psutil.RLIMIT_NOFILE: "NOFILE",
        psutil.RLIMIT_NPROC: "NPROC",
        psutil.RLIMIT_RSS: "RSS",
        psutil.RLIMIT_STACK: "STACK",
    }

    if psutil.LINUX:
        result.update(
            {
                psutil.RLIMIT_LOCKS: "LOCKS",
                psutil.RLIMIT_MSGQUEUE: "MSGQUEUE",
                psutil.RLIMIT_NICE: "NICE",
                psutil.RLIMIT_RTPRIO: "RTPRIO",
                psutil.RLIMIT_RTTIME: "RTTIME",
                psutil.RLIMIT_SIGPENDING: "SIGPENDING",
            }
        )

    if psutil.FREEBSD:
        result.update(
            {
                psutil.RLIMIT_SWAP: "SWAP",
                psutil.RLIMIT_SBSIZE: "SBSIZE",
                psutil.RLIMIT_NPTS: "NPTS",
            }
        )

    return result


@lru_cache()
def _rlimit_key_names() -> MappingProxyType[int, str]:
    return MappingProxyType(_create_rlimit_key_names())


RLIMIT_KEY_NAMES: Final[MappingProxyType[int, str]] = _rlimit_key_names()


class ResourceLimitTuple(NamedTuple):
    resource: int
    name: str
    soft: int
    hard: int

    @property
    def limits(self):
        return self.soft, self.hard


class ResourceLimits(Dict[int, ResourceLimitTuple]):
    @classmethod
    def from_process(cls, process: psutil.Process):
        items = dict()
        for key, name in RLIMIT_KEY_NAMES.items():
            soft, hard = process.rlimit(key)
            items[key] = ResourceLimitTuple(key, name, soft, hard)
        return cls(items)

    @classmethod
    def from_pid(cls, pid: int):
        return cls.from_process(psutil.Process(pid))
