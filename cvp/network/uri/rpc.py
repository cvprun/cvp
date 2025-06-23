# -*- coding: utf-8 -*-

from enum import Enum
from functools import reduce
from io import StringIO
from socket import AF_INET, AF_INET6
from typing import Final, List, NamedTuple, Optional, Tuple, Union

from cvp.network.address_family import get_ip_address_family
from cvp.network.host_port import (
    CLOSING_IPV6,
    OPENING_IPV6,
    OPENING_PORT,
    parse_host_port,
    parse_ipv4_or_domain_port,
    parse_ipv6_port,
)


class RpcSchemeType(Enum):
    Dns = 0
    Unix = 1
    UnixAbstract = 2
    Ipv4 = 3
    Ipv6 = 4


NOT_FOUND_INDEX = -1

SCHEME_DNS = "dns:"
SCHEME_UNIX = "unix:"
SCHEME_UNIX_ABSOLUTE = SCHEME_UNIX + "//"
SCHEME_UNIX_ABSTRACT = "unix-abstract:"
SCHEME_IPV4 = "ipv4:"
SCHEME_IPV6 = "ipv6:"

SCHEME_DNS_LEN = len(SCHEME_DNS)
SCHEME_UNIX_LEN = len(SCHEME_UNIX)
SCHEME_UNIX_ABSOLUTE_LEN = len(SCHEME_UNIX_ABSOLUTE)
SCHEME_UNIX_ABSTRACT_LEN = len(SCHEME_UNIX_ABSTRACT)
SCHEME_IPV4_LEN = len(SCHEME_IPV4)
SCHEME_IPV6_LEN = len(SCHEME_IPV6)


def get_rpc_scheme_type(address: str) -> RpcSchemeType:
    if address.startswith(SCHEME_DNS):
        return RpcSchemeType.Dns
    elif address.startswith(SCHEME_UNIX):
        return RpcSchemeType.Unix
    elif address.startswith(SCHEME_UNIX_ABSTRACT):
        return RpcSchemeType.UnixAbstract
    elif address.startswith(SCHEME_IPV4):
        return RpcSchemeType.Ipv4
    elif address.startswith(SCHEME_IPV6):
        return RpcSchemeType.Ipv6

    # https://github.com/grpc/grpc/blob/master/doc/naming.md
    # If no scheme prefix is specified or the scheme is unknown,
    # the dns scheme is used by default.
    return RpcSchemeType.Dns


OPENING_AUTHORITY = "//"
OPENING_AUTHORITY_LEN = len(OPENING_AUTHORITY)

CLOSING_AUTHORITY = "/"
CLOSING_AUTHORITY_LEN = len(CLOSING_AUTHORITY)


class RpcDnsAddress(NamedTuple):
    """
    Syntax: ``dns:[//authority/]host[:port]``
    """

    authority: Optional[str]
    host: str
    port: Optional[int]

    @property
    def authority_tuple(self) -> Optional[Tuple[str, Optional[int]]]:
        if not self.authority:
            return None

        host_port = parse_host_port(self.authority)
        return host_port.host, host_port.port

    @property
    def authority_host(self) -> Optional[str]:
        host_port = self.authority_tuple
        return host_port[0] if host_port is not None else None

    @property
    def authority_port(self) -> Optional[int]:
        host_port = self.authority_tuple
        return host_port[1] if host_port is not None else None

    def encode(self) -> str:
        buffer = StringIO()
        buffer.write(SCHEME_DNS)
        if self.authority:
            buffer.write(OPENING_AUTHORITY)
            buffer.write(self.authority)
            buffer.write(CLOSING_AUTHORITY)
        buffer.write(self.host)
        if self.port is not None:
            buffer.write(OPENING_PORT)
            buffer.write(str(self.port))
        return buffer.getvalue()

    def __str__(self) -> str:
        return self.encode()

    def __repr__(self) -> str:
        return self.encode()


def _parse_rpc_dns_address(address: str) -> RpcDnsAddress:
    assert get_rpc_scheme_type(address) == RpcSchemeType.Dns

    authority: Optional[str]

    if address.startswith(SCHEME_DNS):
        body = address[SCHEME_DNS_LEN:]
    else:
        body = address

    if body.startswith(OPENING_AUTHORITY):
        closing_authority_index = body[OPENING_AUTHORITY_LEN:].find(CLOSING_AUTHORITY)
        if closing_authority_index == NOT_FOUND_INDEX:
            raise ValueError(
                f"Could not find the closing character ('{CLOSING_AUTHORITY}')"
                f"in the authority section: '{address}'"
            )

        authority_last_index = OPENING_AUTHORITY_LEN + closing_authority_index
        authority = body[OPENING_AUTHORITY_LEN:authority_last_index]
        host_port_begin = authority_last_index + CLOSING_AUTHORITY_LEN
        host_port_body = body[host_port_begin:]
    else:
        authority = None
        host_port_body = body

    host_port = parse_host_port(host_port_body)
    return RpcDnsAddress(authority, host_port.host, host_port.port)


def parse_rpc_dns_address(address: str) -> RpcDnsAddress:
    if get_rpc_scheme_type(address) != RpcSchemeType.Dns:
        raise ValueError(f"Invalid DNS scheme: {address}")
    return _parse_rpc_dns_address(address)


class RpcUnixAddress(NamedTuple):
    """
    Syntax: ``unix:path`` or ``unix://absolute_path``
    """

    path: str

    def encode(self) -> str:
        return SCHEME_UNIX + self.path

    def __str__(self) -> str:
        return self.encode()

    def __repr__(self) -> str:
        return self.encode()


def _parse_rpc_unix_address(address: str) -> RpcUnixAddress:
    assert get_rpc_scheme_type(address) == RpcSchemeType.Unix

    # [IMPORTANT]
    # Do not change the order of if-else statements.
    if address.startswith(SCHEME_UNIX_ABSOLUTE):
        absolute_path = address[SCHEME_UNIX_ABSOLUTE_LEN:]
        if absolute_path[0] != "/":
            raise ValueError(
                f"If you use the `{SCHEME_UNIX_ABSOLUTE}` prefix,"
                f"the path must be absolute: {address}"
            )
        return RpcUnixAddress(absolute_path)
    elif address.startswith(SCHEME_UNIX):
        return RpcUnixAddress(address[SCHEME_UNIX_LEN:])
    else:
        assert False, "Inaccessible section"


def parse_rpc_unix_address(address: str) -> RpcUnixAddress:
    if get_rpc_scheme_type(address) != RpcSchemeType.Unix:
        raise ValueError(f"Invalid Unix scheme: {address}")
    return _parse_rpc_unix_address(address)


class RpcUnixAbstractAddress(NamedTuple):
    """
    Syntax: ``unix-abstract:abstract_path``
    """

    abstract_path: str

    def encode(self) -> str:
        return SCHEME_UNIX_ABSTRACT + self.abstract_path

    def __str__(self) -> str:
        return self.encode()

    def __repr__(self) -> str:
        return self.encode()


def _parse_rpc_unix_abstract_address(address: str) -> RpcUnixAbstractAddress:
    assert get_rpc_scheme_type(address) == RpcSchemeType.UnixAbstract
    return RpcUnixAbstractAddress(address[SCHEME_UNIX_ABSTRACT_LEN:])


def parse_rpc_unix_abstract_address(address: str) -> RpcUnixAbstractAddress:
    if get_rpc_scheme_type(address) != RpcSchemeType.UnixAbstract:
        raise ValueError(f"Invalid Unix Abstract scheme: {address}")
    return _parse_rpc_unix_abstract_address(address)


class Address(NamedTuple):
    address: str
    port: Optional[int]

    def encode(self) -> str:
        if self.port is not None:
            return f"{self.address}{OPENING_PORT}{self.port}"
        else:
            return self.address

    def __str__(self) -> str:
        return self.encode()

    def __repr__(self) -> str:
        return self.encode()


ADDRESS_SEPARATOR: Final[str] = ","


def encode_addresses(*args: Address) -> str:
    return reduce(lambda x, y: f"{x}{ADDRESS_SEPARATOR}{y}", [a.encode() for a in args])


class RpcIpv4Addresses(NamedTuple):
    """
    Syntax: ``ipv4:address[:port][,address[:port],...]``
    """

    addresses: List[Address]

    def encode(self) -> str:
        return SCHEME_IPV4 + encode_addresses(*self.addresses)

    def __str__(self) -> str:
        return self.encode()

    def __repr__(self) -> str:
        return self.encode()


class RpcIpv6Addresses(NamedTuple):
    """
    Syntax: ``ipv6:address[:port][,address[:port],...]``
    """

    addresses: List[Address]

    def encode(self) -> str:
        return SCHEME_IPV6 + encode_addresses(*self.addresses)

    def __str__(self) -> str:
        return self.encode()

    def __repr__(self) -> str:
        return self.encode()


assert RpcIpv4Addresses != RpcIpv6Addresses, "They must be of different types"


def _parse_rpc_ipv4_addresses(address: str) -> RpcIpv4Addresses:
    assert get_rpc_scheme_type(address) == RpcSchemeType.Ipv4

    addresses = list()
    body = address[SCHEME_IPV4_LEN:]
    for ipv4_address in body.split(ADDRESS_SEPARATOR):
        host_port = parse_ipv4_or_domain_port(ipv4_address)
        host = host_port.host
        port = host_port.port

        if get_ip_address_family(host) != AF_INET:
            raise ValueError(f"Invalid IPv4 address included: {address}")

        addresses.append(Address(host, port))

    return RpcIpv4Addresses(addresses)


def parse_rpc_ipv4_addresses(address: str) -> RpcIpv4Addresses:
    if get_rpc_scheme_type(address) != RpcSchemeType.Ipv4:
        raise ValueError(f"Invalid IPv4 scheme: {address}")
    return _parse_rpc_ipv4_addresses(address)


def _parse_rpc_ipv6_addresses(address: str) -> RpcIpv6Addresses:
    assert get_rpc_scheme_type(address) == RpcSchemeType.Ipv6

    addresses = list()
    body = address[SCHEME_IPV6_LEN:]
    for ipv6_address in body.split(ADDRESS_SEPARATOR):
        host_port = parse_ipv6_port(ipv6_address)
        host = host_port.host
        port = host_port.port

        assert host[0] == OPENING_IPV6
        assert host[-1] == CLOSING_IPV6
        remove_square_bracket_host = host[1:-1]

        if get_ip_address_family(remove_square_bracket_host) != AF_INET6:
            raise ValueError(f"Invalid IPv6 address included: {address}")

        addresses.append(Address(host, port))

    return RpcIpv6Addresses(addresses)


def parse_rpc_ipv6_addresses(address: str) -> RpcIpv6Addresses:
    if get_rpc_scheme_type(address) != RpcSchemeType.Ipv6:
        raise ValueError(f"Invalid IPv6 scheme: {address}")
    return _parse_rpc_ipv6_addresses(address)


UnionRpcAddress = Union[
    RpcDnsAddress,
    RpcUnixAddress,
    RpcUnixAbstractAddress,
    RpcIpv4Addresses,
    RpcIpv6Addresses,
]


def parse_rpc_address(address: str) -> Tuple[RpcSchemeType, UnionRpcAddress]:
    scheme_type = get_rpc_scheme_type(address)
    if scheme_type == RpcSchemeType.Dns:
        return RpcSchemeType.Dns, _parse_rpc_dns_address(address)
    elif scheme_type == RpcSchemeType.Unix:
        return RpcSchemeType.Unix, _parse_rpc_unix_address(address)
    elif scheme_type == RpcSchemeType.UnixAbstract:
        return RpcSchemeType.UnixAbstract, _parse_rpc_unix_abstract_address(address)
    elif scheme_type == RpcSchemeType.Ipv4:
        return RpcSchemeType.Ipv4, _parse_rpc_ipv4_addresses(address)
    elif scheme_type == RpcSchemeType.Ipv6:
        return RpcSchemeType.Ipv6, _parse_rpc_ipv6_addresses(address)
    else:
        assert False, "Inaccessible section"


class RpcAddress:
    def __init__(self, scheme: RpcSchemeType, rpc_address: UnionRpcAddress):
        self.scheme = scheme
        self.rpc_address = rpc_address

    @property
    def is_dns(self) -> bool:
        return self.scheme == RpcSchemeType.Dns

    @property
    def is_unix(self) -> bool:
        return self.scheme == RpcSchemeType.Unix

    @property
    def is_unix_abstract(self) -> bool:
        return self.scheme == RpcSchemeType.UnixAbstract

    @property
    def is_ipv4(self) -> bool:
        return self.scheme == RpcSchemeType.Ipv4

    @property
    def is_ipv6(self) -> bool:
        return self.scheme == RpcSchemeType.Ipv6

    @property
    def has_dns_authority(self) -> bool:
        if not self.is_dns:
            return False
        assert isinstance(self.rpc_address, RpcDnsAddress)
        return self.rpc_address.authority is not None

    @property
    def has_dns_host(self) -> bool:
        if not self.is_dns:
            return False
        assert isinstance(self.rpc_address, RpcDnsAddress)
        return bool(self.rpc_address.host)

    @property
    def has_dns_port(self) -> bool:
        if not self.is_dns:
            return False
        assert isinstance(self.rpc_address, RpcDnsAddress)
        return self.rpc_address.port is not None

    @property
    def has_unix_path(self) -> bool:
        if not self.is_unix:
            return False
        assert isinstance(self.rpc_address, RpcUnixAddress)
        return bool(self.rpc_address.path)

    @property
    def has_unix_abstract_path(self) -> bool:
        if not self.is_unix_abstract:
            return False
        assert isinstance(self.rpc_address, RpcUnixAbstractAddress)
        return bool(self.rpc_address.abstract_path)

    @property
    def has_ipv4_addresses(self) -> bool:
        if not self.is_ipv4:
            return False
        assert isinstance(self.rpc_address, RpcIpv4Addresses)
        return bool(self.rpc_address.addresses)

    @property
    def has_ipv6_addresses(self) -> bool:
        if not self.is_ipv6:
            return False
        assert isinstance(self.rpc_address, RpcIpv6Addresses)
        return bool(self.rpc_address.addresses)

    @property
    def has_ip_addresses(self) -> bool:
        if self.is_ipv4:
            assert isinstance(self.rpc_address, RpcIpv4Addresses)
            return bool(self.rpc_address.addresses)
        elif self.is_ipv6:
            assert isinstance(self.rpc_address, RpcIpv6Addresses)
            return bool(self.rpc_address.addresses)
        else:
            return False

    @property
    def has_any_port(self) -> bool:
        if self.is_dns:
            assert isinstance(self.rpc_address, RpcDnsAddress)
            return self.rpc_address.port is not None
        elif self.is_ipv4:
            assert isinstance(self.rpc_address, RpcIpv4Addresses)
            for ipv4 in self.rpc_address.addresses:
                if ipv4.port is not None:
                    return True
        elif self.is_ipv6:
            assert isinstance(self.rpc_address, RpcIpv6Addresses)
            for ipv6 in self.rpc_address.addresses:
                if ipv6.port is not None:
                    return True
        return False

    @property
    def all_ports(self) -> List[int]:
        if self.is_dns:
            assert isinstance(self.rpc_address, RpcDnsAddress)
            if self.rpc_address.port is not None:
                return [self.rpc_address.port]
        elif self.is_ipv4:
            assert isinstance(self.rpc_address, RpcIpv4Addresses)
            return [a.port for a in self.rpc_address.addresses if a.port is not None]
        elif self.is_ipv6:
            assert isinstance(self.rpc_address, RpcIpv6Addresses)
            return [a.port for a in self.rpc_address.addresses if a.port is not None]
        return list()

    @property
    def as_dns(self) -> RpcDnsAddress:
        if not self.is_dns:
            raise TypeError("Only DNS schemes are supported")
        assert isinstance(self.rpc_address, RpcDnsAddress)
        return self.rpc_address

    @property
    def as_unix(self) -> RpcUnixAddress:
        if not self.is_unix:
            raise TypeError("Only Unix schemes are supported")
        assert isinstance(self.rpc_address, RpcUnixAddress)
        return self.rpc_address

    @property
    def as_unix_abstract(self) -> RpcUnixAbstractAddress:
        if not self.is_unix_abstract:
            raise TypeError("Only Unix Abstract schemes are supported")
        assert isinstance(self.rpc_address, RpcUnixAbstractAddress)
        return self.rpc_address

    @property
    def as_ipv4(self) -> RpcIpv4Addresses:
        if not self.is_ipv4:
            raise TypeError("Only IPv4 schemes are supported")
        assert isinstance(self.rpc_address, RpcIpv4Addresses)
        return self.rpc_address

    @property
    def as_ipv6(self) -> RpcIpv6Addresses:
        if not self.is_ipv6:
            raise TypeError("Only IPv6 schemes are supported")
        assert isinstance(self.rpc_address, RpcIpv6Addresses)
        return self.rpc_address

    @property
    def authority(self) -> Optional[str]:
        return self.as_dns.authority

    @property
    def authority_tuple(self) -> Optional[Tuple[str, Optional[int]]]:
        return self.as_dns.authority_tuple

    @property
    def authority_host(self) -> Optional[str]:
        return self.as_dns.authority_host

    @property
    def authority_port(self) -> Optional[int]:
        return self.as_dns.authority_port

    @property
    def host(self) -> str:
        return self.as_dns.host

    @property
    def port(self) -> Optional[int]:
        return self.as_dns.port

    @property
    def path(self) -> str:
        return self.as_unix.path

    @property
    def abstract_path(self) -> str:
        return self.as_unix_abstract.abstract_path

    @property
    def addresses(self) -> List[Address]:
        if self.is_ipv4:
            assert isinstance(self.rpc_address, RpcIpv4Addresses)
            return self.rpc_address.addresses
        elif self.is_ipv6:
            assert isinstance(self.rpc_address, RpcIpv6Addresses)
            return self.rpc_address.addresses
        else:
            raise TypeError("Only IPv4 or IPv6 schemes are supported")

    def encode(self) -> str:
        return self.rpc_address.encode()

    def __str__(self) -> str:
        return self.encode()

    def __repr__(self) -> str:
        return self.encode()


def parse_rpc_address_as_class(address: str) -> RpcAddress:
    scheme, rpc_address = parse_rpc_address(address)
    return RpcAddress(scheme, rpc_address)
