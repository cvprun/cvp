# -*- coding: utf-8 -*-

from subprocess import check_output
from typing import Any, List, Optional, Tuple

from orjson import loads

from cvp.ffmpeg.ffprobe.models import (
    AudioStreamInfo,
    FormatInfo,
    MediaInfo,
    SubtitleStreamInfo,
    VideoStreamInfo,
)


def inspect_source(
    src: str,
    *,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> Any:
    ffprobe_command = [
        ffprobe,
        "-v",
        "quiet",
        "-rtsp_transport",
        "tcp",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        src,
    ]
    return loads(check_output(ffprobe_command, timeout=timeout))


def inspect_media(
    src: str,
    *,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> MediaInfo:
    data = inspect_source(src, timeout=timeout, ffprobe=ffprobe)
    streams = data.get("streams", [])
    format_data = data.get("format", {})

    video_streams = [
        VideoStreamInfo.from_dict(s) for s in streams if s.get("codec_type") == "video"
    ]
    audio_streams = [
        AudioStreamInfo.from_dict(s) for s in streams if s.get("codec_type") == "audio"
    ]
    subtitle_streams = [
        SubtitleStreamInfo.from_dict(s)
        for s in streams
        if s.get("codec_type") == "subtitle"
    ]

    return MediaInfo(
        format=FormatInfo.from_dict(format_data),
        video_streams=video_streams,
        audio_streams=audio_streams,
        subtitle_streams=subtitle_streams,
    )


def inspect_streams(
    src: str,
    *,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> List[Any]:
    data = inspect_source(src, timeout=timeout, ffprobe=ffprobe)
    return data.get("streams", [])


def inspect_video_streams(
    src: str,
    *,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> List[VideoStreamInfo]:
    streams = inspect_streams(src, timeout=timeout, ffprobe=ffprobe)
    return [
        VideoStreamInfo.from_dict(s) for s in streams if s.get("codec_type") == "video"
    ]


def inspect_audio_streams(
    src: str,
    *,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> List[AudioStreamInfo]:
    streams = inspect_streams(src, timeout=timeout, ffprobe=ffprobe)
    return [
        AudioStreamInfo.from_dict(s) for s in streams if s.get("codec_type") == "audio"
    ]


def get_duration(
    src: str,
    *,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> Optional[float]:
    data = inspect_source(src, timeout=timeout, ffprobe=ffprobe)
    format_data = data.get("format", {})
    duration = format_data.get("duration")
    return float(duration) if duration else None


def get_bitrate(
    src: str,
    *,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> Optional[int]:
    data = inspect_source(src, timeout=timeout, ffprobe=ffprobe)
    format_data = data.get("format", {})
    bit_rate = format_data.get("bit_rate")
    return int(bit_rate) if bit_rate else None


def get_format_name(
    src: str,
    *,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> Optional[str]:
    data = inspect_source(src, timeout=timeout, ffprobe=ffprobe)
    format_data = data.get("format", {})
    return format_data.get("format_name")


def inspect_frames(
    src: str,
    *,
    stream_index: Optional[int] = None,
    read_intervals: Optional[str] = None,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> List[Any]:
    ffprobe_command = [
        ffprobe,
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_frames",
    ]
    if stream_index is not None:
        ffprobe_command.extend(["-select_streams", str(stream_index)])
    if read_intervals is not None:
        ffprobe_command.extend(["-read_intervals", read_intervals])
    ffprobe_command.append(src)

    data = loads(check_output(ffprobe_command, timeout=timeout))
    return data.get("frames", [])


def inspect_packets(
    src: str,
    *,
    stream_index: Optional[int] = None,
    read_intervals: Optional[str] = None,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> List[Any]:
    ffprobe_command = [
        ffprobe,
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_packets",
    ]
    if stream_index is not None:
        ffprobe_command.extend(["-select_streams", str(stream_index)])
    if read_intervals is not None:
        ffprobe_command.extend(["-read_intervals", read_intervals])
    ffprobe_command.append(src)

    data = loads(check_output(ffprobe_command, timeout=timeout))
    return data.get("packets", [])


def count_frames(
    src: str,
    *,
    stream_index: Optional[int] = None,
    timeout: Optional[float] = None,
    ffprobe: str = "ffprobe",
) -> int:
    ffprobe_command = [
        ffprobe,
        "-v",
        "quiet",
        "-count_frames",
        "-print_format",
        "json",
        "-show_streams",
    ]
    if stream_index is not None:
        ffprobe_command.extend(["-select_streams", str(stream_index)])
    ffprobe_command.append(src)

    data = loads(check_output(ffprobe_command, timeout=timeout))
    streams = data.get("streams", [])

    total_frames = 0
    for stream in streams:
        nb_read_frames = stream.get("nb_read_frames")
        if nb_read_frames:
            total_frames += int(nb_read_frames)
    return total_frames


def inspect_video_frame_size(
    src: str,
    video_stream_index=0,
    *,
    timeout: Optional[float] = None,
    ffprobe="ffprobe",
) -> Tuple[int, int]:
    inspect_result = inspect_source(src, timeout=timeout, ffprobe=ffprobe)
    assert isinstance(inspect_result, dict)

    streams = inspect_result["streams"]
    video_streams = list(filter(lambda x: x["codec_type"] == "video", streams))
    video_stream_map = {int(stream["index"]): stream for stream in video_streams}
    video_stream = video_stream_map[video_stream_index]

    width = video_stream["width"]
    height = video_stream["height"]
    assert isinstance(width, int)
    assert isinstance(height, int)

    return width, height
