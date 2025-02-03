# -*- coding: utf-8 -*-

from datetime import date, datetime
from typing import NamedTuple


class MonthDay(NamedTuple):
    month: int  # 1-12
    day: int  # 1-31

    def __str__(self):
        return f"{self.month:02}/{self.day:02}"

    @classmethod
    def from_date(cls, d: date):
        return cls(d.month, d.day)

    @classmethod
    def from_datetime(cls, dt: datetime):
        return cls(dt.month, dt.day)

    @classmethod
    def from_format(cls, text: str, fmt="%m/%d"):
        return cls.from_datetime(datetime.strptime(text, fmt))


def in_month_day(
    now: MonthDay,
    begin: MonthDay,
    end: MonthDay,
) -> bool:
    if begin < end:
        return begin <= now <= end
    else:
        return now <= end or begin <= now
