# -*- coding: utf-8 -*-

import socket
from typing import Optional, Union


def _is_inet_server_running(
    family: socket.AddressFamily,
    host: str,
    port: int,
    timeout: float,
) -> bool:
    assert family in (socket.AddressFamily.AF_INET, socket.AddressFamily.AF_INET6)
    sock = socket.socket(family, socket.SOCK_STREAM)
    try:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0
    except BaseException:  # noqa
        return False
    finally:
        sock.close()


def is_ipv4_server_running(host: str, port: int, timeout: float) -> bool:
    return _is_inet_server_running(socket.AF_INET, host, port, timeout)


def is_ipv6_server_running(host: str, port: int, timeout: float) -> bool:
    return _is_inet_server_running(socket.AF_INET6, host, port, timeout)


def resolve_tcp_addresses(
    host: Optional[Union[str, bytes]] = None,
    port: Optional[Union[str, bytes, int]] = None,
):
    return socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)


def resolve_udp_addresses(
    host: Optional[Union[str, bytes]] = None,
    port: Optional[Union[str, bytes, int]] = None,
):
    return socket.getaddrinfo(host, port, proto=socket.IPPROTO_UDP)


def is_tcp_server_running(
    host: Union[str, bytes],
    port: Union[str, bytes, int],
    timeout: float,
) -> bool:
    for addr_info in resolve_tcp_addresses(host, port):
        family = addr_info[0]
        kind = addr_info[1]
        proto = addr_info[2]
        canon_name = addr_info[3]
        sockaddr = addr_info[4]

        assert kind == socket.SocketKind.SOCK_STREAM
        assert proto == socket.IPPROTO_TCP
        assert isinstance(canon_name, str)  # Anything is fine.
        if family == socket.AddressFamily.AF_INET:
            assert isinstance(sockaddr, tuple)
            assert 2 == len(sockaddr)
            # socket_host = sockaddr[0]
            # socket_port = sockaddr[1]
        elif family == socket.AddressFamily.AF_INET6:
            assert isinstance(sockaddr, tuple)
            assert 4 == len(sockaddr)
            # socket_host = sockaddr[0]
            # socket_port = sockaddr[1]
            # socket_flow_info = sockaddr[2]
            # socket_scope_id = sockaddr[3]
        else:
            # Unsupported address family
            continue

        sock = socket.socket(family, kind)
        try:
            sock.settimeout(timeout)
            return sock.connect_ex(sockaddr) == 0
        except BaseException:  # noqa
            return False
        finally:
            sock.close()

    return False
