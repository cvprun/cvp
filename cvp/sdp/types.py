# -*- coding: utf-8 -*-

from typing import Literal

# Network types (nettype)
NettypeLiteral = Literal["IN"]

# Address types (addrtype)
AddrtypeLiteral = Literal["IP4", "IP6"]

# Media types
MediaTypeLiteral = Literal["audio", "video", "text", "application", "message"]

# Transport protocols
ProtoLiteral = Literal[
    "UDP",
    "RTP/AVP",
    "RTP/SAVP",
    "RTP/SAVPF",
    "UDP/TLS/RTP/SAVP",
    "UDP/TLS/RTP/SAVPF",
    "TCP/TLS/RTP/SAVP",
    "TCP/TLS/RTP/SAVPF",
]

# Bandwidth types
BwtypeLiteral = Literal["CT", "AS", "TIAS"]

# Direction attributes
DirectionLiteral = Literal["sendrecv", "sendonly", "recvonly", "inactive"]

# Setup attribute (RFC 4145)
SetupLiteral = Literal["active", "passive", "actpass", "holdconn"]

# ICE candidate types
IceCandidateTypeLiteral = Literal["host", "srflx", "prflx", "relay"]

# ICE transport types
IceTransportLiteral = Literal["UDP", "TCP"]

# RTCP-MUX attribute
RtcpMuxLiteral = Literal["rtcp-mux", "rtcp-mux-only"]

# RTCP-FB types
RtcpFbTypeLiteral = Literal[
    "ack",
    "nack",
    "ccm",
    "goog-remb",
    "transport-cc",
]
