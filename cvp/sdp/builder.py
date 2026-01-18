# -*- coding: utf-8 -*-

from io import StringIO
from typing import List, Optional, Sequence, Union


class SdpBuilder:
    """Fluent builder for SDP (Session Description Protocol) documents."""

    def __init__(self) -> None:
        self._lines: List[str] = []

    def done(self) -> str:
        """Build and return the complete SDP string."""
        buffer = StringIO()
        for line in self._lines:
            buffer.write(line)
            buffer.write("\r\n")
        return buffer.getvalue()

    def _write(self, line: str) -> "SdpBuilder":
        self._lines.append(line)
        return self

    # =====================
    # Session-level fields
    # =====================

    def version(self, v: int = 0) -> "SdpBuilder":
        """v=<version>"""
        return self._write(f"v={v}")

    def origin(
        self,
        username: str,
        sess_id: str,
        sess_version: int,
        nettype: str = "IN",
        addrtype: str = "IP4",
        unicast_address: str = "127.0.0.1",
    ) -> "SdpBuilder":
        """o=<username> <sess-id> <sess-version> <nettype> <addrtype> <address>"""
        return self._write(
            f"o={username} {sess_id} {sess_version} {nettype} {addrtype} "
            f"{unicast_address}"
        )

    def session_name(self, name: str = "-") -> "SdpBuilder":
        """s=<session-name>"""
        return self._write(f"s={name}")

    def session_info(self, info: str) -> "SdpBuilder":
        """i=<session-info>"""
        return self._write(f"i={info}")

    def uri(self, uri: str) -> "SdpBuilder":
        """u=<uri>"""
        return self._write(f"u={uri}")

    def email(self, email: str) -> "SdpBuilder":
        """e=<email>"""
        return self._write(f"e={email}")

    def phone(self, phone: str) -> "SdpBuilder":
        """p=<phone>"""
        return self._write(f"p={phone}")

    def connection(
        self,
        address: str,
        nettype: str = "IN",
        addrtype: str = "IP4",
    ) -> "SdpBuilder":
        """c=<nettype> <addrtype> <connection-address>"""
        return self._write(f"c={nettype} {addrtype} {address}")

    def bandwidth(self, bwtype: str, bandwidth: int) -> "SdpBuilder":
        """b=<bwtype>:<bandwidth>"""
        return self._write(f"b={bwtype}:{bandwidth}")

    def timing(self, start: int = 0, stop: int = 0) -> "SdpBuilder":
        """t=<start-time> <stop-time>"""
        return self._write(f"t={start} {stop}")

    # ==================
    # Generic attributes
    # ==================

    def attr(self, name: str, value: Optional[str] = None) -> "SdpBuilder":
        """a=<name> or a=<name>:<value>"""
        if value is not None:
            return self._write(f"a={name}:{value}")
        return self._write(f"a={name}")

    def attr_group(self, semantics: str, *mids: str) -> "SdpBuilder":
        """a=group:<semantics> <mid> ..."""
        mid_str = " ".join(mids)
        return self._write(f"a=group:{semantics} {mid_str}")

    def attr_msid_semantic(
        self,
        semantic: str = "WMS",
        *stream_ids: str,
    ) -> "SdpBuilder":
        """a=msid-semantic:<semantic> <stream-id> ..."""
        if stream_ids:
            ids = " ".join(stream_ids)
            return self._write(f"a=msid-semantic:{semantic} {ids}")
        return self._write(f"a=msid-semantic:{semantic}")

    # ==============
    # ICE attributes
    # ==============

    def attr_ice_ufrag(self, ufrag: str) -> "SdpBuilder":
        """a=ice-ufrag:<ufrag>"""
        return self.attr("ice-ufrag", ufrag)

    def attr_ice_pwd(self, pwd: str) -> "SdpBuilder":
        """a=ice-pwd:<pwd>"""
        return self.attr("ice-pwd", pwd)

    def attr_ice_options(self, *options: str) -> "SdpBuilder":
        """a=ice-options:<option> ..."""
        return self.attr("ice-options", " ".join(options))

    def attr_ice_lite(self) -> "SdpBuilder":
        """a=ice-lite"""
        return self.attr("ice-lite")

    # ===============
    # DTLS attributes
    # ===============

    def attr_fingerprint(
        self,
        hash_func: str,
        fingerprint: str,
    ) -> "SdpBuilder":
        """a=fingerprint:<hash-func> <fingerprint>"""
        return self.attr("fingerprint", f"{hash_func} {fingerprint}")

    def attr_setup(self, role: str) -> "SdpBuilder":
        """a=setup:<role>"""
        return self.attr("setup", role)

    # =================
    # Media description
    # =================

    def media(
        self,
        media: str,
        port: int,
        proto: str,
        formats: Sequence[Union[int, str]],
    ) -> "SdpBuilder":
        """m=<media> <port> <proto> <fmt> ..."""
        fmt_str = " ".join(str(f) for f in formats)
        return self._write(f"m={media} {port} {proto} {fmt_str}")

    # ======================
    # Media-level attributes
    # ======================

    def attr_mid(self, mid: str) -> "SdpBuilder":
        """a=mid:<mid>"""
        return self.attr("mid", mid)

    def attr_rtpmap(
        self,
        payload_type: int,
        encoding_name: str,
        clock_rate: int,
        encoding_params: Optional[str] = None,
    ) -> "SdpBuilder":
        """a=rtpmap:<pt> <encoding>/<rate>[/<params>]"""
        if encoding_params is not None:
            value = f"{encoding_name}/{clock_rate}/{encoding_params}"
        else:
            value = f"{encoding_name}/{clock_rate}"
        return self._write(f"a=rtpmap:{payload_type} {value}")

    def attr_fmtp(self, format_: int, params: str) -> "SdpBuilder":
        """a=fmtp:<format> <params>"""
        return self._write(f"a=fmtp:{format_} {params}")

    def attr_rtcp_fb(
        self,
        payload_type: int,
        fb_type: str,
        fb_subtype: Optional[str] = None,
    ) -> "SdpBuilder":
        """a=rtcp-fb:<pt> <type> [<subtype>]"""
        if fb_subtype is not None:
            return self._write(f"a=rtcp-fb:{payload_type} {fb_type} {fb_subtype}")
        return self._write(f"a=rtcp-fb:{payload_type} {fb_type}")

    def attr_rtcp(
        self,
        port: int,
        nettype: Optional[str] = None,
        addrtype: Optional[str] = None,
        address: Optional[str] = None,
    ) -> "SdpBuilder":
        """a=rtcp:<port> [<nettype> <addrtype> <address>]"""
        if nettype and addrtype and address:
            return self.attr("rtcp", f"{port} {nettype} {addrtype} {address}")
        return self.attr("rtcp", str(port))

    def attr_rtcp_mux(self) -> "SdpBuilder":
        """a=rtcp-mux"""
        return self.attr("rtcp-mux")

    def attr_rtcp_mux_only(self) -> "SdpBuilder":
        """a=rtcp-mux-only"""
        return self.attr("rtcp-mux-only")

    def attr_rtcp_rsize(self) -> "SdpBuilder":
        """a=rtcp-rsize"""
        return self.attr("rtcp-rsize")

    # ====================
    # Direction attributes
    # ====================

    def attr_direction(self, direction: str) -> "SdpBuilder":
        """a=sendrecv, a=sendonly, a=recvonly, or a=inactive"""
        return self.attr(direction)

    def attr_sendrecv(self) -> "SdpBuilder":
        """a=sendrecv"""
        return self.attr("sendrecv")

    def attr_sendonly(self) -> "SdpBuilder":
        """a=sendonly"""
        return self.attr("sendonly")

    def attr_recvonly(self) -> "SdpBuilder":
        """a=recvonly"""
        return self.attr("recvonly")

    def attr_inactive(self) -> "SdpBuilder":
        """a=inactive"""
        return self.attr("inactive")

    # ===============
    # SSRC attributes
    # ===============

    def attr_ssrc(
        self,
        ssrc: int,
        attribute: str,
        value: Optional[str] = None,
    ) -> "SdpBuilder":
        """a=ssrc:<ssrc> <attribute>[:<value>]"""
        if value is not None:
            return self._write(f"a=ssrc:{ssrc} {attribute}:{value}")
        return self._write(f"a=ssrc:{ssrc} {attribute}")

    def attr_ssrc_group(self, semantics: str, *ssrcs: int) -> "SdpBuilder":
        """a=ssrc-group:<semantics> <ssrc> ..."""
        ssrc_str = " ".join(str(s) for s in ssrcs)
        return self._write(f"a=ssrc-group:{semantics} {ssrc_str}")

    # =============
    # ICE candidate
    # =============

    def attr_candidate(
        self,
        foundation: str,
        component: int,
        transport: str,
        priority: int,
        address: str,
        port: int,
        typ: str,
        raddr: Optional[str] = None,
        rport: Optional[int] = None,
        **extensions: str,
    ) -> "SdpBuilder":
        """
        a=candidate:<foundation> <component> <transport> <priority> <address> <port>
        typ <type> [raddr <addr>] [rport <port>] [<ext>]
        """
        parts = [
            f"candidate:{foundation}",
            str(component),
            transport,
            str(priority),
            address,
            str(port),
            "typ",
            typ,
        ]
        if raddr is not None:
            parts.extend(["raddr", raddr])
        if rport is not None:
            parts.extend(["rport", str(rport)])
        for key, val in extensions.items():
            parts.extend([key, val])
        return self._write("a=" + " ".join(parts))

    def attr_end_of_candidates(self) -> "SdpBuilder":
        """a=end-of-candidates"""
        return self.attr("end-of-candidates")

    # =================
    # Extmap attributes
    # =================

    def attr_extmap(
        self,
        id_: int,
        uri: str,
        direction: Optional[str] = None,
    ) -> "SdpBuilder":
        """a=extmap:<id>[/<direction>] <uri>"""
        if direction is not None:
            return self._write(f"a=extmap:{id_}/{direction} {uri}")
        return self._write(f"a=extmap:{id_} {uri}")

    # ===============
    # Simulcast / RID
    # ===============

    def attr_rid(
        self,
        rid_id: str,
        direction: str,
        params: Optional[str] = None,
    ) -> "SdpBuilder":
        """a=rid:<id> <direction> [<params>]"""
        if params is not None:
            return self._write(f"a=rid:{rid_id} {direction} {params}")
        return self._write(f"a=rid:{rid_id} {direction}")

    def attr_simulcast(
        self,
        send: Optional[str] = None,
        recv: Optional[str] = None,
    ) -> "SdpBuilder":
        """a=simulcast:send <send-list> recv <recv-list>"""
        parts = []
        if send is not None:
            parts.extend(["send", send])
        if recv is not None:
            parts.extend(["recv", recv])
        return self.attr("simulcast", " ".join(parts))


def sdp() -> SdpBuilder:
    """Create a new SDP builder starting with v=0."""
    return SdpBuilder().version(0)
