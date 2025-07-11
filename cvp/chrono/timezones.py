# -*- coding: utf-8 -*-

from typing import Final
from zoneinfo import ZoneInfo, available_timezones

from cvp.containers.immutable_list import ImmutableList


def _create_sorted_available_timezones() -> ImmutableList[ZoneInfo]:
    names = list(available_timezones())
    names.sort()
    zones = [ZoneInfo(name) for name in names]
    return ImmutableList(zones)


TIMEZONES: Final[ImmutableList[ZoneInfo]] = _create_sorted_available_timezones()
ZONE_NAMES: Final[ImmutableList[str]] = ImmutableList(map(lambda x: x.key, TIMEZONES))
