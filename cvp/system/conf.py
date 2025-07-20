# -*- coding: utf-8 -*-

import os
import sys


def get_page_size_with_win32() -> int:
    import ctypes

    class SystemInfo(ctypes.Structure):
        _fields_ = [("dwPageSize", ctypes.c_ulong)]

    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

    si = SystemInfo()

    kernel32.GetSystemInfo(ctypes.byref(si))
    return si.dwPageSize


def get_page_size_with_unix() -> int:
    return os.sysconf("SC_PAGE_SIZE")


def get_page_size() -> int:
    if sys.platform == "win32":
        return get_page_size_with_win32()
    else:
        return get_page_size_with_unix()
