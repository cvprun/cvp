# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Ephemeral_port

from typing import Final

# Ephemeral (Dynamic/Private) ports (49152-65535)
# Reference: IANA, RFC 6335

# Port range boundaries
EPHEMERAL_MIN: Final[int] = 49152
EPHEMERAL_MAX: Final[int] = 65535

# ---------------------------------
# OS-specific ephemeral port ranges
# ---------------------------------

# IANA recommended range (RFC 6335)
IANA_EPHEMERAL_MIN: Final[int] = 49152
IANA_EPHEMERAL_MAX: Final[int] = 65535

# Linux (default since kernel 2.4)
# /proc/sys/net/ipv4/ip_local_port_range
LINUX_EPHEMERAL_MIN: Final[int] = 32768
LINUX_EPHEMERAL_MAX: Final[int] = 60999

# Windows Vista/Server 2008 and later
# netsh int ipv4 show dynamic port tcp
WINDOWS_EPHEMERAL_MIN: Final[int] = 49152
WINDOWS_EPHEMERAL_MAX: Final[int] = 65535

# Windows XP/Server 2003 and earlier
WINDOWS_XP_EPHEMERAL_MIN: Final[int] = 1025
WINDOWS_XP_EPHEMERAL_MAX: Final[int] = 5000

# FreeBSD (default)
FREEBSD_EPHEMERAL_MIN: Final[int] = 49152
FREEBSD_EPHEMERAL_MAX: Final[int] = 65535

# macOS (Darwin)
MACOS_EPHEMERAL_MIN: Final[int] = 49152
MACOS_EPHEMERAL_MAX: Final[int] = 65535

# Solaris
SOLARIS_EPHEMERAL_MIN: Final[int] = 32768
SOLARIS_EPHEMERAL_MAX: Final[int] = 65535

# AIX
AIX_EPHEMERAL_MIN: Final[int] = 32768
AIX_EPHEMERAL_MAX: Final[int] = 65535

# BSD (traditional)
BSD_EPHEMERAL_MIN: Final[int] = 1024
BSD_EPHEMERAL_MAX: Final[int] = 5000
