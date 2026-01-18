# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.sdp.parser import parse_sdp


class SdpParserTestCase(TestCase):
    def test_parse_minimal(self) -> None:
        sdp_text = "v=0\r\no=- 1 1 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\n"
        session = parse_sdp(sdp_text)

        self.assertEqual(0, session.version)
        self.assertIsNotNone(session.origin)
        assert session.origin is not None
        self.assertEqual("-", session.origin.username)
        self.assertEqual("-", session.session_name)
        self.assertIsNotNone(session.timing)
        assert session.timing is not None
        self.assertEqual(0, session.timing.start_time)

    def test_parse_with_connection(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "c=IN IP4 0.0.0.0\r\n"
            "t=0 0\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertIsNotNone(session.connection)
        assert session.connection is not None
        self.assertEqual("IN", session.connection.nettype)
        self.assertEqual("IP4", session.connection.addrtype)
        self.assertEqual("0.0.0.0", session.connection.connection_address)

    def test_parse_with_media(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "m=video 9 UDP/TLS/RTP/SAVPF 96 97\r\n"
            "a=mid:0\r\n"
            "a=sendrecv\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual(1, len(session.media))
        media = session.media[0]
        self.assertEqual("video", media.media)
        self.assertEqual(9, media.port)
        self.assertEqual("UDP/TLS/RTP/SAVPF", media.proto)
        self.assertEqual(["96", "97"], media.formats)
        self.assertEqual("0", media.mid)
        self.assertEqual("sendrecv", media.direction)

    def test_parse_multiple_media(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "m=audio 9 UDP/TLS/RTP/SAVPF 111\r\n"
            "a=mid:0\r\n"
            "m=video 9 UDP/TLS/RTP/SAVPF 96\r\n"
            "a=mid:1\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual(2, len(session.media))
        self.assertEqual("audio", session.media[0].media)
        self.assertEqual("0", session.media[0].mid)
        self.assertEqual("video", session.media[1].media)
        self.assertEqual("1", session.media[1].mid)

    def test_parse_rtpmap(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "m=video 9 UDP/TLS/RTP/SAVPF 96\r\n"
            "a=rtpmap:96 H264/90000\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual(1, len(session.media[0].rtpmaps))
        rtpmap = session.media[0].rtpmaps[0]
        self.assertEqual(96, rtpmap.payload_type)
        self.assertEqual("H264", rtpmap.encoding_name)
        self.assertEqual(90000, rtpmap.clock_rate)

    def test_parse_rtpmap_with_params(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "m=audio 9 UDP/TLS/RTP/SAVPF 111\r\n"
            "a=rtpmap:111 opus/48000/2\r\n"
        )
        session = parse_sdp(sdp_text)

        rtpmap = session.media[0].rtpmaps[0]
        self.assertEqual(111, rtpmap.payload_type)
        self.assertEqual("opus", rtpmap.encoding_name)
        self.assertEqual(48000, rtpmap.clock_rate)
        self.assertEqual("2", rtpmap.encoding_params)

    def test_parse_fmtp(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "m=video 9 UDP/TLS/RTP/SAVPF 96\r\n"
            "a=fmtp:96 profile-level-id=42e01f\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual(1, len(session.media[0].fmtps))
        fmtp = session.media[0].fmtps[0]
        self.assertEqual(96, fmtp.format)
        self.assertEqual("profile-level-id=42e01f", fmtp.params)

    def test_parse_rtcp_fb(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "m=video 9 UDP/TLS/RTP/SAVPF 96\r\n"
            "a=rtcp-fb:96 nack\r\n"
            "a=rtcp-fb:96 nack pli\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual(2, len(session.media[0].rtcp_fbs))
        self.assertEqual("nack", session.media[0].rtcp_fbs[0].fb_type)
        self.assertIsNone(session.media[0].rtcp_fbs[0].fb_subtype)
        self.assertEqual("nack", session.media[0].rtcp_fbs[1].fb_type)
        self.assertEqual("pli", session.media[0].rtcp_fbs[1].fb_subtype)

    def test_parse_ice_attributes(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "a=ice-ufrag:abcd\r\n"
            "a=ice-pwd:secretpwd\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual("abcd", session.ice_ufrag)
        self.assertEqual("secretpwd", session.ice_pwd)

    def test_parse_fingerprint(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "a=fingerprint:sha-256 AB:CD:EF\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual("sha-256 AB:CD:EF", session.fingerprint)

    def test_parse_bandwidth(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "b=AS:1000\r\n"
            "t=0 0\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual(1, len(session.bandwidths))
        self.assertEqual("AS", session.bandwidths[0].bwtype)
        self.assertEqual(1000, session.bandwidths[0].bandwidth)

    def test_parse_media_bandwidth(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "m=video 9 UDP/TLS/RTP/SAVPF 96\r\n"
            "b=TIAS:500000\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual(1, len(session.media[0].bandwidths))
        self.assertEqual("TIAS", session.media[0].bandwidths[0].bwtype)
        self.assertEqual(500000, session.media[0].bandwidths[0].bandwidth)

    def test_parse_with_lf_only(self) -> None:
        """Test parsing SDP with LF line endings instead of CRLF."""
        sdp_text = "v=0\no=- 1 1 IN IP4 127.0.0.1\ns=-\nt=0 0\n"
        session = parse_sdp(sdp_text)

        self.assertEqual(0, session.version)
        self.assertEqual("-", session.session_name)

    def test_parse_optional_fields(self) -> None:
        sdp_text = (
            "v=0\r\n"
            "o=- 1 1 IN IP4 127.0.0.1\r\n"
            "s=Test Session\r\n"
            "i=Session Info\r\n"
            "u=http://example.com\r\n"
            "e=test@example.com\r\n"
            "p=+1-555-1234\r\n"
            "t=0 0\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual("Test Session", session.session_name)
        self.assertEqual("Session Info", session.session_info)
        self.assertEqual("http://example.com", session.uri)
        self.assertEqual("test@example.com", session.email)
        self.assertEqual("+1-555-1234", session.phone)

    def test_parse_webrtc_offer(self) -> None:
        """Test parsing a realistic WebRTC SDP offer."""
        sdp_text = (
            "v=0\r\n"
            "o=- 4611731400430051336 2 IN IP4 127.0.0.1\r\n"
            "s=-\r\n"
            "t=0 0\r\n"
            "a=group:BUNDLE 0 1\r\n"
            "a=ice-ufrag:abc\r\n"
            "a=ice-pwd:xyz123\r\n"
            "a=fingerprint:sha-256 A1:B2:C3:D4\r\n"
            "a=setup:actpass\r\n"
            "m=audio 9 UDP/TLS/RTP/SAVPF 111\r\n"
            "c=IN IP4 0.0.0.0\r\n"
            "a=mid:0\r\n"
            "a=rtpmap:111 opus/48000/2\r\n"
            "a=fmtp:111 minptime=10;useinbandfec=1\r\n"
            "a=rtcp-mux\r\n"
            "a=sendrecv\r\n"
            "m=video 9 UDP/TLS/RTP/SAVPF 96 97\r\n"
            "c=IN IP4 0.0.0.0\r\n"
            "a=mid:1\r\n"
            "a=rtpmap:96 VP8/90000\r\n"
            "a=rtpmap:97 VP9/90000\r\n"
            "a=rtcp-fb:96 nack\r\n"
            "a=rtcp-fb:96 nack pli\r\n"
            "a=rtcp-mux\r\n"
            "a=sendrecv\r\n"
        )
        session = parse_sdp(sdp_text)

        self.assertEqual(0, session.version)
        self.assertEqual("abc", session.ice_ufrag)
        self.assertEqual("xyz123", session.ice_pwd)
        self.assertEqual("sha-256 A1:B2:C3:D4", session.fingerprint)

        self.assertEqual(2, len(session.media))

        # Audio
        audio = session.media[0]
        self.assertEqual("audio", audio.media)
        self.assertEqual("0", audio.mid)
        self.assertEqual(1, len(audio.rtpmaps))
        self.assertEqual("opus", audio.rtpmaps[0].encoding_name)
        self.assertEqual(1, len(audio.fmtps))
        self.assertTrue(audio.has_attribute("rtcp-mux"))
        self.assertEqual("sendrecv", audio.direction)

        # Video
        video = session.media[1]
        self.assertEqual("video", video.media)
        self.assertEqual("1", video.mid)
        self.assertEqual(2, len(video.rtpmaps))
        self.assertEqual("VP8", video.rtpmaps[0].encoding_name)
        self.assertEqual("VP9", video.rtpmaps[1].encoding_name)
        self.assertEqual(2, len(video.rtcp_fbs))
        self.assertEqual("sendrecv", video.direction)

    def test_roundtrip(self) -> None:
        """Test that parse -> encode -> parse produces consistent results."""
        original_text = (
            "v=0\r\n"
            "o=- 123 2 IN IP4 127.0.0.1\r\n"
            "s=Test\r\n"
            "t=0 0\r\n"
            "a=ice-ufrag:test\r\n"
            "m=video 9 UDP/TLS/RTP/SAVPF 96\r\n"
            "a=mid:0\r\n"
            "a=rtpmap:96 H264/90000\r\n"
            "a=sendrecv\r\n"
        )

        session1 = parse_sdp(original_text)
        encoded = session1.encode()
        session2 = parse_sdp(encoded)

        self.assertIsNotNone(session1.origin)
        self.assertIsNotNone(session2.origin)
        assert session1.origin is not None
        assert session2.origin is not None

        self.assertEqual(session1.version, session2.version)
        self.assertEqual(session1.origin.sess_id, session2.origin.sess_id)
        self.assertEqual(session1.session_name, session2.session_name)
        self.assertEqual(len(session1.media), len(session2.media))
        self.assertEqual(session1.media[0].mid, session2.media[0].mid)


if __name__ == "__main__":
    main()
