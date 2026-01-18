# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.sdp.models.rtpmap import Fmtp, RtcpFb, RtpMap


class RtpMapTestCase(TestCase):
    def test_encode(self) -> None:
        rtpmap = RtpMap(
            payload_type=96,
            encoding_name="H264",
            clock_rate=90000,
        )
        self.assertEqual("a=rtpmap:96 H264/90000", rtpmap.encode())

    def test_encode_with_params(self) -> None:
        rtpmap = RtpMap(
            payload_type=111,
            encoding_name="opus",
            clock_rate=48000,
            encoding_params="2",
        )
        self.assertEqual("a=rtpmap:111 opus/48000/2", rtpmap.encode())

    def test_parse(self) -> None:
        rtpmap = RtpMap.parse("a=rtpmap:96 VP8/90000")
        self.assertEqual(96, rtpmap.payload_type)
        self.assertEqual("VP8", rtpmap.encoding_name)
        self.assertEqual(90000, rtpmap.clock_rate)
        self.assertIsNone(rtpmap.encoding_params)

    def test_parse_with_params(self) -> None:
        rtpmap = RtpMap.parse("a=rtpmap:111 opus/48000/2")
        self.assertEqual(111, rtpmap.payload_type)
        self.assertEqual("opus", rtpmap.encoding_name)
        self.assertEqual(48000, rtpmap.clock_rate)
        self.assertEqual("2", rtpmap.encoding_params)

    def test_parse_invalid(self) -> None:
        with self.assertRaises(ValueError):
            RtpMap.parse("invalid")


class FmtpTestCase(TestCase):
    def test_encode(self) -> None:
        fmtp = Fmtp(
            format=96,
            params="level-asymmetry-allowed=1;packetization-mode=1",
        )
        expected = "a=fmtp:96 level-asymmetry-allowed=1;packetization-mode=1"
        self.assertEqual(expected, fmtp.encode())

    def test_parse(self) -> None:
        fmtp = Fmtp.parse("a=fmtp:96 profile-level-id=42e01f")
        self.assertEqual(96, fmtp.format)
        self.assertEqual("profile-level-id=42e01f", fmtp.params)

    def test_parse_invalid(self) -> None:
        with self.assertRaises(ValueError):
            Fmtp.parse("invalid")


class RtcpFbTestCase(TestCase):
    def test_encode(self) -> None:
        rtcp_fb = RtcpFb(payload_type=96, fb_type="nack")
        self.assertEqual("a=rtcp-fb:96 nack", rtcp_fb.encode())

    def test_encode_with_subtype(self) -> None:
        rtcp_fb = RtcpFb(payload_type=96, fb_type="nack", fb_subtype="pli")
        self.assertEqual("a=rtcp-fb:96 nack pli", rtcp_fb.encode())

    def test_parse(self) -> None:
        rtcp_fb = RtcpFb.parse("a=rtcp-fb:96 goog-remb")
        self.assertEqual(96, rtcp_fb.payload_type)
        self.assertEqual("goog-remb", rtcp_fb.fb_type)
        self.assertIsNone(rtcp_fb.fb_subtype)

    def test_parse_with_subtype(self) -> None:
        rtcp_fb = RtcpFb.parse("a=rtcp-fb:96 ccm fir")
        self.assertEqual(96, rtcp_fb.payload_type)
        self.assertEqual("ccm", rtcp_fb.fb_type)
        self.assertEqual("fir", rtcp_fb.fb_subtype)

    def test_parse_invalid(self) -> None:
        with self.assertRaises(ValueError):
            RtcpFb.parse("invalid")


if __name__ == "__main__":
    main()
