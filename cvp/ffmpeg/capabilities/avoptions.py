# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass, field
from enum import IntFlag, StrEnum, unique
from io import StringIO
from re import Pattern
from re import compile as re_compile
from subprocess import check_output
from typing import Deque, Final, List, Optional, Tuple

from cvp.itertools.find import find_element

_AV_OPTION_CONST_PREFIX: Final[str] = "     "
_RANGE_REGEX: Final[Pattern[str]] = re_compile(r" \(from (.+?) to (.+?)\)")
_DEFAULT_REGEX: Final[Pattern[str]] = re_compile(r" \(default (.+?)\)")
_FLAG_REGEX: Final[Pattern[str]] = re_compile(
    r"(.*)([E.][D.][F.][V.][A.][S.][X.][R.][B.][T.][P.])(.*)",
)


@unique
class AVOptionType(StrEnum):
    """An option type determines:

    - for native access, the underlying C type of the field that an AVOption
      refers to;
    - for foreign access, the semantics of accessing the option through this API,
      e.g. which av_opt_get_*() and av_opt_set_*() functions can be called, or
      what format will av_opt_get()/av_opt_set() expect/produce.

    https://github.com/FFmpeg/FFmpeg/blob/master/libavutil/opt.h
    """

    flags = "<flags>"
    """Underlying C type is unsigned int."""

    int = "<int>"
    """Underlying C type is int."""

    int64 = "<int64>"
    """Underlying C type is int64_t."""

    double = "<double>"
    """Underlying C type is double."""

    float = "<float>"
    """Underlying C type is float."""

    string = "<string>"
    """
    Underlying C type is a uint8_t* that is either NULL or points to a C
    string allocated with the av_malloc() family of functions.
    """

    rational = "<rational>"
    """Underlying C type is AVRational."""

    binary = "<binary>"
    """
    Underlying C type is a uint8_t* that is either NULL or points to an array
    allocated with the av_malloc() family of functions. The pointer is
    immediately followed by an int containing the array length in bytes.
    """

    dictionary = "<dictionary>"
    """Underlying C type is AVDictionary*."""

    uint64 = "<uint64>"
    """Underlying C type is uint64_t."""

    image_size = "<image_size>"
    """Underlying C type is two consecutive integers."""

    pix_fmt = "<pix_fmt>"
    """Underlying C type is enum AVPixelFormat."""

    sample_fmt = "<sample_fmt>"
    """Underlying C type is enum AVSampleFormat."""

    video_rate = "<video_rate>"
    """Underlying C type is AVRational."""

    duration = "<duration>"
    """Underlying C type is int64_t."""

    color = "<color>"
    """Underlying C type is uint8_t[4]."""

    boolean = "<boolean>"
    """Underlying C type is int."""

    channel_layout = "<channel_layout>"
    """Underlying C type is AVChannelLayout."""

    unsigned = "<unsigned>"
    """Underlying C type is unsigned int."""


@unique
class AVOptionFlag(IntFlag):
    encoding = 1 << 0
    """A generic parameter which can be set by the user for muxing or encoding."""

    decoding = 1 << 1
    """A generic parameter which can be set by the user for demuxing or decoding."""

    audio = 1 << 3
    video = 1 << 4
    subtitle = 1 << 5

    export = 1 << 6
    """The option is intended for exporting values to the caller."""

    readonly = 1 << 7
    """
    The option may not be set through the AVOptions API, only read.
    This flag only makes sense when AV_OPT_FLAG_EXPORT is also set.
    """

    bsf = 1 << 8
    """A generic parameter which can be set by the user for bit stream filtering."""

    runtime = 1 << 15
    """A generic parameter which can be set by the user at runtime."""

    filtering = 1 << 16
    """A generic parameter which can be set by the user for filtering."""

    deprecated = 1 << 17
    """Set if option is deprecated,
    users should refer to AVOption.help text for more information.
    """

    child_consts = 1 << 18
    """Set if option constants can also reside in child objects."""

    def __str__(self):
        # https://github.com/FFmpeg/FFmpeg/blob/master/libavutil/opt.c#L1591
        buffer = StringIO()
        buffer.write("E" if bool(self & type(self).encoding) else ".")
        buffer.write("D" if bool(self & type(self).decoding) else ".")
        buffer.write("F" if bool(self & type(self).filtering) else ".")
        buffer.write("V" if bool(self & type(self).video) else ".")
        buffer.write("A" if bool(self & type(self).audio) else ".")
        buffer.write("S" if bool(self & type(self).subtitle) else ".")
        buffer.write("X" if bool(self & type(self).export) else ".")
        buffer.write("R" if bool(self & type(self).readonly) else ".")
        buffer.write("B" if bool(self & type(self).bsf) else ".")
        buffer.write("T" if bool(self & type(self).runtime) else ".")
        buffer.write("P" if bool(self & type(self).deprecated) else ".")
        return buffer.getvalue()

    @classmethod
    def from_text(cls, text: str):
        # https://github.com/FFmpeg/FFmpeg/blob/master/libavutil/opt.c#L1591
        flags = cls(0)
        if text[0] == "E":
            flags |= cls.encoding
        if text[1] == "D":
            flags |= cls.decoding
        if text[2] == "F":
            flags |= cls.filtering
        if text[3] == "V":
            flags |= cls.video
        if text[4] == "A":
            flags |= cls.audio
        if text[5] == "S":
            flags |= cls.subtitle
        if text[6] == "X":
            flags |= cls.export
        if text[7] == "R":
            flags |= cls.readonly
        if text[8] == "B":
            flags |= cls.bsf
        if text[9] == "T":
            flags |= cls.runtime
        if text[10] == "P":
            flags |= cls.deprecated
        return flags


@dataclass
class AVOptionConst:
    name: str
    value: Optional[int]
    flag: AVOptionFlag
    description: Optional[str]


@dataclass
class AVOption:
    name: str
    type: AVOptionType
    flag: AVOptionFlag
    description: Optional[str] = None
    constants: List[AVOptionConst] = field(default_factory=list)
    range: Optional[Tuple[str, str]] = None
    default: Optional[str] = None


@dataclass
class AVOptions:
    name: str = field(default_factory=str)
    options: List[AVOption] = field(default_factory=list)


class AVOptionsFormatError(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


def extract_option_range(text: str) -> Optional[Tuple[str, str]]:
    if match := _RANGE_REGEX.search(text):
        return match.group(1), match.group(2)
    else:
        return None


def extract_option_default(text: str) -> Optional[str]:
    if match := _DEFAULT_REGEX.search(text):
        return match.group(1)
    else:
        return None


def parse_avoptions_with_deque(lines: Deque[str]) -> AVOptions:
    lines_deque = deque(lines)
    result = AVOptions()

    # Find AVOptions Title
    while lines_deque:
        try:
            line = lines_deque.popleft()
        except IndexError:
            break

        if not line.strip():
            # Skip empty line
            continue

        if not line.endswith("AVOptions:"):
            raise ValueError("Unexpected AVOptions title format")

        result.name = line.removesuffix("AVOptions:").strip()
        break

    if not result.name:
        raise ValueError("Could not find AVOptions title")

    while lines_deque:
        try:
            line = lines_deque.popleft()
        except IndexError:
            break

        if line.startswith(_AV_OPTION_CONST_PREFIX):
            if 0 == len(result.options):
                # If the const prefix ('     ') comes at the beginning,
                # it means the previous `AVOption` has already been added.
                raise AVOptionsFormatError("AVOptions must have at least one option")

            name_more = line.split(maxsplit=1)
            if 2 != len(name_more):
                raise AVOptionsFormatError("Invalid AVOptionConst format")

            const_name = name_more[0]
            more = name_more[1]
            assert isinstance(const_name, str)
            assert isinstance(more, str)

            const_match = _FLAG_REGEX.match(more)
            if const_match is None:
                raise AVOptionsFormatError("Not found AVOptionConst's flag format")

            const_value_text = const_match.group(1).strip()
            const_flag_text = const_match.group(2)
            const_desc_text = const_match.group(3).strip()

            const_value = int(const_value_text) if const_value_text else None
            const_flag = AVOptionFlag.from_text(const_flag_text)
            const_desc = str(const_desc_text) or None

            const = AVOptionConst(const_name, const_value, const_flag, const_desc)
            result.options[-1].constants.append(const)
        else:
            option_items = line.split(maxsplit=3)
            if len(option_items) not in (3, 4):
                raise AVOptionsFormatError("Invalid AVOption format")

            opt_name = option_items[0]
            opt_type = option_items[1]
            opt_flag = option_items[2]
            opt_desc = option_items[3] if 4 <= len(option_items) else str()

            option = AVOption(
                name=opt_name,
                type=AVOptionType(opt_type),
                flag=AVOptionFlag.from_text(opt_flag),
                description=opt_desc,
                constants=list(),
                range=extract_option_range(opt_desc),
                default=extract_option_default(opt_desc),
            )
            result.options.append(option)

    return result


def parse_avoptions_with_text(text: str) -> AVOptions:
    lines = deque(text.splitlines(keepends=False))
    return parse_avoptions_with_deque(lines)


@dataclass
class _SectionRange:
    begin: int
    end: int


def parse_avoptions_output(text: str) -> List[AVOptions]:
    result = list()
    lines = text.splitlines(keepends=False)
    section_range: Optional[_SectionRange] = None

    for i, line in enumerate(lines):
        if line:
            if section_range is not None:
                section_range.end += 1
            else:
                section_range = _SectionRange(i, i + 1)
        else:
            if section_range is not None:
                begin = section_range.begin
                end = section_range.end
                try:
                    options = parse_avoptions_with_deque(deque(lines[begin:end]))
                    result.append(options)
                except AVOptionsFormatError:
                    raise
                except ValueError:
                    pass
                finally:
                    section_range = None
            else:
                pass

    return result


def inspect_avoptions(ffmpeg="ffmpeg") -> List[AVOptions]:
    cmds = ffmpeg, "-hide_banner", "-h", "full"
    output = check_output(cmds).decode("utf-8")
    return parse_avoptions_output(output)


def find_avoptions(name: str, ffmpeg="ffmpeg") -> AVOptions:
    return find_element(inspect_avoptions(ffmpeg), lambda x: x.name == name)
