# -*- coding: utf-8 -*-
"""
Available protocols

ffmpeg -hide_banner -protocols

https://www.ffmpeg.org/ffmpeg-protocols.html
"""

from enum import StrEnum, auto, unique


@unique
class InputProtocols(StrEnum):
    amqp = auto()
    async_ = "async"
    bluray = auto()
    cache = auto()
    concat = auto()
    crypto = auto()
    data = auto()
    ffrtmphttp = auto()
    file = auto()
    ftp = auto()
    gopher = auto()
    gophers = auto()
    hls = auto()
    http = auto()
    httpproxy = auto()
    https = auto()
    mmsh = auto()
    mmst = auto()
    pipe = auto()
    rtmp = auto()
    rtmps = auto()
    rtmpt = auto()
    rtmpts = auto()
    rtp = auto()
    sctp = auto()
    sftp = auto()
    srt = auto()
    srtp = auto()
    subfile = auto()
    tcp = auto()
    tls = auto()
    udp = auto()
    udplite = auto()
    unix = auto()
    zmq = auto()


@unique
class OutputProtocols(StrEnum):
    amqp = auto()
    crypto = auto()
    ffrtmphttp = auto()
    file = auto()
    ftp = auto()
    gopher = auto()
    gophers = auto()
    http = auto()
    httpproxy = auto()
    https = auto()
    icecast = auto()
    md5 = auto()
    pipe = auto()
    prompeg = auto()
    rtmp = auto()
    rtmps = auto()
    rtmpt = auto()
    rtmpts = auto()
    rtp = auto()
    sctp = auto()
    sftp = auto()
    srt = auto()
    srtp = auto()
    tcp = auto()
    tee = auto()
    tls = auto()
    udp = auto()
    udplite = auto()
    unix = auto()
    zmq = auto()
