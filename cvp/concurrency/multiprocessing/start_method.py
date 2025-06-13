# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class StartMethod(StrEnum):
    spawn = auto()
    fork = auto()
    forkserver = auto()


def get_start_method() -> StartMethod:
    import multiprocessing as mp

    return StartMethod(mp.get_start_method())


def set_start_method(method: StartMethod) -> None:
    import multiprocessing as mp

    if method not in mp.get_all_start_methods():
        raise ValueError(f"Unsupported start method: {str(method)}")

    mp.set_start_method(str(method))
