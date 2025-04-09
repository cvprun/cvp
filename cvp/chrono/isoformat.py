# -*- coding: utf-8 -*-

from datetime import UTC, datetime, tzinfo
from enum import StrEnum
from enum import auto as _auto
from enum import unique
from typing import Optional, TypeAlias, Union

DateTimeLike: TypeAlias = Optional[Union[datetime, str]]


@unique
class TimeSpec(StrEnum):
    hours = _auto()
    minutes = _auto()
    seconds = _auto()
    milliseconds = _auto()
    microseconds = _auto()
    auto = _auto()


def isoformat(
    dt: DateTimeLike = None,
    tz: Optional[tzinfo] = None,
    sep="T",
    timespec=TimeSpec.auto,
) -> str:
    if dt is None:
        dt = datetime.now()
    elif isinstance(dt, str):
        dt = datetime.fromisoformat(dt)

    assert isinstance(dt, datetime)
    return dt.astimezone(tz).isoformat(sep=sep, timespec=str(timespec))


def fromisoformat(dt: DateTimeLike = None, tz: Optional[tzinfo] = None) -> datetime:
    if dt is None:
        return datetime.now().astimezone(tz)
    elif isinstance(dt, datetime):
        if dt.tzinfo is not None and tz is None:
            return dt
        else:
            return dt.astimezone(tz)
    elif isinstance(dt, str):
        return datetime.fromisoformat(dt).astimezone(tz)
    else:
        raise TypeError(f"Unsupported datetime like type: {type(dt).__name__}")


def isoformat_with_utc(dt: DateTimeLike = None, sep="T", timespec=TimeSpec.auto):
    return isoformat(dt, tz=UTC, sep=sep, timespec=timespec)


def fromisoformat_with_utc(dt: DateTimeLike = None):
    return fromisoformat(dt, tz=UTC)
