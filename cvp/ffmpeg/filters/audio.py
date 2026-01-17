# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional, Union

from cvp.ffmpeg.filters.filter_builder import make_filter


def volume(
    volume: Union[float, str],
    precision: Optional[str] = None,
) -> str:
    """
    Adjust audio volume.

    Args:
        volume: Volume level (e.g., 0.5, "2", "3dB", "-6dB")
        precision: "fixed", "float", or "double"
    """
    kwargs = {"volume": volume}
    if precision:
        kwargs["precision"] = precision
    return make_filter("volume", **kwargs)


def aresample(sample_rate: int) -> str:
    """
    Resample audio.

    Args:
        sample_rate: Target sample rate in Hz
    """
    return make_filter("aresample", sample_rate)


def atempo(tempo: float) -> str:
    """
    Adjust audio tempo (speed).

    Args:
        tempo: Tempo factor (0.5 to 100.0, 1.0 = normal)
    """
    if not 0.5 <= tempo <= 100.0:
        raise ValueError("tempo must be between 0.5 and 100.0")
    return make_filter("atempo", tempo)


def asetpts(expr: str) -> str:
    """
    Set audio presentation timestamp.

    Args:
        expr: PTS expression (e.g., "PTS-STARTPTS", "N/SR/TB")
    """
    return make_filter("asetpts", expr)


def afade(
    type_: str = "in",
    start_sample: Optional[int] = None,
    nb_samples: Optional[int] = None,
    start_time: Optional[float] = None,
    duration: Optional[float] = None,
    curve: Optional[str] = None,
) -> str:
    """
    Apply audio fade effect.

    Args:
        type_: "in" or "out"
        start_sample: Start sample number
        nb_samples: Number of samples for fade
        start_time: Start time in seconds
        duration: Duration in seconds
        curve: Fade curve type
    """
    kwargs: Dict[str, Any] = {"t": type_}
    if start_sample is not None:
        kwargs["ss"] = start_sample
    if nb_samples is not None:
        kwargs["ns"] = nb_samples
    if start_time is not None:
        kwargs["st"] = start_time
    if duration is not None:
        kwargs["d"] = duration
    if curve:
        kwargs["curve"] = curve
    return make_filter("afade", **kwargs)


def atrim(
    start: Optional[Union[float, str]] = None,
    end: Optional[Union[float, str]] = None,
    start_sample: Optional[int] = None,
    end_sample: Optional[int] = None,
    duration: Optional[float] = None,
) -> str:
    """
    Trim audio.

    Args:
        start: Start time in seconds
        end: End time in seconds
        start_sample: Start sample number
        end_sample: End sample number
        duration: Maximum duration
    """
    kwargs = {}
    if start is not None:
        kwargs["start"] = start
    if end is not None:
        kwargs["end"] = end
    if start_sample is not None:
        kwargs["start_sample"] = start_sample
    if end_sample is not None:
        kwargs["end_sample"] = end_sample
    if duration is not None:
        kwargs["duration"] = duration
    return make_filter("atrim", **kwargs)


def aformat(
    sample_fmts: Optional[str] = None,
    sample_rates: Optional[str] = None,
    channel_layouts: Optional[str] = None,
) -> str:
    """
    Convert audio to specified format.

    Args:
        sample_fmts: Sample format(s), e.g., "s16|s32"
        sample_rates: Sample rate(s), e.g., "44100|48000"
        channel_layouts: Channel layout(s), e.g., "stereo|mono"
    """
    kwargs = {}
    if sample_fmts:
        kwargs["sample_fmts"] = sample_fmts
    if sample_rates:
        kwargs["sample_rates"] = sample_rates
    if channel_layouts:
        kwargs["channel_layouts"] = channel_layouts
    return make_filter("aformat", **kwargs)


def pan(channel_layout: str, channel_mapping: str) -> str:
    """
    Remix audio channels.

    Args:
        channel_layout: Output channel layout (e.g., "stereo", "5.1")
        channel_mapping: Channel mapping (e.g., "c0=c0|c1=c1")
    """
    return f"pan={channel_layout}|{channel_mapping}"


def amerge(inputs: int = 2) -> str:
    """
    Merge multiple audio streams.

    Args:
        inputs: Number of inputs
    """
    return make_filter("amerge", inputs=inputs)


def amix(
    inputs: int = 2,
    duration: Optional[str] = None,
    dropout_transition: Optional[float] = None,
) -> str:
    """
    Mix multiple audio inputs.

    Args:
        inputs: Number of inputs
        duration: "longest", "shortest", or "first"
        dropout_transition: Transition time for dropout
    """
    kwargs: Dict[str, Any] = {"inputs": inputs}
    if duration:
        kwargs["duration"] = duration
    if dropout_transition is not None:
        kwargs["dropout_transition"] = dropout_transition
    return make_filter("amix", **kwargs)


def highpass(frequency: float, poles: int = 2) -> str:
    """
    Apply high-pass filter.

    Args:
        frequency: Cutoff frequency in Hz
        poles: Number of poles (1 or 2)
    """
    return make_filter("highpass", f=frequency, poles=poles)


def lowpass(frequency: float, poles: int = 2) -> str:
    """
    Apply low-pass filter.

    Args:
        frequency: Cutoff frequency in Hz
        poles: Number of poles (1 or 2)
    """
    return make_filter("lowpass", f=frequency, poles=poles)


def equalizer(
    frequency: float,
    width_type: str = "q",
    width: float = 1.0,
    gain: float = 0.0,
) -> str:
    """
    Apply equalizer band filter.

    Args:
        frequency: Center frequency in Hz
        width_type: "h" (Hz), "q" (Q-Factor), "o" (octave), "s" (slope)
        width: Bandwidth
        gain: Gain in dB
    """
    return make_filter(
        "equalizer", f=frequency, width_type=width_type, width=width, gain=gain
    )


def compand(
    attacks: str,
    decays: str,
    points: str,
    soft_knee: Optional[float] = None,
    gain: Optional[float] = None,
) -> str:
    """
    Compress or expand audio dynamic range.

    Args:
        attacks: Attack time per channel
        decays: Decay time per channel
        points: Transfer function points
        soft_knee: Soft knee radius in dB
        gain: Output gain in dB
    """
    kwargs: Dict[str, Any] = {"attacks": attacks, "decays": decays, "points": points}
    if soft_knee is not None:
        kwargs["soft-knee"] = soft_knee
    if gain is not None:
        kwargs["gain"] = gain
    return make_filter("compand", **kwargs)


def anull() -> str:
    """Pass audio unchanged."""
    return "anull"


def asplit(outputs: int = 2) -> str:
    """
    Split audio into multiple identical outputs.

    Args:
        outputs: Number of outputs
    """
    if outputs == 2:
        return "asplit"
    return f"asplit={outputs}"


def silenceremove(
    start_periods: int = 1,
    start_duration: float = 0.0,
    start_threshold: float = 0.0,
    stop_periods: int = 0,
    stop_duration: float = 0.0,
    stop_threshold: float = 0.0,
) -> str:
    """
    Remove silence from audio.

    Args:
        start_periods: Number of non-silence periods at start to remove before
        start_duration: Duration of non-silence at start
        start_threshold: Threshold for start silence detection
        stop_periods: Number of silence periods at end to keep (-1 for all)
        stop_duration: Duration for stop detection
        stop_threshold: Threshold for stop silence detection
    """
    return make_filter(
        "silenceremove",
        start_periods=start_periods,
        start_duration=start_duration,
        start_threshold=start_threshold,
        stop_periods=stop_periods,
        stop_duration=stop_duration,
        stop_threshold=stop_threshold,
    )
