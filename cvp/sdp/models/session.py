# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Optional

from cvp.sdp.models.attribute import Attribute
from cvp.sdp.models.bandwidth import Bandwidth
from cvp.sdp.models.connection import Connection
from cvp.sdp.models.media import MediaDescription
from cvp.sdp.models.origin import Origin
from cvp.sdp.models.timing import Timing


@dataclass
class SessionDescription:
    """SDP session description.

    Represents a complete SDP document.
    """

    # Required fields
    version: int = 0
    origin: Optional[Origin] = None
    session_name: str = "-"

    # Optional session-level fields
    session_info: Optional[str] = None
    uri: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    connection: Optional[Connection] = None
    bandwidths: List[Bandwidth] = field(default_factory=list)
    timing: Optional[Timing] = None

    # Session-level attributes
    attributes: List[Attribute] = field(default_factory=list)

    # Media descriptions
    media: List[MediaDescription] = field(default_factory=list)

    def encode(self) -> str:
        lines = []

        # Version (required)
        lines.append(f"v={self.version}")

        # Origin (required)
        if self.origin is not None:
            lines.append(self.origin.encode())

        # Session name (required)
        lines.append(f"s={self.session_name}")

        # Session information (optional)
        if self.session_info is not None:
            lines.append(f"i={self.session_info}")

        # URI (optional)
        if self.uri is not None:
            lines.append(f"u={self.uri}")

        # Email (optional)
        if self.email is not None:
            lines.append(f"e={self.email}")

        # Phone (optional)
        if self.phone is not None:
            lines.append(f"p={self.phone}")

        # Connection (optional)
        if self.connection is not None:
            lines.append(self.connection.encode())

        # Bandwidths
        for bw in self.bandwidths:
            lines.append(bw.encode())

        # Timing (required for valid SDP)
        if self.timing is not None:
            lines.append(self.timing.encode())

        # Session-level attributes
        for attr in self.attributes:
            lines.append(attr.encode())

        # Media descriptions
        for m in self.media:
            lines.append(m.encode())

        return "\r\n".join(lines)

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
    def ice_ufrag(self) -> Optional[str]:
        return self.get_attribute_value("ice-ufrag")

    @property
    def ice_pwd(self) -> Optional[str]:
        return self.get_attribute_value("ice-pwd")

    @property
    def fingerprint(self) -> Optional[str]:
        return self.get_attribute_value("fingerprint")

    def __str__(self) -> str:
        return self.encode()
