# -*- coding: utf-8 -*-

from enum import Enum, auto, unique
from typing import Final, NamedTuple, Tuple

from imgui_bundle import imgui

from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags import color_var

DEFAULT_VERTICAL_SPLITTER_IDENTIFIER: Final[str] = "## VSplitter"
DEFAULT_HORIZONTAL_SPLITTER_IDENTIFIER: Final[str] = "## HSplitter"
AVAILABLE_REGION_SIZE: Final[float] = -1.0
DEFAULT_SPLITTER_SIZE: Final[float] = 3.0
DEFAULT_SPLITTER_THICKNESS: Final[float] = 2.0


@unique
class SplitterOrientation(Enum):
    vertical = auto()
    horizontal = auto()


class SplitterResult(NamedTuple):
    changed: bool
    hovered: bool
    value: float
    roi: Tuple[float, float, float, float]

    def __bool__(self) -> bool:
        return self.changed


def splitter(
    identifier: str,
    orientation: SplitterOrientation,
    width: float,
    height: float,
    flags=0,
    thickness=DEFAULT_SPLITTER_THICKNESS,
):
    screen_pos = imgui.get_cursor_screen_pos()
    region_size = imgui.get_content_region_avail()

    cx, cy = screen_pos.x, screen_pos.y
    cw, ch = region_size.x, region_size.y

    begin: Tuple[float, float]
    end: Tuple[float, float]

    match orientation:
        case SplitterOrientation.vertical:
            if width <= 0:
                raise ValueError("The 'width' argument must be greater than zero")
            height = height if height >= 0 else ch + height - AVAILABLE_REGION_SIZE
            begin = cx + (width / 2), cy
            end = begin[0], cy + height
        case SplitterOrientation.horizontal:
            if height <= 0:
                raise ValueError("The 'height' argument must be greater than zero")
            width = width if width >= 0 else cw + width - AVAILABLE_REGION_SIZE
            begin = cx, cy + (height / 2)
            end = cx + width, begin[1]
        case _:
            assert False, "Inaccessible Section"

    width = width if width != 0.0 else -1.0
    height = height if height != 0.0 else -1.0

    imgui.invisible_button(identifier, (width, height), flags)
    item_active = imgui.is_item_active()
    item_hovered = imgui.is_item_hovered()

    if item_active:
        style = color_var.SEPARATOR_ACTIVE
    elif item_hovered:
        style = color_var.SEPARATOR_HOVERED
    else:
        style = color_var.SEPARATOR

    color = imgui.get_style_color_vec4(style)
    stroke_color = imgui.get_color_u32(color)

    draw_list = get_window_draw_list()
    draw_list.add_line(begin[0], begin[1], end[0], end[1], stroke_color, thickness)
    roi = begin[0], begin[1], end[0], end[1]

    if item_active:
        match orientation:
            case SplitterOrientation.vertical:
                mouse_delta = imgui.get_io().mouse_delta.x
            case SplitterOrientation.horizontal:
                mouse_delta = imgui.get_io().mouse_delta.y
            case _:
                assert False, "Inaccessible Section"
        return SplitterResult(True, item_hovered, mouse_delta, roi)
    else:
        return SplitterResult(False, item_hovered, 0, roi)


def vertical_splitter(
    identifier=DEFAULT_VERTICAL_SPLITTER_IDENTIFIER,
    width=DEFAULT_SPLITTER_SIZE,
    height=AVAILABLE_REGION_SIZE,
    flags=0,
    thickness=DEFAULT_SPLITTER_THICKNESS,
):
    return splitter(
        identifier=identifier,
        orientation=SplitterOrientation.vertical,
        width=width,
        height=height,
        flags=flags,
        thickness=thickness,
    )


def horizontal_splitter(
    identifier=DEFAULT_HORIZONTAL_SPLITTER_IDENTIFIER,
    width=AVAILABLE_REGION_SIZE,
    height=DEFAULT_SPLITTER_SIZE,
    flags=0,
    thickness=DEFAULT_SPLITTER_THICKNESS,
):
    return splitter(
        identifier=identifier,
        orientation=SplitterOrientation.horizontal,
        width=width,
        height=height,
        flags=flags,
        thickness=thickness,
    )
