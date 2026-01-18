# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class RtpMap:
    """RTP map attribute (a=rtpmap).

    Format: a=rtpmap:<payload-type> <encoding-name>/<clock-rate>[/<encoding-params>]
    """

    payload_type: int
    encoding_name: str
    clock_rate: int
    encoding_params: Optional[str] = None

    def encode(self) -> str:
        if self.encoding_params is not None:
            return (
                f"a=rtpmap:{self.payload_type} "
                f"{self.encoding_name}/{self.clock_rate}/{self.encoding_params}"
            )
        return (
            f"a=rtpmap:{self.payload_type} " f"{self.encoding_name}/{self.clock_rate}"
        )

    @classmethod
    def parse(cls, line: str) -> "RtpMap":
        if not line.startswith("a=rtpmap:"):
            raise ValueError(f"Invalid rtpmap line: {line}")
        content = line[9:]
        parts = content.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Invalid rtpmap format: {line}")
        payload_type = int(parts[0])
        encoding_parts = parts[1].split("/")
        if len(encoding_parts) < 2:
            raise ValueError(f"Invalid rtpmap encoding format: {line}")
        encoding_name = encoding_parts[0]
        clock_rate = int(encoding_parts[1])
        encoding_params = encoding_parts[2] if len(encoding_parts) > 2 else None
        return cls(
            payload_type=payload_type,
            encoding_name=encoding_name,
            clock_rate=clock_rate,
            encoding_params=encoding_params,
        )

    def __str__(self) -> str:
        return self.encode()


@dataclass
class Fmtp:
    """Format parameters attribute (a=fmtp).

    Format: a=fmtp:<format> <format-specific-params>
    """

    format: int
    params: str

    def encode(self) -> str:
        return f"a=fmtp:{self.format} {self.params}"

    @classmethod
    def parse(cls, line: str) -> "Fmtp":
        if not line.startswith("a=fmtp:"):
            raise ValueError(f"Invalid fmtp line: {line}")
        content = line[7:]
        parts = content.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Invalid fmtp format: {line}")
        return cls(format=int(parts[0]), params=parts[1])

    def __str__(self) -> str:
        return self.encode()


@dataclass
class RtcpFb:
    """RTCP feedback attribute (a=rtcp-fb).

    Format: a=rtcp-fb:<payload-type> <fb-type> [<fb-subtype>]
    """

    payload_type: int
    fb_type: str
    fb_subtype: Optional[str] = None

    def encode(self) -> str:
        if self.fb_subtype is not None:
            return f"a=rtcp-fb:{self.payload_type} {self.fb_type} {self.fb_subtype}"
        return f"a=rtcp-fb:{self.payload_type} {self.fb_type}"

    @classmethod
    def parse(cls, line: str) -> "RtcpFb":
        if not line.startswith("a=rtcp-fb:"):
            raise ValueError(f"Invalid rtcp-fb line: {line}")
        content = line[10:]
        parts = content.split(maxsplit=2)
        if len(parts) < 2:
            raise ValueError(f"Invalid rtcp-fb format: {line}")
        payload_type = int(parts[0])
        fb_type = parts[1]
        fb_subtype = parts[2] if len(parts) > 2 else None
        return cls(payload_type=payload_type, fb_type=fb_type, fb_subtype=fb_subtype)

    def __str__(self) -> str:
        return self.encode()
