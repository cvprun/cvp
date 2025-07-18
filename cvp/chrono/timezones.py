# -*- coding: utf-8 -*-

from datetime import datetime, tzinfo
from functools import lru_cache
from types import MappingProxyType
from typing import Final, Iterable, List, NamedTuple
from zoneinfo import ZoneInfo, available_timezones

from cvp.containers.immutable_list import ImmutableList


def format_utc_offset(tz: tzinfo) -> str:
    offset = datetime.now(tz).utcoffset()
    assert offset is not None

    total_seconds = offset.total_seconds()
    hours, remainder = divmod(int(total_seconds), 3600)
    minutes = remainder // 60

    sign = "+" if total_seconds >= 0 else "-"
    return f"{sign}{abs(hours):02d}:{minutes:02d}"


class ZoneTuple(NamedTuple):
    name: str
    info: tzinfo

    @property
    def utc_offset(self) -> str:
        return format_utc_offset(self.info)


@lru_cache
def local_tzinfo() -> ZoneTuple:
    now = datetime.now().astimezone()
    name = now.tzname()
    info = now.tzinfo
    assert name is not None
    assert info is not None
    return ZoneTuple(name, info)


@lru_cache
def _create_tzinfos() -> ImmutableList[ZoneTuple]:
    zone_names = available_timezones()
    zone_infos: List[ZoneTuple] = [ZoneTuple(z, ZoneInfo(z)) for z in zone_names]

    local_info = local_tzinfo()
    if local_info.name not in zone_names:
        zone_infos.append(local_info)

    sorted_infos = sorted(zone_infos, key=lambda x: x.name)
    return ImmutableList(sorted_infos)


def mapping_tzinfos(tzinfos: Iterable[ZoneTuple]) -> MappingProxyType[str, tzinfo]:
    return MappingProxyType({tz.name: tz.info for tz in tzinfos})


TZINFOS: Final[ImmutableList[ZoneTuple]] = _create_tzinfos()
TZINFO_MAP: Final[MappingProxyType[str, tzinfo]] = mapping_tzinfos(TZINFOS)
ZONE_NAMES: Final[ImmutableList[str]] = ImmutableList(tz.name for tz in TZINFOS)
ZONE_INFOS: Final[ImmutableList[tzinfo]] = ImmutableList(tz.info for tz in TZINFOS)
UTC_OFFSETS: Final[ImmutableList[str]] = ImmutableList(tz.utc_offset for tz in TZINFOS)
