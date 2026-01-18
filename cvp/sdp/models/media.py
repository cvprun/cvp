# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Optional

from cvp.sdp.models.attribute import Attribute
from cvp.sdp.models.bandwidth import Bandwidth
from cvp.sdp.models.connection import Connection
from cvp.sdp.models.rtpmap import Fmtp, RtcpFb, RtpMap


@dataclass
class MediaDescription:
    """SDP media description (m=).

    Format: m=<media> <port> <proto> <fmt> ...
    """

    media: str
    port: int
    proto: str
    formats: List[str] = field(default_factory=list)

    # Media-level optional fields
    title: Optional[str] = None
    connection: Optional[Connection] = None
    bandwidths: List[Bandwidth] = field(default_factory=list)

    # Parsed attributes
    rtpmaps: List[RtpMap] = field(default_factory=list)
    fmtps: List[Fmtp] = field(default_factory=list)
    rtcp_fbs: List[RtcpFb] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)

    def encode(self) -> str:
        lines = []
        fmt_str = " ".join(self.formats)
        lines.append(f"m={self.media} {self.port} {self.proto} {fmt_str}")

        if self.title is not None:
            lines.append(f"i={self.title}")

        if self.connection is not None:
            lines.append(self.connection.encode())

        for bw in self.bandwidths:
            lines.append(bw.encode())

        for rtpmap in self.rtpmaps:
            lines.append(rtpmap.encode())

        for fmtp in self.fmtps:
            lines.append(fmtp.encode())

        for rtcp_fb in self.rtcp_fbs:
            lines.append(rtcp_fb.encode())

        for attr in self.attributes:
            lines.append(attr.encode())

        return "\r\n".join(lines)

    @classmethod
    def parse_media_line(cls, line: str) -> "MediaDescription":
        if not line.startswith("m="):
            raise ValueError(f"Invalid media line: {line}")
        content = line[2:]
        parts = content.split()
        if len(parts) < 4:
            raise ValueError(f"Invalid media format: {line}")
        return cls(
            media=parts[0],
            port=int(parts[1]),
            proto=parts[2],
            formats=parts[3:],
        )

    def get_attribute(self, name: str) -> Optional[Attribute]:
        for attr in self.attributes:
            if attr.name == name:
                return attr
        return None

    def get_attribute_value(self, name: str) -> Optional[str]:
        attr = self.get_attribute(name)
        return attr.value if attr else None

    def has_attribute(self, name: str) -> bool:
        return self.get_attribute(name) is not None

    @property
    def mid(self) -> Optional[str]:
        return self.get_attribute_value("mid")

    @property
    def direction(self) -> Optional[str]:
        for d in ("sendrecv", "sendonly", "recvonly", "inactive"):
            if self.has_attribute(d):
                return d
        return None

    def __str__(self) -> str:
        return self.encode()
