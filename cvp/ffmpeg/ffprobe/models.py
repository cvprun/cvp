# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VideoStreamInfo:
    index: int
    codec_name: str
    codec_long_name: str
    width: int
    height: int
    pix_fmt: Optional[str] = None
    profile: Optional[str] = None
    level: Optional[int] = None
    color_range: Optional[str] = None
    color_space: Optional[str] = None
    color_transfer: Optional[str] = None
    color_primaries: Optional[str] = None
    field_order: Optional[str] = None
    r_frame_rate: Optional[str] = None
    avg_frame_rate: Optional[str] = None
    time_base: Optional[str] = None
    bit_rate: Optional[int] = None
    nb_frames: Optional[int] = None
    duration: Optional[float] = None
    disposition: Optional[Dict[str, int]] = None
    tags: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VideoStreamInfo":
        return cls(
            index=data["index"],
            codec_name=data.get("codec_name", "unknown"),
            codec_long_name=data.get("codec_long_name", "unknown"),
            width=data["width"],
            height=data["height"],
            pix_fmt=data.get("pix_fmt"),
            profile=data.get("profile"),
            level=data.get("level"),
            color_range=data.get("color_range"),
            color_space=data.get("color_space"),
            color_transfer=data.get("color_transfer"),
            color_primaries=data.get("color_primaries"),
            field_order=data.get("field_order"),
            r_frame_rate=data.get("r_frame_rate"),
            avg_frame_rate=data.get("avg_frame_rate"),
            time_base=data.get("time_base"),
            bit_rate=int(data["bit_rate"]) if data.get("bit_rate") else None,
            nb_frames=int(data["nb_frames"]) if data.get("nb_frames") else None,
            duration=float(data["duration"]) if data.get("duration") else None,
            disposition=data.get("disposition"),
            tags=data.get("tags"),
        )


@dataclass
class AudioStreamInfo:
    index: int
    codec_name: str
    codec_long_name: str
    sample_rate: int
    channels: int
    channel_layout: Optional[str] = None
    sample_fmt: Optional[str] = None
    bits_per_sample: Optional[int] = None
    bit_rate: Optional[int] = None
    nb_frames: Optional[int] = None
    duration: Optional[float] = None
    profile: Optional[str] = None
    disposition: Optional[Dict[str, int]] = None
    tags: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AudioStreamInfo":
        return cls(
            index=data["index"],
            codec_name=data.get("codec_name", "unknown"),
            codec_long_name=data.get("codec_long_name", "unknown"),
            sample_rate=int(data.get("sample_rate", 0)),
            channels=data.get("channels", 0),
            channel_layout=data.get("channel_layout"),
            sample_fmt=data.get("sample_fmt"),
            bits_per_sample=data.get("bits_per_sample"),
            bit_rate=int(data["bit_rate"]) if data.get("bit_rate") else None,
            nb_frames=int(data["nb_frames"]) if data.get("nb_frames") else None,
            duration=float(data["duration"]) if data.get("duration") else None,
            profile=data.get("profile"),
            disposition=data.get("disposition"),
            tags=data.get("tags"),
        )


@dataclass
class SubtitleStreamInfo:
    index: int
    codec_name: str
    codec_long_name: str
    duration: Optional[float] = None
    disposition: Optional[Dict[str, int]] = None
    tags: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SubtitleStreamInfo":
        return cls(
            index=data["index"],
            codec_name=data.get("codec_name", "unknown"),
            codec_long_name=data.get("codec_long_name", "unknown"),
            duration=float(data["duration"]) if data.get("duration") else None,
            disposition=data.get("disposition"),
            tags=data.get("tags"),
        )


@dataclass
class FormatInfo:
    filename: str
    format_name: str
    format_long_name: str
    nb_streams: int
    nb_programs: int
    start_time: Optional[float] = None
    duration: Optional[float] = None
    size: Optional[int] = None
    bit_rate: Optional[int] = None
    probe_score: Optional[int] = None
    tags: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FormatInfo":
        return cls(
            filename=data["filename"],
            format_name=data["format_name"],
            format_long_name=data.get("format_long_name", data["format_name"]),
            nb_streams=data.get("nb_streams", 0),
            nb_programs=data.get("nb_programs", 0),
            start_time=float(data["start_time"]) if data.get("start_time") else None,
            duration=float(data["duration"]) if data.get("duration") else None,
            size=int(data["size"]) if data.get("size") else None,
            bit_rate=int(data["bit_rate"]) if data.get("bit_rate") else None,
            probe_score=data.get("probe_score"),
            tags=data.get("tags"),
        )


@dataclass
class MediaInfo:
    format: FormatInfo
    video_streams: List[VideoStreamInfo]
    audio_streams: List[AudioStreamInfo]
    subtitle_streams: List[SubtitleStreamInfo]

    @property
    def duration(self) -> Optional[float]:
        return self.format.duration

    @property
    def bit_rate(self) -> Optional[int]:
        return self.format.bit_rate

    @property
    def has_video(self) -> bool:
        return len(self.video_streams) > 0

    @property
    def has_audio(self) -> bool:
        return len(self.audio_streams) > 0

    @property
    def primary_video(self) -> Optional[VideoStreamInfo]:
        return self.video_streams[0] if self.video_streams else None

    @property
    def primary_audio(self) -> Optional[AudioStreamInfo]:
        return self.audio_streams[0] if self.audio_streams else None
