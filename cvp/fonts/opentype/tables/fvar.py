# -*- coding: utf-8 -*-
# https://learn.microsoft.com/en-us/typography/opentype/spec/fvar

from typing import Dict, NamedTuple, Optional, Union


class Axis(NamedTuple):
    axis_name_id: int
    axis_tag: str
    default_value: float
    flags: int
    max_value: float
    min_value: float


class InstanceRecord(NamedTuple):
    subfamily_name_id: int
    """
    The name ID for entries in the 'name' table that provide subfamily names for this
    instance.
    """

    flags: int
    """
    Reserved for future use. set to 0.
    """

    coordinates: Dict[str, Union[int, float]]
    """The coordinate array for this instance."""

    post_script_name_id: Optional[int] = None
    """
    The name ID for entries in the 'name' table that provide PostScript names for this
    instance.
    """
