# -*- coding: utf-8 -*-

from datetime import datetime
from types import MappingProxyType
from typing import Final
from zoneinfo import ZoneInfo, available_timezones

from cvp.containers.immutable_list import ImmutableList


def format_utc_offset(tz: ZoneInfo) -> str:
    offset = datetime.now(tz).utcoffset()
    assert offset is not None

    total_seconds = offset.total_seconds()
    hours, remainder = divmod(int(total_seconds), 3600)
    minutes = remainder // 60

    sign = "+" if total_seconds >= 0 else "-"
    return f"{sign}{abs(hours):02d}:{minutes:02d}"


def _create_sorted_available_timezones() -> ImmutableList[ZoneInfo]:
    names = list(available_timezones())
    names.sort()
    zones = [ZoneInfo(name) for name in names]
    return ImmutableList(zones)


def _create_zone_names() -> ImmutableList[str]:
    return ImmutableList(map(lambda x: x.key, TIME_ZONES))


def _create_utc_offsets() -> MappingProxyType[str, str]:
    return MappingProxyType({tz.key: format_utc_offset(tz) for tz in TIME_ZONES})


TIME_ZONES: Final[ImmutableList[ZoneInfo]] = _create_sorted_available_timezones()
ZONE_NAMES: Final[ImmutableList[str]] = _create_zone_names()
UTC_OFFSETS: Final[MappingProxyType[str, str]] = _create_utc_offsets()
