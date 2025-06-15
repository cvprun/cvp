# -*- coding: utf-8 -*-

from typing import Optional

from croniter import croniter


class CronexprError(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


def validate_cronexpr(cronexpr: str) -> Optional[BaseException]:
    try:
        croniter(cronexpr)
        return None
    except BaseException as e:
        return e
