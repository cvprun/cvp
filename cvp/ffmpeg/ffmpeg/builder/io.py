# -*- coding: utf-8 -*-

from shlex import split
from typing import List, Optional, Tuple, Union

from cvp.ffmpeg.utils.video_size import VIDEO_SIZES
from cvp.types.override import override


class FileBuilder:
    _options: List[str]

    def __init__(self, base, file: str):
        self._base = base
        self._options = list()
        self._file = file
        self._done = False

    def as_args(self) -> List[str]:
        raise NotImplementedError

    def clear(self) -> None:
        self._options.clear()
        self._done = False

    def append(self, *args: str):
        if self._done:
            raise ValueError("The 'done' flag is already set")

        self._options += args
        return self

    def append_with_text(self, text: str, *, comments=False, posix=True):
        return self.append(*split(text, comments=comments, posix=posix))

    def done(self):
        self._done = True

        # [IMPORTANT] Avoid 'circular import' issues
        from cvp.ffmpeg.ffmpeg.builder import FFmpegBuilder

        assert isinstance(self._base, FFmpegBuilder)
        return self._base

    def find_s(
        self,
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> str:
        """
        -s[:stream_specifier] size (input/output,per-stream)

        Set frame size.
        """
        value = f"-s:{stream_specifier}" if stream_specifier is not None else "-s"
        return self._options[self._options.index(value) + 1]

    @staticmethod
    def parse_s(text: str) -> Tuple[int, int]:
        if text in VIDEO_SIZES:
            return VIDEO_SIZES[text]
        else:
            width, height = text.split("x")
            return int(width), int(height)


class InputFileBuilder(FileBuilder):
    @classmethod
    def from_stdin(cls, base):
        return cls(base, "pipe:0")

    @override
    def as_args(self) -> List[str]:
        return self._options + ["-i", self._file]

    def seek(self, position: Union[str, float]) -> "InputFileBuilder":
        """
        -ss position (input/output)
        Seek to given time position in seconds or HH:MM:SS format.
        """
        return self.append("-ss", str(position))

    def duration(self, duration: Union[str, float]) -> "InputFileBuilder":
        """
        -t duration (input/output)
        Stop reading the input after duration seconds.
        """
        return self.append("-t", str(duration))

    def to(self, position: Union[str, float]) -> "InputFileBuilder":
        """
        -to position (input/output)
        Stop reading at position.
        """
        return self.append("-to", str(position))

    def format_(self, fmt: str) -> "InputFileBuilder":
        """
        -f fmt (input/output)
        Force input format.
        """
        return self.append("-f", fmt)

    def stream_loop(self, number: int) -> "InputFileBuilder":
        """
        -stream_loop number (input)
        Set number of times input stream shall be looped.
        """
        return self.append("-stream_loop", str(number))

    def re(self) -> "InputFileBuilder":
        """
        -re (input)
        Read input at native frame rate.
        """
        return self.append("-re")

    def readrate(self, speed: float) -> "InputFileBuilder":
        """
        -readrate speed (input)
        Read input at specified rate.
        """
        return self.append("-readrate", str(speed))


class OutputFileBuilder(FileBuilder):
    @classmethod
    def from_stdout(cls, base):
        return cls(base, "pipe:1")

    @classmethod
    def from_stderr(cls, base):
        return cls(base, "pipe:2")

    @override
    def as_args(self) -> List[str]:
        return self._options + [self._file]

    def codec_video(
        self,
        codec: str,
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> "OutputFileBuilder":
        """
        -c:v codec (output)
        Select video codec for encoding.
        """
        if stream_specifier is not None:
            return self.append(f"-c:v:{stream_specifier}", codec)
        return self.append("-c:v", codec)

    def codec_audio(
        self,
        codec: str,
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> "OutputFileBuilder":
        """
        -c:a codec (output)
        Select audio codec for encoding.
        """
        if stream_specifier is not None:
            return self.append(f"-c:a:{stream_specifier}", codec)
        return self.append("-c:a", codec)

    def bitrate_video(
        self,
        bitrate: str,
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> "OutputFileBuilder":
        """
        -b:v bitrate (output)
        Set video bitrate (e.g., "1M", "500k").
        """
        if stream_specifier is not None:
            return self.append(f"-b:v:{stream_specifier}", bitrate)
        return self.append("-b:v", bitrate)

    def bitrate_audio(
        self,
        bitrate: str,
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> "OutputFileBuilder":
        """
        -b:a bitrate (output)
        Set audio bitrate (e.g., "128k", "192k").
        """
        if stream_specifier is not None:
            return self.append(f"-b:a:{stream_specifier}", bitrate)
        return self.append("-b:a", bitrate)

    def framerate(
        self,
        fps: Union[str, int, float],
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> "OutputFileBuilder":
        """
        -r fps (output)
        Set frame rate.
        """
        if stream_specifier is not None:
            return self.append(f"-r:{stream_specifier}", str(fps))
        return self.append("-r", str(fps))

    def video_size(
        self,
        size: Union[str, Tuple[int, int]],
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> "OutputFileBuilder":
        """
        -s size (output)
        Set frame size (WxH or predefined size name).
        """
        if isinstance(size, tuple):
            size_str = f"{size[0]}x{size[1]}"
        else:
            size_str = size
        if stream_specifier is not None:
            return self.append(f"-s:{stream_specifier}", size_str)
        return self.append("-s", size_str)

    def pixel_format(
        self,
        pix_fmt: str,
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> "OutputFileBuilder":
        """
        -pix_fmt format (output)
        Set pixel format.
        """
        if stream_specifier is not None:
            return self.append(f"-pix_fmt:{stream_specifier}", pix_fmt)
        return self.append("-pix_fmt", pix_fmt)

    def video_filter(self, filter_graph: str) -> "OutputFileBuilder":
        """
        -vf filtergraph (output)
        Apply video filtergraph.
        """
        return self.append("-vf", filter_graph)

    def audio_filter(self, filter_graph: str) -> "OutputFileBuilder":
        """
        -af filtergraph (output)
        Apply audio filtergraph.
        """
        return self.append("-af", filter_graph)

    def preset(self, preset: str) -> "OutputFileBuilder":
        """
        -preset preset (output)
        Set encoding preset (ultrafast, fast, medium, slow, etc.).
        """
        return self.append("-preset", preset)

    def crf(self, value: int) -> "OutputFileBuilder":
        """
        -crf value (output)
        Set Constant Rate Factor for quality-based encoding.
        """
        return self.append("-crf", str(value))

    def tune(self, tune: str) -> "OutputFileBuilder":
        """
        -tune tune (output)
        Tune encoder settings for specific content.
        """
        return self.append("-tune", tune)

    def profile(
        self,
        profile: str,
        stream_specifier: Optional[Union[str, int]] = None,
    ) -> "OutputFileBuilder":
        """
        -profile:v profile (output)
        Set encoding profile.
        """
        if stream_specifier is not None:
            return self.append(f"-profile:v:{stream_specifier}", profile)
        return self.append("-profile:v", profile)

    def map(
        self,
        input_file_index: int,
        stream_specifier: Optional[str] = None,
        optional: bool = False,
    ) -> "OutputFileBuilder":
        """
        -map input_file_index[:stream_specifier] (output)
        Map input streams to output.
        """
        map_spec = f"{input_file_index}"
        if stream_specifier is not None:
            map_spec = f"{map_spec}:{stream_specifier}"
        if optional:
            map_spec = f"-{map_spec}?"
        return self.append("-map", map_spec)

    def format_(self, fmt: str) -> "OutputFileBuilder":
        """
        -f fmt (output)
        Force output format.
        """
        return self.append("-f", fmt)

    def seek(self, position: Union[str, float]) -> "OutputFileBuilder":
        """
        -ss position (output)
        Seek in output.
        """
        return self.append("-ss", str(position))

    def duration(self, duration: Union[str, float]) -> "OutputFileBuilder":
        """
        -t duration (output)
        Stop writing the output after duration seconds.
        """
        return self.append("-t", str(duration))

    def to(self, position: Union[str, float]) -> "OutputFileBuilder":
        """
        -to position (output)
        Stop writing at position.
        """
        return self.append("-to", str(position))

    def movflags(self, flags: str) -> "OutputFileBuilder":
        """
        -movflags flags (output)
        Set MOV/MP4 muxer flags.
        """
        return self.append("-movflags", flags)

    def metadata(
        self,
        key: str,
        value: str,
        stream_specifier: Optional[str] = None,
    ) -> "OutputFileBuilder":
        """
        -metadata[:stream_specifier] key=value (output)
        Set metadata.
        """
        if stream_specifier is not None:
            return self.append(f"-metadata:{stream_specifier}", f"{key}={value}")
        return self.append("-metadata", f"{key}={value}")
