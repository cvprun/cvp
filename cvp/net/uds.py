# -*- coding: utf-8 -*-

from typing import Final

ACCEPTED_UDS_PORT_NUMBER: Final[int] = 1
"""The accepted UDS(Unix Domain Socket) port number is fixed as `1`.

Reference:
 - File: grpc/src/core/lib/iomgr/unix_sockets_posix.cc
 - Func: grpc_resolve_unix_domain_address
"""

UNIX_URI_PREFIX: Final[str] = "unix:"
"""Prefix of UDS(Unix Domain Socket).

Reference:
 - Site: `gRPC Name Resolution <https://grpc.github.io/grpc/cpp/md_doc_naming.html>`_
 - File: grpc/src/core/ext/transport/chttp2/server/chttp2_server.cc
"""

UNIX_ABSTRACT_URI_PREFIX: Final[str] = "unix-abstract:"
"""Prefix of UDS(Unix Domain Socket) in abstract namespace.

Reference:
 - Site: `gRPC Name Resolution <https://grpc.github.io/grpc/cpp/md_doc_naming.html>`_
 - File: grpc/src/core/ext/transport/chttp2/server/chttp2_server.cc
"""


def is_uds_family(address: str) -> bool:
    """
    Make sure it is a Unix Domain Socket (UDS) address.
    """
    if address.startswith(UNIX_URI_PREFIX):
        return True
    if address.startswith(UNIX_ABSTRACT_URI_PREFIX):
        return True
    return False
