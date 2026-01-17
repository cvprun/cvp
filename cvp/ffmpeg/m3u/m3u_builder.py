# -*- coding: utf-8 -*-

from functools import reduce
from io import StringIO
from typing import Any, Iterable, List, Optional, Tuple, Union, get_args

from cvp.ffmpeg.m3u.m3u_tags import (
    EXT_X_BITRATE,
    EXT_X_BYTERANGE,
    EXT_X_DATERANGE,
    EXT_X_DEFINE,
    EXT_X_DISCONTINUITY,
    EXT_X_DISCONTINUITY_SEQUENCE,
    EXT_X_ENDLIST,
    EXT_X_GAP,
    EXT_X_I_FRAME_STREAM_INF,
    EXT_X_I_FRAMES_ONLY,
    EXT_X_INDEPENDENT_SEGMENTS,
    EXT_X_KEY,
    EXT_X_MAP,
    EXT_X_MEDIA,
    EXT_X_MEDIA_SEQUENCE,
    EXT_X_PART,
    EXT_X_PART_INF,
    EXT_X_PLAYLIST_TYPE,
    EXT_X_PRELOAD_HINT,
    EXT_X_PROGRAM_DATE_TIME,
    EXT_X_RENDITION_REPORT,
    EXT_X_SERVER_CONTROL,
    EXT_X_SESSION_DATA,
    EXT_X_SESSION_KEY,
    EXT_X_SKIP,
    EXT_X_START,
    EXT_X_STREAM_INF,
    EXT_X_TARGETDURATION,
    EXT_X_VERSION,
    EXTINF,
    EXTM3U,
    ExtXKey_MethodLiteral,
    ExtXMedia_TypeLiteral,
    ExtXPlaylistTypeLiteral,
    ExtXPreloadHint_TypeLiteral,
    ExtXStreamInf_HdcpLevelLiteral,
    ExtXStreamInf_VideoRangeLiteral,
    ExtXVersionLiteral,
)

_required = object()
_no_quoting = object()
_append_comma = object()


def _raise_enum_error(name: str, literal_cls):
    raise ValueError(
        f"The `{name}` argument must be one of the following values:"
        f"{get_args(literal_cls)}"
    )


class M3uBuilder:
    def __init__(self, master: Optional[bool] = None):
        self._master = master
        self._lines: List[str] = list()

    def done(self) -> str:
        buffer = StringIO()
        for line in self._lines:
            if not line:
                buffer.write("\n")
                continue
            if line[-1] == "\n":
                buffer.write(line)
            else:
                buffer.write(line + "\n")
        return buffer.getvalue().strip()

    def write(self, line: str) -> "M3uBuilder":
        self._lines.append(line.strip())
        return self

    def newline(self):
        return self.write("\n")

    @staticmethod
    def make_attribute_list(
        tag: str,
        *attribute_list: Optional[Tuple[str, Any]],
    ) -> str:
        buffer = StringIO()

        for attribute in attribute_list:
            if attribute is None:
                continue

            assert len(attribute) >= 2
            key = attribute[0]
            val = attribute[1]
            assert key

            if len(attribute) >= 3:
                flags = attribute[2:]
                no_quoting = _no_quoting in flags
                required = _required in flags
            else:
                no_quoting = False
                required = False

            if val is None:
                if required:
                    raise ValueError(f"The `{key}` value of `{tag}` is REQUIRED")
                else:
                    continue

            if buffer.tell():
                buffer.write(",")

            if isinstance(val, bool):
                boolean_val = "YES" if val else "NO"
                buffer.write(f"{key}={boolean_val}")
            elif isinstance(val, str):
                if no_quoting:
                    buffer.write(f"{key}={val}")
                else:
                    buffer.write(f'{key}="{val}"')
            else:
                buffer.write(f"{key}={val}")

        if buffer.tell():
            return f"{tag}:{buffer.getvalue()}"
        else:
            return tag

    def write_attribute_list(self, tag: str, *attribute_list):
        return self.write(self.make_attribute_list(tag, *attribute_list))

    # ----------
    # Basic Tags
    # ----------

    def extm3u(self):
        return self.write(EXTM3U)

    def ext_x_version(self, n: Union[int, ExtXVersionLiteral]):
        return self.write(f"{EXT_X_VERSION}:{n}")

    # -----------------------------
    # Media or Master Playlist Tags
    # -----------------------------

    def ext_x_independent_segments(self):
        return self.write(EXT_X_INDEPENDENT_SEGMENTS)

    def ext_x_start(
        self,
        time_offset: Optional[float] = None,
        precise: Optional[bool] = None,
    ):
        return self.write_attribute_list(
            EXT_X_START,
            ("TIME-OFFSET", time_offset),
            ("PRECISE", precise),
        )

    def ext_x_define(
        self,
        name: Optional[str] = None,
        value: Optional[str] = None,
        import_: Optional[str] = None,
    ):
        if name is not None and value is None:
            raise ValueError("If `name` exists, then `value` must also exist")
        if name is None and value is not None:
            raise ValueError(
                "If `name` does not exist then `value` must not exist either"
            )

        if self._master and import_ is not None:
            raise ValueError("`IMPORT` attribute MUST NOT occur in master playlists")

        return self.write_attribute_list(
            EXT_X_DEFINE,
            ("NAME", name),
            ("VALUE", value),
            ("IMPORT", import_),
        )

    # -------------------
    # Media Playlist Tags
    # -------------------

    def ext_x_targetduration(self, s: int):
        return self.write(f"{EXT_X_TARGETDURATION}:{s}")

    def ext_x_media_sequence(self, number: int):
        return self.write(f"{EXT_X_MEDIA_SEQUENCE}:{number}")

    def ext_x_discontinuity_sequence(self, number: int):
        return self.write(f"{EXT_X_DISCONTINUITY_SEQUENCE}:{number}")

    def ext_x_endlist(self):
        return self.write(EXT_X_ENDLIST)

    def ext_x_playlist_type(
        self,
        type_: Union[str, ExtXPlaylistTypeLiteral],
    ) -> "M3uBuilder":
        if type_ not in get_args(ExtXPlaylistTypeLiteral):
            _raise_enum_error("type_", ExtXPlaylistTypeLiteral)
        return self.write(f"{EXT_X_PLAYLIST_TYPE}:{type_}")

    def ext_x_i_frames_only(self) -> "M3uBuilder":
        return self.write(EXT_X_I_FRAMES_ONLY)

    def ext_x_part_inf(
        self,
        part_target: float,
    ) -> "M3uBuilder":
        return self.write_attribute_list(
            EXT_X_PART_INF,
            ("PART-TARGET", part_target, _required),
        )

    def ext_x_server_control(
        self,
        can_skip_until: Optional[float] = None,
        can_skip_dateranges: Optional[bool] = None,
        hold_back: Optional[float] = None,
        part_hold_back: Optional[float] = None,
        can_block_reload: Optional[bool] = None,
    ) -> "M3uBuilder":
        return self.write_attribute_list(
            EXT_X_SERVER_CONTROL,
            ("CAN-SKIP-UNTIL", can_skip_until),
            ("CAN-SKIP-DATERANGES", can_skip_dateranges),
            ("HOLD-BACK", hold_back),
            ("PART-HOLD-BACK", part_hold_back),
            ("CAN-BLOCK-RELOAD", can_block_reload),
        )

    # ------------------
    # Media Segment Tags
    # ------------------

    def extinf(self, duration: float, title: Optional[str] = None):
        if title:
            return self.write(f"{EXTINF}:{duration},{title}")
        else:
            # In the spec, must include commas(',').
            return self.write(f"{EXTINF}:{duration},")

    def extinf_uri(self, uri: str, *args, **kwargs):
        return self.extinf(*args, **kwargs).write(uri)

    def ext_x_byterange(
        self,
        length: int,
        offset: Optional[int] = None,
    ) -> "M3uBuilder":
        if offset is not None:
            return self.write(f"{EXT_X_BYTERANGE}:{length}@{offset}")
        else:
            return self.write(f"{EXT_X_BYTERANGE}:{length}")

    def ext_x_discontinuity(self) -> "M3uBuilder":
        return self.write(EXT_X_DISCONTINUITY)

    def ext_x_key(
        self,
        method: Union[str, ExtXKey_MethodLiteral],
        uri: Optional[str] = None,
        iv: Optional[str] = None,
        keyformat: Optional[str] = None,
        keyformatversions: Optional[str] = None,
    ):
        if method not in get_args(ExtXKey_MethodLiteral):
            _raise_enum_error("method", ExtXKey_MethodLiteral)

        if method != "NONE" and not uri:
            raise ValueError(
                "The `URI` attribute is REQUIRED unless the METHOD is NONE"
            )

        return self.write_attribute_list(
            EXT_X_KEY,
            ("METHOD", method, _required, _no_quoting),
            ("URI", uri),
            ("IV", iv),  # hexadecimal-sequence 128-bit
            ("KEYFORMAT", keyformat),
            ("KEYFORMATVERSIONS", keyformatversions),
        )

    def ext_x_map(
        self,
        uri: str,
        byterange: Optional[str] = None,
    ) -> "M3uBuilder":
        return self.write_attribute_list(
            EXT_X_MAP,
            ("URI", uri, _required),
            ("BYTERANGE", byterange),
        )

    def ext_x_program_date_time(
        self,
        date_time: str,
    ) -> "M3uBuilder":
        return self.write(f"{EXT_X_PROGRAM_DATE_TIME}:{date_time}")

    def ext_x_gap(self) -> "M3uBuilder":
        return self.write(EXT_X_GAP)

    def ext_x_bitrate(
        self,
        rate: int,
    ) -> "M3uBuilder":
        return self.write(f"{EXT_X_BITRATE}:{rate}")

    def ext_x_part(
        self,
        uri: str,
        duration: float,
        independent: Optional[bool] = None,
        byterange: Optional[str] = None,
        gap: Optional[bool] = None,
    ) -> "M3uBuilder":
        return self.write_attribute_list(
            EXT_X_PART,
            ("URI", uri, _required),
            ("DURATION", duration, _required),
            ("INDEPENDENT", independent),
            ("BYTERANGE", byterange),
            ("GAP", gap),
        )

    # -------------------
    # Media Metadata Tags
    # -------------------

    def ext_x_daterange(
        self,
        id_: str,
        class_: Optional[str] = None,
        start_date: Optional[str] = None,
        cue: Optional[str] = None,
        end_date: Optional[str] = None,
        duration: Optional[float] = None,
        planned_duration: Optional[float] = None,
        end_on_next: Optional[bool] = None,
        scte35_cmd: Optional[str] = None,
        scte35_out: Optional[str] = None,
        scte35_in: Optional[str] = None,
    ) -> "M3uBuilder":
        return self.write_attribute_list(
            EXT_X_DATERANGE,
            ("ID", id_, _required),
            ("CLASS", class_),
            ("START-DATE", start_date),
            ("CUE", cue),
            ("END-DATE", end_date),
            ("DURATION", duration),
            ("PLANNED-DURATION", planned_duration),
            ("END-ON-NEXT", end_on_next),
            ("SCTE35-CMD", scte35_cmd),
            ("SCTE35-OUT", scte35_out),
            ("SCTE35-IN", scte35_in),
        )

    def ext_x_skip(
        self,
        skipped_segments: int,
        recently_removed_dateranges: Optional[str] = None,
    ) -> "M3uBuilder":
        return self.write_attribute_list(
            EXT_X_SKIP,
            ("SKIPPED-SEGMENTS", skipped_segments, _required),
            ("RECENTLY-REMOVED-DATERANGES", recently_removed_dateranges),
        )

    def ext_x_preload_hint(
        self,
        type_: Union[str, ExtXPreloadHint_TypeLiteral],
        uri: str,
        byterange_start: Optional[int] = None,
        byterange_length: Optional[int] = None,
    ) -> "M3uBuilder":
        if type_ not in get_args(ExtXPreloadHint_TypeLiteral):
            _raise_enum_error("type_", ExtXPreloadHint_TypeLiteral)
        return self.write_attribute_list(
            EXT_X_PRELOAD_HINT,
            ("TYPE", type_, _required, _no_quoting),
            ("URI", uri, _required),
            ("BYTERANGE-START", byterange_start),
            ("BYTERANGE-LENGTH", byterange_length),
        )

    def ext_x_rendition_report(
        self,
        uri: str,
        last_msn: Optional[int] = None,
        last_part: Optional[int] = None,
    ) -> "M3uBuilder":
        return self.write_attribute_list(
            EXT_X_RENDITION_REPORT,
            ("URI", uri, _required),
            ("LAST-MSN", last_msn),
            ("LAST-PART", last_part),
        )

    # --------------------
    # Master Playlist Tags
    # --------------------

    def ext_x_media(
        self,
        type_: Union[str, ExtXMedia_TypeLiteral],
        group_id: str,
        name: str,
        language: Optional[str] = None,
        assoc_language: Optional[str] = None,
        default: Optional[bool] = None,
        autoselect: Optional[bool] = None,
        forced: Optional[bool] = None,
        instream_id: Optional[str] = None,
        characteristics: Optional[str] = None,
        channels: Optional[str] = None,
        uri: Optional[str] = None,
    ) -> "M3uBuilder":
        if type_ not in get_args(ExtXMedia_TypeLiteral):
            _raise_enum_error("type_", ExtXMedia_TypeLiteral)
        return self.write_attribute_list(
            EXT_X_MEDIA,
            ("TYPE", type_, _required, _no_quoting),
            ("GROUP-ID", group_id, _required),
            ("NAME", name, _required),
            ("LANGUAGE", language),
            ("ASSOC-LANGUAGE", assoc_language),
            ("DEFAULT", default),
            ("AUTOSELECT", autoselect),
            ("FORCED", forced),
            ("INSTREAM-ID", instream_id),
            ("CHARACTERISTICS", characteristics),
            ("CHANNELS", channels),
            ("URI", uri),
        )

    def ext_x_stream_inf(
        self,
        bandwidth: int,
        average_bandwidth: Optional[int] = None,
        score: Optional[float] = None,
        codecs: Optional[Iterable[str]] = None,
        resolution: Optional[Tuple[int, int]] = None,
        frame_rate: Optional[float] = None,
        hdcp_level: Optional[Union[str, ExtXStreamInf_HdcpLevelLiteral]] = None,
        allowed_cpc: Optional[str] = None,
        video_range: Optional[Union[str, ExtXStreamInf_VideoRangeLiteral]] = None,
        stable_variant_id: Optional[str] = None,
        audio: Optional[str] = None,
        video: Optional[str] = None,
        subtitles: Optional[str] = None,
        closed_captions: Optional[str] = None,
    ):
        if hdcp_level and hdcp_level not in get_args(ExtXStreamInf_HdcpLevelLiteral):
            _raise_enum_error("hdcp_level", ExtXStreamInf_HdcpLevelLiteral)
        if video_range and video_range not in get_args(ExtXStreamInf_VideoRangeLiteral):
            _raise_enum_error("video_range", ExtXStreamInf_VideoRangeLiteral)

        if codecs:
            merged_codecs = reduce(lambda x, y: x + "," + y, codecs)
        else:
            merged_codecs = None

        if resolution:
            assert len(resolution) == 2
            merged_resolution = f"{resolution[0]}x{resolution[1]}"
        else:
            merged_resolution = None

        return self.write_attribute_list(
            EXT_X_STREAM_INF,
            ("BANDWIDTH", bandwidth, _required),
            ("AVERAGE-BANDWIDTH", average_bandwidth),
            ("SCORE", score),
            ("CODECS", merged_codecs if merged_codecs else None),  # SHOULD
            ("RESOLUTION", merged_resolution, _no_quoting),
            ("FRAME-RATE", frame_rate),
            ("HDCP-LEVEL", hdcp_level, _no_quoting),
            ("ALLOWED-CPC", allowed_cpc),
            ("VIDEO-RANGE", video_range, _no_quoting),
            ("STABLE-VARIANT-ID", stable_variant_id),
            ("AUDIO", audio),
            ("VIDEO", video),
            ("SUBTITLES", subtitles),
            ("CLOSED-CAPTIONS", closed_captions),
        )

    def ext_x_stream_inf_uri(self, uri: str, *args, **kwargs):
        return self.ext_x_stream_inf(*args, **kwargs).write(uri)

    def ext_x_i_frame_stream_inf(
        self,
        bandwidth: int,
        uri: str,
        average_bandwidth: Optional[int] = None,
        score: Optional[float] = None,
        codecs: Optional[Iterable[str]] = None,
        resolution: Optional[Tuple[int, int]] = None,
        hdcp_level: Optional[Union[str, ExtXStreamInf_HdcpLevelLiteral]] = None,
        allowed_cpc: Optional[str] = None,
        video_range: Optional[Union[str, ExtXStreamInf_VideoRangeLiteral]] = None,
        stable_variant_id: Optional[str] = None,
        video: Optional[str] = None,
    ) -> "M3uBuilder":
        if hdcp_level and hdcp_level not in get_args(ExtXStreamInf_HdcpLevelLiteral):
            _raise_enum_error("hdcp_level", ExtXStreamInf_HdcpLevelLiteral)
        if video_range and video_range not in get_args(ExtXStreamInf_VideoRangeLiteral):
            _raise_enum_error("video_range", ExtXStreamInf_VideoRangeLiteral)

        if codecs:
            merged_codecs = reduce(lambda x, y: x + "," + y, codecs)
        else:
            merged_codecs = None

        if resolution:
            assert len(resolution) == 2
            merged_resolution = f"{resolution[0]}x{resolution[1]}"
        else:
            merged_resolution = None

        return self.write_attribute_list(
            EXT_X_I_FRAME_STREAM_INF,
            ("BANDWIDTH", bandwidth, _required),
            ("URI", uri, _required),
            ("AVERAGE-BANDWIDTH", average_bandwidth),
            ("SCORE", score),
            ("CODECS", merged_codecs if merged_codecs else None),
            ("RESOLUTION", merged_resolution, _no_quoting),
            ("HDCP-LEVEL", hdcp_level, _no_quoting),
            ("ALLOWED-CPC", allowed_cpc),
            ("VIDEO-RANGE", video_range, _no_quoting),
            ("STABLE-VARIANT-ID", stable_variant_id),
            ("VIDEO", video),
        )

    def ext_x_session_data(
        self,
        data_id: str,
        value: Optional[str] = None,
        uri: Optional[str] = None,
        format_: Optional[str] = None,
        language: Optional[str] = None,
    ) -> "M3uBuilder":
        if value is None and uri is None:
            raise ValueError("Either `value` or `uri` must be provided")
        if value is not None and uri is not None:
            raise ValueError("Cannot provide both `value` and `uri`")
        return self.write_attribute_list(
            EXT_X_SESSION_DATA,
            ("DATA-ID", data_id, _required),
            ("VALUE", value),
            ("URI", uri),
            ("FORMAT", format_),
            ("LANGUAGE", language),
        )

    def ext_x_session_key(
        self,
        method: Union[str, ExtXKey_MethodLiteral],
        uri: Optional[str] = None,
        iv: Optional[str] = None,
        keyformat: Optional[str] = None,
        keyformatversions: Optional[str] = None,
    ) -> "M3uBuilder":
        if method not in get_args(ExtXKey_MethodLiteral):
            _raise_enum_error("method", ExtXKey_MethodLiteral)

        if method == "NONE":
            raise ValueError("METHOD cannot be NONE for EXT-X-SESSION-KEY")

        if not uri:
            raise ValueError("The `URI` attribute is REQUIRED for EXT-X-SESSION-KEY")

        return self.write_attribute_list(
            EXT_X_SESSION_KEY,
            ("METHOD", method, _required, _no_quoting),
            ("URI", uri, _required),
            ("IV", iv),
            ("KEYFORMAT", keyformat),
            ("KEYFORMATVERSIONS", keyformatversions),
        )


def extm3u(master: Optional[bool] = None) -> M3uBuilder:
    return M3uBuilder(master).extm3u()
