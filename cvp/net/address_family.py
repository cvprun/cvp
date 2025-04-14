# -*- coding: utf-8 -*-

from ipaddress import (
    AddressValueError,
    IPv4Address,
    IPv6Address,
    NetmaskValueError,
    ip_address,
)
from socket import AF_INET, AF_INET6


def get_ip_address_family(address: str) -> int:
    return AF_INET if type(ip_address(address)) is IPv4Address else AF_INET6


def is_ip_address(address: str) -> bool:
    try:
        ip_address(address)
    except ValueError:
        return False
    else:
        return True


def is_ipv4_address(address: str) -> bool:
    try:
        IPv4Address(address)
    except (AddressValueError, NetmaskValueError):
        return False
    else:
        return True


def is_ipv6_address(address: str) -> bool:
    try:
        IPv6Address(address)
    except (AddressValueError, NetmaskValueError):
        return False
    else:
        return True
