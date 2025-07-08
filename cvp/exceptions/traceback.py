# -*- coding: utf-8 -*-

from traceback import format_exception
from typing import Optional


def traceback_exception_string(
    exc: BaseException,
    *,
    limit: Optional[int] = None,
    chain=True,
):
    return "".join(format_exception(exc, limit=limit, chain=chain))
