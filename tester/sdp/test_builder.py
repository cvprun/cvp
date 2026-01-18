# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.sdp.builder import sdp
from cvp.sdp.parser import parse_sdp


class SdpBuilderTestCase(TestCase):
    def test_basic_sdp(self) -> None:
        result = (
            sdp()
            .origin("-", "123456", 2, "IN", "IP4", "127.0.0.1")
            .session_name("-")
            .timing(0, 0)
            .done()
        )
        lines = result.strip().split("\r\n")
        self.assertEqual("v=0", lines[0])
        self.assertEqual("o=- 123456 2 IN IP4 127.0.0.1", lines[1])
        self.assertEqual("s=-", lines[2])
        self.assertEqual("t=0 0", lines[3])

    def test_with_connection(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("Test")
            .connection("0.0.0.0")
            .timing(0, 0)
            .done()
        )
        self.assertIn("c=IN IP4 0.0.0.0\r\n", result)

    def test_with_media(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96, 97])
            .attr_mid("0")
            .attr_rtpmap(96, "H264", 90000)
            .attr_sendrecv()
            .done()
        )
        self.assertIn("m=video 9 UDP/TLS/RTP/SAVPF 96 97\r\n", result)
        self.assertIn("a=mid:0\r\n", result)
        self.assertIn("a=rtpmap:96 H264/90000\r\n", result)
        self.assertIn("a=sendrecv\r\n", result)

    def test_ice_attributes(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .attr_ice_ufrag("abcd")
            .attr_ice_pwd("secretpwd")
            .attr_ice_options("trickle")
            .done()
        )
        self.assertIn("a=ice-ufrag:abcd\r\n", result)
        self.assertIn("a=ice-pwd:secretpwd\r\n", result)
        self.assertIn("a=ice-options:trickle\r\n", result)

    def test_fingerprint_and_setup(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .attr_fingerprint("sha-256", "AB:CD:EF:00")
            .attr_setup("actpass")
            .done()
        )
        self.assertIn("a=fingerprint:sha-256 AB:CD:EF:00\r\n", result)
        self.assertIn("a=setup:actpass\r\n", result)

    def test_rtpmap_with_params(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("audio", 9, "UDP/TLS/RTP/SAVPF", [111])
            .attr_rtpmap(111, "opus", 48000, "2")
            .done()
        )
        self.assertIn("a=rtpmap:111 opus/48000/2\r\n", result)

    def test_fmtp(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_fmtp(96, "profile-level-id=42e01f")
            .done()
        )
        self.assertIn("a=fmtp:96 profile-level-id=42e01f\r\n", result)

    def test_rtcp_fb(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_rtcp_fb(96, "nack")
            .attr_rtcp_fb(96, "nack", "pli")
            .done()
        )
        self.assertIn("a=rtcp-fb:96 nack\r\n", result)
        self.assertIn("a=rtcp-fb:96 nack pli\r\n", result)

    def test_group_and_msid_semantic(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .attr_group("BUNDLE", "0", "1")
            .attr_msid_semantic("WMS", "stream1")
            .done()
        )
        self.assertIn("a=group:BUNDLE 0 1\r\n", result)
        self.assertIn("a=msid-semantic:WMS stream1\r\n", result)

    def test_ssrc(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_ssrc(12345678, "cname", "test")
            .done()
        )
        self.assertIn("a=ssrc:12345678 cname:test\r\n", result)

    def test_candidate(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_candidate("1", 1, "UDP", 2122260223, "192.168.1.1", 54321, "host")
            .done()
        )
        self.assertIn(
            "a=candidate:1 1 UDP 2122260223 192.168.1.1 54321 typ host\r\n",
            result,
        )

    def test_candidate_with_relay(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_candidate(
                "2",
                1,
                "UDP",
                1000,
                "1.2.3.4",
                5678,
                "relay",
                raddr="192.168.1.1",
                rport=54321,
            )
            .done()
        )
        expected = (
            "a=candidate:2 1 UDP 1000 1.2.3.4 5678 typ relay "
            "raddr 192.168.1.1 rport 54321\r\n"
        )
        self.assertIn(expected, result)

    def test_extmap(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_extmap(1, "urn:ietf:params:rtp-hdrext:toffset")
            .done()
        )
        self.assertIn("a=extmap:1 urn:ietf:params:rtp-hdrext:toffset\r\n", result)

    def test_rid_and_simulcast(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_rid("q", "send")
            .attr_rid("h", "send")
            .attr_simulcast(send="q;h")
            .done()
        )
        self.assertIn("a=rid:q send\r\n", result)
        self.assertIn("a=rid:h send\r\n", result)
        self.assertIn("a=simulcast:send q;h\r\n", result)

    def test_direction_methods(self) -> None:
        for direction in ("sendrecv", "sendonly", "recvonly", "inactive"):
            result = (
                sdp()
                .origin("-", "1", 1)
                .session_name("-")
                .timing(0, 0)
                .attr_direction(direction)
                .done()
            )
            self.assertIn(f"a={direction}\r\n", result)

    def test_rtcp_mux(self) -> None:
        result = (
            sdp()
            .origin("-", "1", 1)
            .session_name("-")
            .timing(0, 0)
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_rtcp_mux()
            .done()
        )
        self.assertIn("a=rtcp-mux\r\n", result)

    def test_roundtrip(self) -> None:
        """Test that build -> parse -> encode produces consistent results."""
        original = (
            sdp()
            .origin("-", "123", 2, "IN", "IP4", "127.0.0.1")
            .session_name("Test Session")
            .timing(0, 0)
            .attr_ice_ufrag("abcd")
            .attr_ice_pwd("1234")
            .media("video", 9, "UDP/TLS/RTP/SAVPF", [96])
            .attr_mid("0")
            .attr_rtpmap(96, "H264", 90000)
            .attr_sendrecv()
            .attr_rtcp_mux()
            .done()
        )

        parsed = parse_sdp(original)
        self.assertEqual(0, parsed.version)
        self.assertIsNotNone(parsed.origin)
        assert parsed.origin is not None
        self.assertEqual("-", parsed.origin.username)
        self.assertEqual("123", parsed.origin.sess_id)
        self.assertEqual("Test Session", parsed.session_name)
        self.assertEqual(1, len(parsed.media))
        self.assertEqual("video", parsed.media[0].media)
        self.assertEqual(9, parsed.media[0].port)
        self.assertEqual("0", parsed.media[0].mid)
        self.assertEqual("sendrecv", parsed.media[0].direction)


if __name__ == "__main__":
    main()
