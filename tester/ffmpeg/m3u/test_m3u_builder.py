# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ffmpeg.m3u.m3u_builder import extm3u


class M3uBuilderTestCase(TestCase):
    def test_extm3u(self) -> None:
        builder = extm3u()
        result = builder.done()
        self.assertEqual(result, "#EXTM3U")

    def test_basic_media_playlist(self) -> None:
        builder = (
            extm3u()
            .ext_x_version(3)
            .ext_x_targetduration(10)
            .ext_x_media_sequence(0)
            .extinf(9.009, "")
            .write("http://example.com/segment0.ts")
            .ext_x_endlist()
        )
        result = builder.done()
        self.assertIn("#EXTM3U", result)
        self.assertIn("#EXT-X-VERSION:3", result)
        self.assertIn("#EXT-X-TARGETDURATION:10", result)
        self.assertIn("#EXTINF:9.009,", result)
        self.assertIn("#EXT-X-ENDLIST", result)

    def test_ext_x_playlist_type(self) -> None:
        builder = extm3u().ext_x_playlist_type("VOD")
        result = builder.done()
        self.assertIn("#EXT-X-PLAYLIST-TYPE:VOD", result)

    def test_ext_x_i_frames_only(self) -> None:
        builder = extm3u().ext_x_i_frames_only()
        result = builder.done()
        self.assertIn("#EXT-X-I-FRAMES-ONLY", result)

    def test_ext_x_part_inf(self) -> None:
        builder = extm3u().ext_x_part_inf(0.5)
        result = builder.done()
        self.assertIn("#EXT-X-PART-INF:PART-TARGET=0.5", result)

    def test_ext_x_server_control(self) -> None:
        builder = extm3u().ext_x_server_control(
            can_skip_until=12.0,
            hold_back=6.0,
            can_block_reload=True,
        )
        result = builder.done()
        self.assertIn("#EXT-X-SERVER-CONTROL:", result)
        self.assertIn("CAN-SKIP-UNTIL=12.0", result)
        self.assertIn("CAN-BLOCK-RELOAD=YES", result)

    def test_ext_x_byterange(self) -> None:
        builder = extm3u().ext_x_byterange(1024, 0)
        result = builder.done()
        self.assertIn("#EXT-X-BYTERANGE:1024@0", result)

    def test_ext_x_discontinuity(self) -> None:
        builder = extm3u().ext_x_discontinuity()
        result = builder.done()
        self.assertIn("#EXT-X-DISCONTINUITY", result)

    def test_ext_x_map(self) -> None:
        builder = extm3u().ext_x_map("init.mp4")
        result = builder.done()
        self.assertIn('#EXT-X-MAP:URI="init.mp4"', result)

    def test_ext_x_program_date_time(self) -> None:
        builder = extm3u().ext_x_program_date_time("2020-01-01T00:00:00.000Z")
        result = builder.done()
        self.assertIn("#EXT-X-PROGRAM-DATE-TIME:2020-01-01T00:00:00.000Z", result)

    def test_ext_x_gap(self) -> None:
        builder = extm3u().ext_x_gap()
        result = builder.done()
        self.assertIn("#EXT-X-GAP", result)

    def test_ext_x_bitrate(self) -> None:
        builder = extm3u().ext_x_bitrate(5000)
        result = builder.done()
        self.assertIn("#EXT-X-BITRATE:5000", result)

    def test_ext_x_part(self) -> None:
        builder = extm3u().ext_x_part("segment.ts", 0.5, independent=True)
        result = builder.done()
        self.assertIn('#EXT-X-PART:URI="segment.ts"', result)
        self.assertIn("DURATION=0.5", result)
        self.assertIn("INDEPENDENT=YES", result)

    def test_ext_x_daterange(self) -> None:
        builder = extm3u().ext_x_daterange(
            "ad-1",
            start_date="2020-01-01T00:00:00.000Z",
            duration=30.0,
        )
        result = builder.done()
        self.assertIn('#EXT-X-DATERANGE:ID="ad-1"', result)
        self.assertIn("DURATION=30.0", result)

    def test_ext_x_skip(self) -> None:
        builder = extm3u().ext_x_skip(5)
        result = builder.done()
        self.assertIn("#EXT-X-SKIP:SKIPPED-SEGMENTS=5", result)

    def test_ext_x_preload_hint(self) -> None:
        builder = extm3u().ext_x_preload_hint("PART", "next-part.ts")
        result = builder.done()
        self.assertIn("#EXT-X-PRELOAD-HINT:", result)
        self.assertIn("TYPE=PART", result)
        self.assertIn('URI="next-part.ts"', result)

    def test_ext_x_rendition_report(self) -> None:
        builder = extm3u().ext_x_rendition_report("other.m3u8", last_msn=10)
        result = builder.done()
        self.assertIn('#EXT-X-RENDITION-REPORT:URI="other.m3u8"', result)
        self.assertIn("LAST-MSN=10", result)

    def test_ext_x_media(self) -> None:
        builder = extm3u().ext_x_media(
            "AUDIO",
            "audio-group",
            "English",
            language="en",
            default=True,
            uri="audio_en.m3u8",
        )
        result = builder.done()
        self.assertIn("#EXT-X-MEDIA:", result)
        self.assertIn("TYPE=AUDIO", result)
        self.assertIn('GROUP-ID="audio-group"', result)
        self.assertIn('NAME="English"', result)
        self.assertIn('LANGUAGE="en"', result)
        self.assertIn("DEFAULT=YES", result)

    def test_ext_x_i_frame_stream_inf(self) -> None:
        builder = extm3u().ext_x_i_frame_stream_inf(
            86000,
            "iframe.m3u8",
            resolution=(640, 480),
        )
        result = builder.done()
        self.assertIn("#EXT-X-I-FRAME-STREAM-INF:", result)
        self.assertIn("BANDWIDTH=86000", result)
        self.assertIn('URI="iframe.m3u8"', result)
        self.assertIn("RESOLUTION=640x480", result)

    def test_ext_x_session_data(self) -> None:
        builder = extm3u().ext_x_session_data("com.example.data", value="test-value")
        result = builder.done()
        self.assertIn('#EXT-X-SESSION-DATA:DATA-ID="com.example.data"', result)
        self.assertIn('VALUE="test-value"', result)

    def test_ext_x_session_key(self) -> None:
        builder = extm3u().ext_x_session_key(
            "AES-128",
            uri="https://example.com/key",
        )
        result = builder.done()
        self.assertIn("#EXT-X-SESSION-KEY:", result)
        self.assertIn("METHOD=AES-128", result)
        self.assertIn('URI="https://example.com/key"', result)


if __name__ == "__main__":
    main()
