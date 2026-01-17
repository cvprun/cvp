# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional, Union

from cvp.ffmpeg.filters.filter_builder import make_filter


def scale(
    width: Optional[Union[int, str]] = None,
    height: Optional[Union[int, str]] = None,
    force_original_aspect_ratio: Optional[str] = None,
    flags: Optional[str] = None,
) -> str:
    """
    Scale (resize) video.

    Args:
        width: Output width (-1 to keep aspect ratio)
        height: Output height (-1 to keep aspect ratio)
        force_original_aspect_ratio: "decrease" or "increase"
        flags: Scaling algorithm (e.g., "lanczos", "bicubic")
    """
    kwargs = {}
    if width is not None:
        kwargs["w"] = width
    if height is not None:
        kwargs["h"] = height
    if force_original_aspect_ratio:
        kwargs["force_original_aspect_ratio"] = force_original_aspect_ratio
    if flags:
        kwargs["flags"] = flags
    return make_filter("scale", **kwargs)


def crop(
    width: Union[int, str],
    height: Union[int, str],
    x: Optional[Union[int, str]] = None,
    y: Optional[Union[int, str]] = None,
) -> str:
    """
    Crop video.

    Args:
        width: Output width
        height: Output height
        x: Horizontal position (default: center)
        y: Vertical position (default: center)
    """
    return make_filter("crop", width, height, x, y)


def fps(framerate: Union[int, float, str]) -> str:
    """
    Convert video to constant frame rate.

    Args:
        framerate: Target frame rate
    """
    return make_filter("fps", fps=framerate)


def overlay(
    x: Union[int, str] = 0,
    y: Union[int, str] = 0,
    eof_action: Optional[str] = None,
    format_: Optional[str] = None,
) -> str:
    """
    Overlay one video on top of another.

    Args:
        x: Horizontal offset
        y: Vertical offset
        eof_action: Action when overlay ends ("repeat", "endall", "pass")
        format_: Pixel format
    """
    kwargs = {"x": x, "y": y}
    if eof_action:
        kwargs["eof_action"] = eof_action
    if format_:
        kwargs["format"] = format_
    return make_filter("overlay", **kwargs)


def pad(
    width: Union[int, str],
    height: Union[int, str],
    x: Optional[Union[int, str]] = None,
    y: Optional[Union[int, str]] = None,
    color: Optional[str] = None,
) -> str:
    """
    Pad video with borders.

    Args:
        width: Output width
        height: Output height
        x: Horizontal position of input
        y: Vertical position of input
        color: Padding color (default: black)
    """
    return make_filter("pad", width, height, x, y, color=color)


def setpts(expr: str) -> str:
    """
    Set presentation timestamp.

    Args:
        expr: PTS expression (e.g., "PTS-STARTPTS", "0.5*PTS")
    """
    return make_filter("setpts", expr)


def transpose(direction: int) -> str:
    """
    Transpose rows and columns.

    Args:
        direction: 0=ccw+vflip, 1=cw, 2=ccw, 3=cw+vflip
    """
    return make_filter("transpose", direction)


def hflip() -> str:
    """Flip video horizontally."""
    return "hflip"


def vflip() -> str:
    """Flip video vertically."""
    return "vflip"


def rotate(angle: Union[float, str], fillcolor: Optional[str] = None) -> str:
    """
    Rotate video.

    Args:
        angle: Rotation angle in radians or expression
        fillcolor: Background fill color
    """
    kwargs = {"a": angle}
    if fillcolor:
        kwargs["fillcolor"] = fillcolor
    return make_filter("rotate", **kwargs)


def drawtext(
    text: Optional[str] = None,
    textfile: Optional[str] = None,
    x: Union[int, str] = 0,
    y: Union[int, str] = 0,
    fontsize: Optional[int] = None,
    fontcolor: Optional[str] = None,
    fontfile: Optional[str] = None,
    box: Optional[int] = None,
    boxcolor: Optional[str] = None,
) -> str:
    """
    Draw text on video.

    Args:
        text: Text string
        textfile: Text file path
        x: Horizontal position
        y: Vertical position
        fontsize: Font size
        fontcolor: Font color
        fontfile: Font file path
        box: Enable text box (1 or 0)
        boxcolor: Box background color
    """
    kwargs = {"x": x, "y": y}
    if text:
        kwargs["text"] = f"'{text}'"
    if textfile:
        kwargs["textfile"] = textfile
    if fontsize:
        kwargs["fontsize"] = fontsize
    if fontcolor:
        kwargs["fontcolor"] = fontcolor
    if fontfile:
        kwargs["fontfile"] = fontfile
    if box is not None:
        kwargs["box"] = box
    if boxcolor:
        kwargs["boxcolor"] = boxcolor
    return make_filter("drawtext", **kwargs)


def fade(
    type_: str = "in",
    start_frame: Optional[int] = None,
    nb_frames: Optional[int] = None,
    start_time: Optional[float] = None,
    duration: Optional[float] = None,
    color: Optional[str] = None,
) -> str:
    """
    Apply fade effect.

    Args:
        type_: "in" or "out"
        start_frame: Start frame number
        nb_frames: Number of frames for fade
        start_time: Start time in seconds
        duration: Duration in seconds
        color: Fade color (default: black)
    """
    kwargs: Dict[str, Any] = {"t": type_}
    if start_frame is not None:
        kwargs["s"] = start_frame
    if nb_frames is not None:
        kwargs["n"] = nb_frames
    if start_time is not None:
        kwargs["st"] = start_time
    if duration is not None:
        kwargs["d"] = duration
    if color:
        kwargs["c"] = color
    return make_filter("fade", **kwargs)


def trim(
    start: Optional[Union[float, str]] = None,
    end: Optional[Union[float, str]] = None,
    start_frame: Optional[int] = None,
    end_frame: Optional[int] = None,
    duration: Optional[float] = None,
) -> str:
    """
    Trim video.

    Args:
        start: Start time in seconds
        end: End time in seconds
        start_frame: Start frame number
        end_frame: End frame number
        duration: Maximum duration
    """
    kwargs = {}
    if start is not None:
        kwargs["start"] = start
    if end is not None:
        kwargs["end"] = end
    if start_frame is not None:
        kwargs["start_frame"] = start_frame
    if end_frame is not None:
        kwargs["end_frame"] = end_frame
    if duration is not None:
        kwargs["duration"] = duration
    return make_filter("trim", **kwargs)


def eq(
    brightness: Optional[float] = None,
    contrast: Optional[float] = None,
    saturation: Optional[float] = None,
    gamma: Optional[float] = None,
) -> str:
    """
    Adjust brightness, contrast, saturation, and gamma.

    Args:
        brightness: -1.0 to 1.0 (default: 0)
        contrast: -1000.0 to 1000.0 (default: 1)
        saturation: 0.0 to 3.0 (default: 1)
        gamma: 0.1 to 10.0 (default: 1)
    """
    kwargs = {}
    if brightness is not None:
        kwargs["brightness"] = brightness
    if contrast is not None:
        kwargs["contrast"] = contrast
    if saturation is not None:
        kwargs["saturation"] = saturation
    if gamma is not None:
        kwargs["gamma"] = gamma
    return make_filter("eq", **kwargs)


def format_(pix_fmts: Union[str, list]) -> str:
    """
    Convert to specified pixel format(s).

    Args:
        pix_fmts: Pixel format(s), e.g., "yuv420p" or ["yuv420p", "rgb24"]
    """
    if isinstance(pix_fmts, list):
        pix_fmts = "|".join(pix_fmts)
    return make_filter("format", pix_fmts=pix_fmts)


def null() -> str:
    """Pass video unchanged."""
    return "null"


def split(outputs: int = 2) -> str:
    """
    Split input into multiple identical outputs.

    Args:
        outputs: Number of outputs
    """
    if outputs == 2:
        return "split"
    return f"split={outputs}"
