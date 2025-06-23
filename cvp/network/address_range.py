# -*- coding: utf-8 -*-

from ipaddress import IPv4Address, IPv6Address
from typing import List

from cvp.network.address_family import is_ipv4_address, is_ipv6_address


def calc_ipv4_range(start: str, end: str) -> List[str]:
    start_ip = int(IPv4Address(start))
    end_ip = int(IPv4Address(end))

    if end_ip < start_ip:
        raise ValueError("Start IP must be less than or equal to end IP")

    return [str(IPv4Address(ip)) for ip in range(start_ip, end_ip + 1)]


def calc_ipv6_range(start: str, end: str) -> List[str]:
    start_ip = int(IPv6Address(start))
    end_ip = int(IPv6Address(end))

    if end_ip < start_ip:
        raise ValueError("Start IP must be less than or equal to end IP")

    return [str(IPv6Address(ip)) for ip in range(start_ip, end_ip + 1)]


def calc_ip_range(start: str, end: str) -> List[str]:
    if is_ipv4_address(start) and is_ipv4_address(end):
        return calc_ipv4_range(start, end)
    elif is_ipv6_address(start) and is_ipv6_address(end):
        return calc_ipv6_range(start, end)
    else:
        raise ValueError("Start and end IPs must be of the same address family")
