# -*- coding: utf-8 -*-

from typing import List, Optional

from cvp.sdp.models.attribute import Attribute
from cvp.sdp.models.bandwidth import Bandwidth
from cvp.sdp.models.connection import Connection
from cvp.sdp.models.media import MediaDescription
from cvp.sdp.models.origin import Origin
from cvp.sdp.models.rtpmap import Fmtp, RtcpFb, RtpMap
from cvp.sdp.models.session import SessionDescription
from cvp.sdp.models.timing import Timing


def _split_lines(sdp_text: str) -> List[str]:
    """Split SDP text into lines, handling both CRLF and LF."""
    lines = sdp_text.replace("\r\n", "\n").split("\n")
    return [line for line in lines if line.strip()]


def _parse_media_attributes(media: MediaDescription, line: str) -> None:
    """Parse a media-level attribute line."""
    if line.startswith("a=rtpmap:"):
        media.rtpmaps.append(RtpMap.parse(line))
    elif line.startswith("a=fmtp:"):
        media.fmtps.append(Fmtp.parse(line))
    elif line.startswith("a=rtcp-fb:"):
        media.rtcp_fbs.append(RtcpFb.parse(line))
    elif line.startswith("a="):
        media.attributes.append(Attribute.parse(line))


def parse_sdp(sdp_text: str) -> SessionDescription:
    """Parse an SDP string into a SessionDescription object.

    Args:
        sdp_text: The SDP text to parse.

    Returns:
        A SessionDescription object representing the parsed SDP.

    Raises:
        ValueError: If the SDP is malformed.
    """
    lines = _split_lines(sdp_text)
    session = SessionDescription()

    current_media: Optional[MediaDescription] = None

    for line in lines:
        if not line:
            continue

        line_type = line[0] if line else ""

        # Check for media description start
        if line.startswith("m="):
            # Save previous media if exists
            if current_media is not None:
                session.media.append(current_media)
            current_media = MediaDescription.parse_media_line(line)
            continue

        # If we're in a media description, parse media-level fields
        if current_media is not None:
            if line.startswith("i="):
                current_media.title = line[2:]
            elif line.startswith("c="):
                current_media.connection = Connection.parse(line)
            elif line.startswith("b="):
                current_media.bandwidths.append(Bandwidth.parse(line))
            elif line.startswith("a="):
                _parse_media_attributes(current_media, line)
            continue

        # Session-level fields
        if line_type == "v":
            session.version = int(line[2:])
        elif line_type == "o":
            session.origin = Origin.parse(line)
        elif line_type == "s":
            session.session_name = line[2:]
        elif line_type == "i":
            session.session_info = line[2:]
        elif line_type == "u":
            session.uri = line[2:]
        elif line_type == "e":
            session.email = line[2:]
        elif line_type == "p":
            session.phone = line[2:]
        elif line_type == "c":
            session.connection = Connection.parse(line)
        elif line_type == "b":
            session.bandwidths.append(Bandwidth.parse(line))
        elif line_type == "t":
            session.timing = Timing.parse(line)
        elif line_type == "a":
            session.attributes.append(Attribute.parse(line))

    # Don't forget the last media description
    if current_media is not None:
        session.media.append(current_media)

    return session
